
__all__ = (
  'IPYTHON',
  'REPL',
  'TTY',
)

import sys

"""Is Interactive ipython"""
IPYTHON: bool = hasattr(__builtins__, '__IPYTHON__')
"""Inside a REPL, has sys.ps1, or IPYTHON, or sys.argv '' or stdin is a tty"""
REPL: bool = hasattr(sys, 'ps1') or IPYTHON or sys.argv[0] == '' or sys.__stdin__.isatty() or 'pythonconsole' in sys.stdout.__class__.__module__ 
"""Is sys stdin or stdout a tty"""
TTY: bool = sys.__stdin__.isatty() or sys.__stdout__.isatty()

