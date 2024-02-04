# Initially taken from:
# http://code.activestate.com/recipes/134892/
# Thanks to Danny Yoo
from __future__ import absolute_import, print_function
from contextlib import contextmanager
import codecs
import os
import sys

from .keynames import PLATFORM_KEYS

class Platform:
    def __init__(self):
        keys = self.KEYS
        if isinstance(keys, str):
            keys = PLATFORM_KEYS[keys]
        self.key = self.keys = keys
        interrupts = self.INTERRUPTS
        self.interrupts = {self.keys.code(name): action for name, action in interrupts.items()}

        assert(self.__class__.getchar != Platform.getchar or
            self.__class__.getchars != Platform.getchars)

    def getkey(self, blocking=True):
        buffer = ''
        for c in self.getchars(blocking):
            buffer += c
            if buffer not in self.keys.escapes:
                break

        keycode = self.keys.canon(buffer)
        if keycode in self.interrupts:
            interrupt = self.interrupts[keycode]
            if isinstance(interrupt, BaseException) or \
                issubclass(interrupt, BaseException):
                raise interrupt
            else:
                raise NotImplementedError(f'Unimplemented interrupt: {interrupt!r}')
        return keycode

    def bang(self):
        while True:
            code = self.getkey(True)
            name = self.keys.name(code) or '???'
            print(f'{name} = {code!r}')

    def getchars(self, blocking=True):
        char = self.getchar(blocking)
        while char:
            yield char
            char = self.getchar(False)

    def getchar(self, blocking=True):
        for char in self.getchars(blocking):
            return char
        return None


class PlatformUnix(Platform):
    KEYS = 'unix'
    INTERRUPTS = {'CTRL_C': KeyboardInterrupt}

    def __init__(self):
        super().__init__()
        self.stdin = sys.stdin
        from select import select
        import tty
        import termios
        self.select = select
        self.tty = tty
        self.termios = termios
        self.__decoded_stream = OSReadWrapper(self.stdin)

    def fileno(self):
        return self.__decoded_stream.fileno()

    @contextmanager
    def context(self):
        fd = self.fileno()
        old_settings = self.termios.tcgetattr(fd)
        assert old_settings[3] & 8
        self.tty.setcbreak(fd)
        try:
            yield
        finally:
            old_settings[3] |= 8
            assert old_settings[3] & 8
            self.termios.tcsetattr(fd, self.termios.TCSADRAIN, old_settings)
            old_settings = self.termios.tcgetattr(fd)
            assert old_settings[3] & 8

    def getchars(self, blocking=True):
        with self.context():
            if blocking:
                yield self.__decoded_stream.read()
            while self.select([self.fileno()], [], [], 0)[0]:
                yield self.__decoded_stream.read()

class OSReadWrapper:

    def __init__(self, stream):
        self.__stream = stream
        self.__fd = stream.fileno()
        self.encoding = stream.encoding
        self.__decoder = codecs.getincrementaldecoder(self.encoding)()

    def fileno(self):
        return self.__fd

    @property
    def buffer(self):
        return self.__stream.buffer

    def read(self):
        return self.__decoder.decode(os.read(self.__fd, 1))

class PlatformWindows(Platform):
    KEYS = 'windows'
    INTERRUPTS = {'CTRL_C': KeyboardInterrupt}

    def __init__(self):
        super().__init__()
        import msvcrt
        self.msvcrt = msvcrt

    def getchars(self, blocking=True):
        if blocking:
            yield self.read(1)
        while self.msvcrt.kbhit():
            yield self.read(1)

    def read(self, chars):
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

def windows_or_unix():
    try:
        import msvcrt
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

def platform():
    for prefix, ctor in PLATFORMS:
        if sys.platform.startswith(prefix):
            return ctor()
    raise NotImplementedError('Unknown platform {sys.platform!r}')
