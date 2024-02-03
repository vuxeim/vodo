import sys
import string

class UnknownKey(Exception):
    pass

class Printable:
    TICK = '`'
    TILDE = '~'
    EXCLAMATION = '!'
    AT = '@'
    HASH = '#'
    DOLAR = '$'
    PERCENT = '%'
    CARET = '^'
    AMPERSAND = '&'
    ASTERISK = '*'
    OPEN_PAREN = '('
    CLOSE_PAREN = ')'
    MINUS = '-'
    UNDERSCORE = '_'
    EQUALS = '='
    PLUS = '+'
    OPEN_SQUARE_BRACKET = '['
    CLOSE_SQUARE_BRACKET = ']'
    OPEN_CURLY_BRACKET = '{'
    CLOSE_CURLY_BRACKET = '}'
    BACKSLASH = '\\'
    PIPE = '|'
    SEMICOLON = ';'
    COLON = ':'
    APOSTROPHE = '\''
    QUOTE = '"'
    COMMA = ','
    PERIOD = '.'
    LESS_THAN = '<'
    GREATER_THAN = '>'
    SLASH = '/'
    QUESTION = '?'
    SPACE = ' '
    TAB = '\t'

for c in string.ascii_lowercase:
    up = c.upper()
    up_name = 'SHIFT_'+up
    setattr(Printable, up, c)
    setattr(Printable, up_name, up)

for n in string.digits:
    setattr(Printable, 'N'+n, n)

class Alias:
    BANG = Printable.EXCLAMATION
    DOUBLE_QUOTE = Printable.QUOTE
    LT = Printable.LESS_THAN
    GT = Printable.GREATER_THAN
    WHAT = Printable.QUESTION
    QUESTION_MARK = Printable.QUESTION
    EXCLAMATION_MARK = Printable.EXCLAMATION
    DOT = Printable.PERIOD
    BACKTICK = Printable.TICK
    STAR = Printable.ASTERISK

class Windows:
    ESC = '\x1b'
    ENTER = '\r'
    BACKSPACE = '\x08'
    LEFT = '\xe0K'
    RIGHT = '\xe0M'
    UP = '\xe0H'
    DOWN = '\xe0P'
    INSERT = '\xe0R'
    DELETE = '\xe0S'
    PAGE_UP = '\xe0I'
    PAGE_DOWN = '\xe0Q'
    HOME = '\xe0G'
    END = '\xe0O'

class Linux:
    ESC = '\x1b'
    ENTER = '\n'
    BACKSPACE = '\x7f'
    UP = '\x1b[A'
    DOWN = '\x1b[B'
    LEFT = '\x1b[D'
    RIGHT = '\x1b[C'
    SHIFT_UP = '\x1b[a'
    SHIFT_DOWN = '\x1b[b'
    SHIFT_LEFT = '\x1b[d'
    SHIFT_RIGHT = '\x1b[c'
    INSERT = '\x1b[2~'
    DELETE = '\x1b[3~'
    PAGE_UP = '\x1b[5'
    PAGE_DOWN = '\x1b[6'
    HOME = '\x1b[H'
    END = '\x1b[F'

class Key:

    def __init__(self) -> None:

        printable = __class__._get(Printable)
        alias = __class__._get(Alias)
        platform = {'linux': Linux, 'win32': Windows}[sys.platform]
        special = __class__._get(platform)

        self._keys: dict = printable | alias | special

    @staticmethod
    def _get(keygroup: type) -> dict[str, str]:
        keys = {}
        for name in dir(keygroup):
            if name == name.upper() and not name.startswith('_'):
                keys[name] = getattr(keygroup, name)
        return keys


    def __getattr__(self, name: str) -> str:
        code = self._keys.get(name)
        if code is not None:
            return code
        raise UnknownKey(f'Key named \'{name}\' does not exist')

key = Key()
