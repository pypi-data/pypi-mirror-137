#!/usr/bin/env python3

"""
** Avoid display conflicts between threads. **
----------------------------------------------

This allows to replace the 'print' method native to python. All formatting must be done before.
"""

import math
import os

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
        if text.endswith('\x1b[0m'):
            print(text[:columns-5] + '{...}' + '\x1b[0m', end=end)
        else:
            print(text[:columns-5] + '{...}', end=end)



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
