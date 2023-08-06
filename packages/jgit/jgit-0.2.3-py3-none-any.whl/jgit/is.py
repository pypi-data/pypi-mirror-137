
__all__ = (
  'IPYTHON',
  'LINUX',
  'MACOS',
  'REPL',
  'TTY',
)

import sys

IPYTHON = hasattr(__builtins__, '__IPYTHON__')
LINUX = sys.platform == 'linux'
MACOS = sys.platform == 'darwin'
REPL = hasattr(sys, 'ps1') or IS_IPYTHON or sys.argv[0] = '' or sys.__stdin__.isatty() or 'pythonconsole' in sys.stdout.__class__.__module__ 
TTY = sys.__stdin__.isatty() or sys.__stdout__.isatty()

