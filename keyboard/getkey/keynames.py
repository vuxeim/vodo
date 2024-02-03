# Which key(s) were pressed
# What chars to print (if any)
# Keycode(s) generating event
import string


class UnicodeAsciiKeys:
    NULL = '\x00'
    START_OF_HEADING = '\x01'
    START_OF_TEXT = '\x02'
    END_OF_TEXT = '\x03'
    END_OF_TRANSMISSION = '\x04'
    ENQUIRY = '\x05'
    ACKNOWLEDGE = '\x06'
    BELL = '\x07'
    BACKSPACE = '\x08'
    CHARACTER_TABULATION = '\t'
    HORIZONTAL_TABULATION = '\t'
    TAB = '\t'
    LINE_FEED = '\n'
    NEW_LINE = '\n'
    END_OF_LINE = '\n'
    LINE_TABULATION = '\x0b'
    VERTICAL_TABULATION = '\x0b'
    FORM_FEED = '\x0c'
    CARRIAGE_RETURN = '\r'
    SHIFT_OUT = '\x0e'
    SHIFT_IN = '\x0f'
    DATA_LINK_ESCAPE = '\x10'
    DEVICE_CONTROL_ONE = '\x11'
    DEVICE_CONTROL_TWO = '\x12'
    DEVICE_CONTROL_THREE = '\x13'
    DEVICE_CONTROL_FOUR = '\x14'
    NEGATIVE_ACKNOWLEDGE = '\x15'
    SYNCHRONOUS_IDLE = '\x16'
    END_OF_TRANSMISSION_BLOCK = '\x17'
    CANCEL = '\x18'
    END_OF_MEDIUM = '\x19'
    SUBSTITUTE = '\x1a'
    ESCAPE = '\x1b'
    INFORMATION_SEPARATOR_FOUR = '\x1c'
    FILE_SEPARATOR = '\x1c'
    INFORMATION_SEPARATOR_THREE = '\x1d'
    GROUP_SEPARATOR = '\x1d'
    INFORMATION_SEPARATOR_TWO = '\x1e'
    RECORD_SEPARATOR = '\x1e'
    INFORMATION_SEPARATOR_ONE = '\x1f'
    UNIT_SEPARATOR = '\x1f'
    SPACE = ' '
    EXCLAMATION_MARK = '!'
    FACTORIAL = '!'
    BANG = '!'
    QUOTATION_MARK = '"'
    NUMBER_SIGN = '#'
    POUND_SIGN = '#'
    HASH = '#'
    CROSSHATCH = '#'
    OCTOTHORPE = '#'
    DOLLAR_SIGN = '$'
    ESCUDO = '$'
    PERCENT_SIGN = '%'
    AMPERSAND = '&'
    APOSTROPHE = "'"
    APOSTROPHE_QUOTE = "'"
    APL_QUOTE = "'"
    LEFT_PARENTHESIS = '('
    OPENING_PARENTHESIS = '('
    RIGHT_PARENTHESIS = ')'
    CLOSING_PARENTHESIS = ')'
    ASTERISK = '*'
    STAR = '*'
    PLUS_SIGN = '+'
    COMMA = ','
    DECIMAL_SEPARATOR = ','
    HYPHEN_MINUS = '-'
    HYPHEN_OR_MINUS_SIGN = '-'
    FULL_STOP = '.'
    PERIOD = '.'
    DOT = '.'
    DECIMAL_POINT = '.'
    SOLIDUS = '/'
    SLASH = '/'
    VIRGULE = '/'
    DIGIT_ZERO = '0'
    DIGIT_ONE = '1'
    DIGIT_TWO = '2'
    DIGIT_THREE = '3'
    DIGIT_FOUR = '4'
    DIGIT_FIVE = '5'
    DIGIT_SIX = '6'
    DIGIT_SEVEN = '7'
    DIGIT_EIGHT = '8'
    DIGIT_NINE = '9'
    COLON = ':'
    SEMICOLON = ';'
    LESS_THAN_SIGN = '<'
    EQUALS_SIGN = '='
    GREATER_THAN_SIGN = '>'
    QUESTION_MARK = '?'
    COMMERCIAL_AT = '@'
    AT_SIGN = '@'
    LATIN_CAPITAL_LETTER_A = 'A'
    LATIN_CAPITAL_LETTER_B = 'B'
    LATIN_CAPITAL_LETTER_C = 'C'
    LATIN_CAPITAL_LETTER_D = 'D'
    LATIN_CAPITAL_LETTER_E = 'E'
    LATIN_CAPITAL_LETTER_F = 'F'
    LATIN_CAPITAL_LETTER_G = 'G'
    LATIN_CAPITAL_LETTER_H = 'H'
    LATIN_CAPITAL_LETTER_I = 'I'
    LATIN_CAPITAL_LETTER_J = 'J'
    LATIN_CAPITAL_LETTER_K = 'K'
    LATIN_CAPITAL_LETTER_L = 'L'
    LATIN_CAPITAL_LETTER_M = 'M'
    LATIN_CAPITAL_LETTER_N = 'N'
    LATIN_CAPITAL_LETTER_O = 'O'
    LATIN_CAPITAL_LETTER_P = 'P'
    LATIN_CAPITAL_LETTER_Q = 'Q'
    LATIN_CAPITAL_LETTER_R = 'R'
    LATIN_CAPITAL_LETTER_S = 'S'
    LATIN_CAPITAL_LETTER_T = 'T'
    LATIN_CAPITAL_LETTER_U = 'U'
    LATIN_CAPITAL_LETTER_V = 'V'
    LATIN_CAPITAL_LETTER_W = 'W'
    LATIN_CAPITAL_LETTER_X = 'X'
    LATIN_CAPITAL_LETTER_Y = 'Y'
    LATIN_CAPITAL_LETTER_Z = 'Z'
    LEFT_SQUARE_BRACKET = '['
    OPENING_SQUARE_BRACKET = '['
    REVERSE_SOLIDUS = '\\'
    BACKSLASH = '\\'
    RIGHT_SQUARE_BRACKET = ']'
    CLOSING_SQUARE_BRACKET = ']'
    CIRCUMFLEX_ACCENT = '^'
    LOW_LINE = '_'
    SPACING_UNDERSCORE = '_'
    GRAVE_ACCENT = '`'
    LATIN_SMALL_LETTER_A = 'a'
    LATIN_SMALL_LETTER_B = 'b'
    LATIN_SMALL_LETTER_C = 'c'
    LATIN_SMALL_LETTER_D = 'd'
    LATIN_SMALL_LETTER_E = 'e'
    LATIN_SMALL_LETTER_F = 'f'
    LATIN_SMALL_LETTER_G = 'g'
    LATIN_SMALL_LETTER_H = 'h'
    LATIN_SMALL_LETTER_I = 'i'
    LATIN_SMALL_LETTER_J = 'j'
    LATIN_SMALL_LETTER_K = 'k'
    LATIN_SMALL_LETTER_L = 'l'
    LATIN_SMALL_LETTER_M = 'm'
    LATIN_SMALL_LETTER_N = 'n'
    LATIN_SMALL_LETTER_O = 'o'
    LATIN_SMALL_LETTER_P = 'p'
    LATIN_SMALL_LETTER_Q = 'q'
    LATIN_SMALL_LETTER_R = 'r'
    LATIN_SMALL_LETTER_S = 's'
    LATIN_SMALL_LETTER_T = 't'
    LATIN_SMALL_LETTER_U = 'u'
    LATIN_SMALL_LETTER_V = 'v'
    LATIN_SMALL_LETTER_W = 'w'
    LATIN_SMALL_LETTER_X = 'x'
    LATIN_SMALL_LETTER_Y = 'y'
    LATIN_SMALL_LETTER_Z = 'z'
    LEFT_CURLY_BRACKET = '{'
    OPENING_CURLY_BRACKET = '{'
    LEFT_BRACE = '{'
    VERTICAL_LINE = '|'
    VERTICAL_BAR = '|'
    RIGHT_CURLY_BRACKET = '}'
    CLOSING_CURLY_BRACKET = '}'
    RIGHT_BRACE = '}'
    TILDE = '~'
    DELETE = '\x7f'


