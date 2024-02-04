# Initially taken from:
# http://code.activestate.com/recipes/134892/
from contextlib import contextmanager, nullcontext
import codecs
import os
import sys

from .keynames import PLATFORM_KEYS

class Platform:

    def __init__(self):
        self.keys = PLATFORM_KEYS[self.KEYS]

    def getkey(self):
        buffer = ''
        for c in self.getchars():
            buffer += c
            if buffer not in self.keys.escapes:
                break
        keycode = self.keys.canon(buffer)
        if keycode == self.keys.code('CTRL_C'):
            raise KeyboardInterrupt
        return keycode

class PlatformUnix(Platform):
    KEYS = 'unix'

    def __init__(self):
        super().__init__()
        import termios
        self.termios = termios
        import tty
        self.tty = tty
        self._fd = sys.stdin.fileno()
        self._decoder = codecs.getincrementaldecoder(sys.stdin.encoding)()

    def getchars(self):
        yield self.read()

    def read(self):
        return self._decoder.decode(os.read(self._fd, 1))

    @contextmanager
    def context(self):
        settings = self.termios.tcgetattr(self._fd)
        self.tty.setcbreak(self._fd)
        try:
            yield
        finally:
            self.termios.tcsetattr(self._fd, termios.TCSADRAIN, settings)

class PlatformWindows(Platform):
    KEYS = 'windows'

    def __init__(self):
        super().__init__()
        import msvcrt
        self.msvcrt = msvcrt

    def getchars(self):
        yield self.read()

    def read(self, chars=1):
        buffer = bytes()
        while len(buffer) < chars:
            buffer += self.msvcrt.getch()
            # If the pressed key was a special function key,
            # this will return '\000' or '\xe0';
            # the next call will return the keycode.
            # https://docs.python.org/3/library/msvcrt.html#msvcrt.getch 
            if self.msvcrt.kbhit():
                buffer += self.msvcrt.getch()
        return buffer.decode('windows-1252')

    context = nullcontext

def windows_or_unix():
    try:
        from ctypes import WinDLL
    except ImportError:
        return PlatformUnix()
    else:
        return PlatformWindows()

PLATFORMS = [
    ('linux', PlatformUnix),
    ('darwin', PlatformUnix),
    ('win32', PlatformWindows),
    ('cygwin', windows_or_unix),
]

def get_platform():
    for prefix, ctor in PLATFORMS:
        if sys.platform.startswith(prefix):
            return ctor()

platform = get_platform()
getkey = platform.getkey
context = platform.context
