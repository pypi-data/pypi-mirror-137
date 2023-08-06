#!/usr/bin/env python3

"""
** Avoid display conflicts between threads. **
----------------------------------------------

This allows to replace the 'print' method native to python. All formatting must be done before.
"""

import math
import os
import re

from context_verbose.memory import get_lifo


def print_safe(text, *, end='\n'):
    """
    ** Replacement of 'print'. **

    Constrained to display in a particular area to avoid mixing between threads.

    Parameters
    ----------
    text : str
        The string to display
    end : str, optional
        Transfer directly to the native ``print`` function.
    """
    assert isinstance(text, str)

    columns, _ = get_terminal_size()
    if len(text) <= columns or columns <= 5:
        print(text, end=end)
    else:
        print('\n'.join(truncate(text, columns)))


def truncate(string, size):
    r"""
    ** Allows to cut the text without breaking the special characters. **

    Parameters
    ----------
    string : str
        The text to be cut, which can contain text formatting characters.

    Returns
    -------
    sections : list
        Each element of the list is a portion of the
        text cut in order to ensure correct formatting.

    Examples
    --------
    >>> from context_verbose.color import format_text
    >>> from context_verbose.thread_safe import truncate
    >>> format_text('test_string')
    'test_string'
    >>> truncate(_, 7)
    ['test_st', 'ring']
    >>> format_text('test_string', color='blue')
    '\x1b[22m\x1b[34mtest_string\x1b[0m'
    >>> truncate(_, 7)
    ['\x1b[22m\x1b[34mtest_st\x1b[0m', '\x1b[22m\x1b[34mring\x1b[0m']
    >>> format_text('test_string', color='blue') + format_text('test_string', color='red')
    '\x1b[22m\x1b[34mtest_string\x1b[0m\x1b[22m\x1b[31mtest_string\x1b[0m'
    >>> truncate(_, 11)
    ['\x1b[22m\x1b[34mtest_string\x1b[0m', '\x1b[22m\x1b[34m\x1b[0m\x1b[22m\x1b[31mtest_string\x1b[0m']
    >>>
    """
    assert isinstance(string, str)
    assert isinstance(size, int)
    assert size > 0

    sections = []
    specials = list(re.finditer(r'\x1b\[\S+?m', string))

    # cutting in packages of the right size
    clean_string = string
    for special_str in {m.group() for m in specials}:
        clean_string = clean_string.replace(special_str, '')
    while clean_string:
        sections.append(clean_string[:size])
        clean_string = clean_string[size:]

    # repositioning of special chains
    dec = 0
    positions = {}
    for special in specials:
        start, end = special.span()
        positions[start-dec] = positions.get(start-dec, '') + special.group()
        dec += end - start

    # added markup
    current_markers = ''
    loc_dec = 0
    for dec, section in enumerate(sections.copy()):
        section = current_markers + section
        loc_dec = len(current_markers)
        for i in range(size):
            if i + dec*size in positions:
                special = positions[i + dec*size]
                section = section[:i+loc_dec] + special + section[i+loc_dec:]
                if special == '\x1b[0m':
                    current_markers = ''
                else:
                    current_markers += special
                loc_dec += len(special)
        if current_markers:
            section += '\x1b[0m'
        sections[dec] = section

    if not string.endswith('\x1b[0m') and sections[-1].endswith('\x1b[0m'):
        sections[-1] = sections[-1][:-4]
    return sections


def get_terminal_size():
    """
    ** Recover the dimensions of the terminal. **

    Returns
    -------
    columns : int
        The number of columns in the terminal.
    lines : int
        The number of lines present in the terminal.

    Examples
    --------
    >>> import tempfile
    >>> import sys
    >>> from context_verbose.thread_safe import get_terminal_size
    >>> size = get_terminal_size()
    >>> size # doctest: +SKIP
    (100, 30)
    >>> stdout = sys.stdout
    >>> with tempfile.TemporaryFile('w', encoding='utf-8') as file:
    ...     sys.stdout = file
    ...     size = get_terminal_size()
    ...
    >>> sys.stdout = stdout
    >>> size
    (100, inf)
    >>>
    """
    try:
        size = os.get_terminal_size()
    except OSError:
        return get_lifo().columns, math.inf
    else:
        return size.columns, size.lines