# These are used for the names of ctrl keys, etc.
ASCII_NAMES = {
    '\t': 'tab',
    ' ': 'space',          # 0x20
    '!': 'exclamation',    # 0x21
    '"': 'double quote',   # 0x22
    '#': 'hash',           # 0x23
    '$': 'dollar',         # 0x24
    '%': 'percent',        # 0x25
    '&': 'ampersand',      # 0x26
    '\'': 'single quote',  # 0x27
    '(': 'open paren',     # 0x28
    ')': 'close paren',    # 0x29
    '*': 'asterisk',       # 0x2a
    '+': 'plus',           # 0x2b
    ',': 'comma',          # 0x2c
    '-': 'minus',          # 0x2d
    '.': 'period',         # 0x2e
    '/': 'slash',          # 0x2f

    ':': 'colon',          # 0x3a
    ';': 'semicolon',      # 0x3b
    '<': 'less than',      # 0x3c
    '=': 'equals',         # 0x3d
    '>': 'greater than',   # 0x3e
    '?': 'question',       # 0x3f
    '@': 'at',             # 0x40

    '[': 'left bracket',   # 0x5b
    '\\': 'backslash',     # 0x5c
    ']': 'right bracket',  # 0x5d
    '^': 'caret',          # 0x5e
    '_': 'underscore',     # 0x5f
    '`': 'backtick',       # 0x60

    '{': 'left brace',     # 0x7b
    '|': 'pipe',           # 0x7c
    '}': 'right brace',    # 0x7d
    '~': 'tilde',          # 0x7e
}


