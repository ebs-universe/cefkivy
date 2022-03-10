

from collections import namedtuple

KeyCode = namedtuple('keycode', 'unix windows character is_special shift capslock')

# Windows codes from https://boostrobotics.eu/windows-key-codes/
# Unix codes from Dell...

# Obviously, gave up entirely on trying to keep windows codes straight when shift
# etc. came into play.

_codes = [
    KeyCode(301, 20, 'capslock', True, 0, False),
    KeyCode(27, 27, 'escape', True, 0, False),
    KeyCode(8, 8, 'backspace', True, 0, False),
    KeyCode(9, 9, 'tab', True, 0, False),
    KeyCode(13, 13, 'enter', True, 0, False),
    KeyCode(271, 13, 'enter', True, 0, False),
    KeyCode(304, 160, 'lshift', True, 0, False),
    KeyCode(303, 161, 'rshift', True, 0, False),
    KeyCode(305, 162, 'lctrl', True, 0, False),
    KeyCode(306, 163, 'rctrl', True, 0, False),
    KeyCode(308, 164, 'lalt', True, 0, False),
    KeyCode(313, 165, 'ralt', True, 0, False),
    KeyCode(307, 18, 'alt-gr', True, 0, False), # NOTE AltGr and ralt are actually different keys.
    KeyCode(277, 45, 'insert', True, 0, False),
    KeyCode(127, 46, 'delete', True, 0, False),
    KeyCode(278, 36, 'home', True, 0, False),
    KeyCode(279, 35, 'end', True, 0, False),
    KeyCode(280, 33, 'pageup', True, 0, False),
    KeyCode(281, 34, 'pagedown', True, 0, False),
    KeyCode(276, 37, 'left', True, 0, False),
    KeyCode(273, 38, 'up', True, 0, False),
    KeyCode(275, 39, 'right', True, 0, False),
    KeyCode(274, 40, 'down', True, 0, False),
    KeyCode(32, 32, ' ', False, 0, False),
    KeyCode(91, 91, '[', False, ord('{') - 91, False),
    KeyCode(93, 93, ']', False, ord('}') - 93, False),
    KeyCode(59, 59, ';', False, ord(':') - 59, False),
    KeyCode(39, 39, "'", False, ord('"') - 39, False),
    KeyCode(47, 47, '/', False, ord('?') - 47, False),
    KeyCode(92, 92, '\\', False, ord('|') - 92, False),
    KeyCode(96, 96, '`', False, ord('~') - 96, False),
    KeyCode(45, 45, '-', False, ord('_') - 45, False),
    KeyCode(61, 61, '=', False, ord('+') - 61, False),
    KeyCode(44, 44, ',', False, ord('<') - 44, False),
    KeyCode(46, 46, '.', False, ord('>') - 46, False),
]

# Missing stuff
# PrintScreen
# ScrollLock
# Pause
# Ralt

for i in range(1, 14):
    _codes.append(KeyCode(281 + i, 111 + i, 'f{}'.format(i), True, 0, False))

for i in range(26):
    _codes.append(KeyCode(97 + i, 65 + i, chr(97 + i), False, -32, True))

_nums_shift = [')', '!', '@', '#', '$', '%', '^', '&', '*', '(']

for i in range(10):
    _codes.append(KeyCode(48 + i, 48 + i, str(i), False, (ord(_nums_shift[i]) - 48 - i), False))


_by_char = {
    character: (unix, windows, is_special, shift, capslock)
    for (unix, windows, character, is_special, shift, capslock) in _codes
}

_by_unix = {
    unix: (character, windows, is_special, shift, capslock)
    for (unix, windows, character, is_special, shift, capslock) in _codes
}

_by_windows = {
    windows: (character, unix, is_special, shift, capslock)
    for (unix, windows, character, is_special, shift, capslock) in _codes
}


def get_unix_keycode(character):
    return _by_char[character][0]


def get_windows_keycode(character):
    return _by_char[character][1]


def get_native_keycode(character):
    return get_unix_keycode(character)


def get_character_unix(unix, modifiers=None):
    if not modifiers:
        modifiers = []
    if unix not in _by_unix.keys():
        return chr(unix)
    spec = _by_unix[unix]
    character = spec[0]
    shift_applies = False
    offset = spec[3]
    if offset:
        capslock = spec[4]
        if not capslock:
            if 'shift' in modifiers:
                shift_applies = True
        else:
            if ('shift' in modifiers and not 'capslock' in modifiers)\
                    or ('capslock' in modifiers and not 'shift' in modifiers):
                shift_applies = True
    if shift_applies:
        if offset and len(character) == 1:
            character = chr(ord(character) + offset)
    return character


def get_character_windows(windows, modifiers=None):
    return _by_windows[windows][0]


def get_character_native(native, modifiers=None):
    return get_character_unix(native, modifiers)


def get_unix_from_windows(windows):
    return _by_windows[windows][1]


def get_windows_from_unix(unix):
    return _by_unix[unix][1]


def get_windows_from_native(native):
    return get_windows_from_unix(native)


def get_unix_from_native(native):
    return native


def check_is_special(native):
    if native not in _by_unix.keys():
        return False
    return _by_unix[native][2]


if __name__ == '__main__':
    for spec in _codes:
        print(spec)
