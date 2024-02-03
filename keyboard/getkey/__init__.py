from __future__ import absolute_import, print_function
import sys

from .platforms import platform

__platform = platform()

getkey = __platform.getkey
# keys = __platform.keys
# key = keys # alias
# bang = __platform.bang