class UnicodeKeys:
    """ Represents Unicode keys """
    # Names from ftp://ftp.unicode.org/Public/UNIDATA/NamesList.txt
    NULL = chr(0x00)
    START_OF_HEADING = chr(0x01)


class JargonKeys:
    """ Represents common names for keys """
    BANG = '!'
    SHRIEK = '!'
    DOUBLE_QUOTE = '"'
    QUOTE = '"'
    NUMBER_SIGN = '#'
    SHARP = '#'
    OCTOTHORPE = '#'
    BUCK = '$'
    CASH = '$'
    STRING = '$'
    MOD = '%'
    GRAPES = '%'
    AMPERSAND = '&'
    AMP = '&'
    AND_SIGN = '&'
    APOSTROPHE = '\''
    PRIME = '\''
    TICK = '\''
    STAR = '*'
    SPLAT = '*'
    GLOB = '*'
    ADD = '+'


class IntercalKeys:
    """ Represents itercal keys """
    SPOT = '.'
    TWO_SPOT = ':'
    TAIL = ','
    HYBRID = ';'
    MESH = '#'
    HALF_MESH = '='
    SPARK = '\''
    BACKSPARK = '`'
    WOW = '!'
    WHAT = '?'
    RABBIT_EARS = '"'
    # RABBIT is `"` over `.`
    SPIKE = '|'
    DOUBLE_OH_SEVEN = '%'
    WORM = '-'
    ANGLE = '<'
    RIGHT_ANGLE = '>'
    WAX = '('
    WANE = ')'
    U_TURN = '['
    U_TURN_BACK = ']'
    EMBRACE = '{'
    BRACELET = '}'
    SPLAT = '*'
    AMPERSAND = '&'
    V = 'V'
    BOOK = 'V'
    # BOOKWORM is `-` over `V`
    BIG_MONEY = '$'
    # CHANGE is cent sign
    SQUIGGLE = '~'
    FLAT_WORM = '_'
    # OVERLINE is line on top
    INTERSECTION = '+'
    SLAT = '/'
    BACKSLAT = '\\'
    WHIRLPOOL = '@'
    # HOOKWORK is logical NOT symbol
    SHARK = '^'
    SHARKFIN = '^'
    # BLOTCH is several characters smashed on top of each other


class VT100StandardModeKeys:
    """ Represents VT100 terminal standard keys """
    # http://www.braun-home.net/michael/mbedit/info/misc/VT100_commands.htm
    # http://www.ccs.neu.edu/research/gpc/MSim/vona/terminal/VT100_Escape_Codes.html
    F1 = '\x1bOP'
    F2 = '\x1bOQ'
    F3 = '\x1bOR'
    F4 = '\x1bOS'

    UP = '\x1b[A'
    SHIFT_UP = '\x1b[a'
    DOWN = '\x1b[B'
    RIGHT = '\x1b[C'
    LEFT = '\x1b[D'


class UnixKeys:
    """ Represents Unix keys """
    # Keys found experimentally, of unknown provenance
    ESC = '\x1b'

    HOME = '\x1b[H'
    END = '\x1b[F'
    PAGE_UP = '\x1b[5'
    PAGE_DOWN = '\x1b[6'

    ENTER = '\n'
    CR = '\r'
    BACKSPACE = '\x7f'

    SPACE = ' '

    INSERT = '\x1b[2~'
    DELETE = '\x1b[3~'


class AlternativeUnixFunctionKeys:
    """ Represents alternative Unix keys """
    # Unsure origin: alternate V220 mode?
    F1 = '\x1bO11~'
    F2 = '\x1bO12~'
    F3 = '\x1bO13~'
    F4 = '\x1bO14~'
    F5 = '\x1bO15~'
    F6 = '\x1bO17~'
    F7 = '\x1bO18~'
    F8 = '\x1bO19~'
    F9 = '\x1bO20~'
    F10 = '\x1bO21~'
    F11 = '\x1bO23~'
    F12 = '\x1bO24~'


class ControlKeys:
    """ Represents control keys """
    def __init__(self, fmt='CTRL_{}'):
        for i in range(0x20):
            low_char = chr(i)
            high_char = chr(i + 0x40)
            name = ASCII_NAMES.get(high_char, high_char).upper()
            ctrl_name = fmt.format(name)
            setattr(self, ctrl_name, low_char)


class AsciiKeys:
    def __init__(self,
                 lower_format='{}',
                 upper_format='SHIFT_{}',
                 digit_format='N{}',
                 ascii_names=ASCII_NAMES,
    ):
        for letter in string.ascii_lowercase:
            name = lower_format.format(letter.upper())
            setattr(self, name, letter)

        for letter in string.ascii_uppercase:
            name = upper_format.format(letter.upper())
            setattr(self, name, letter)

        for digit in string.digits:
            name = digit_format.format(digit)
            setattr(self, name, digit)

        for char, name in ascii_names.items():
            name = name.upper().replace(' ', '_')
            setattr(self, name, char)


class Keys:
    def __init__(self, keyclasses):
        self.__names = dict()  # Map of codes -> names
        self.__codes = dict()  # Map of names -> codes

        self.__escapes = set()

        for keyclass in keyclasses:
            for name in dir(keyclass):
                if self._is_key_name(name):
                    code = getattr(keyclass, name)
                    self.register(name, code)

    def register(self, name, code):
        if name not in self.__codes:
            self.__codes[name] = code
        if code not in self.__names:
            self.__names[code] = name
        for i in range(len(code)):
            self.__escapes.add(code[:i])

        # Update towards canonicity
        while True:
            canon_code = self.canon(code)
            canon_canon_code = self.canon(canon_code)
            if canon_code != canon_canon_code:
                self.__codes[self.name(code)] = canon_canon_code
            else:
                break
        while True:
            canon_name = self.name(self.code(name))
            canon_canon_name = self.name(self.code(canon_name))
            if canon_name != canon_canon_name:
                self.__names[self.code(name)] = canon_canon_name
            else:
                break

    @property
    def escapes(self):
        return self.__escapes

    @property
    def names(self):
        return self.__codes.keys()

    def name(self, code):
        return self.__names.get(code)

    def code(self, name):
        return self.__codes.get(name)

    def canon(self, code):
        name = self.name(code)
        return self.code(name) if name else code

    def __getattr__(self, name):
        code = self.code(name)
        if code is not None:
            return code
        return self.__getattribute__(name)

    def _is_key_name(self, name):
        return name == name.upper() and not name.startswith('_')


def __make_escapes(codes):
    escapes = set()
    for code in codes:
        for i in range(len(code)):
            escapes.add(code[:i])
    return escapes


both = {
    AsciiKeys(),
    ControlKeys(),
    UnicodeAsciiKeys(),
    JargonKeys(),
    IntercalKeys(),
    UnixKeys(),
    AlternativeUnixFunctionKeys(),
    VT100StandardModeKeys(),
}

PLATFORM_KEYS = {
    'unix': Keys(both),
}
