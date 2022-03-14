import cefpython3.cefpython_py37

from . import keycodes


class KeystrokeEventProcessor(object):
    def __init__(self, cefpython, browser_widget, *args, **kwargs):
        self.cefpython = cefpython
        self.browser_widget = browser_widget
        self._use_textinput = kwargs.pop('use_textinput', True)
        # Kivy does not provide modifiers in on_key_up, but these
        # must be sent to CEF as well.
        self.is_lshift = False
        self.is_rshift = False
        self.is_lctrl = False
        self.is_rctrl = False
        self.is_lalt = False
        self.is_ralt = False
        self.is_altgr = False

    def reset_all_modifiers(self):
        self.is_lshift = False
        self.is_lctrl = False
        self.is_lalt = False
        self.is_rshift = False
        self.is_rctrl = False
        self.is_ralt = False
        self.is_altgr = False

    def on_key_down(self, browser, keyboard, keycode, text, modifiers):
        # print("\non_key_down:", keycode, text, modifiers)
        if keycodes.get_character_native(keycode[0]) == 'escape':
            # On escape release the keyboard
            self.browser_widget.release_keyboard()
            return

        cef_modifiers = self.cefpython.EVENTFLAG_NONE
        if "shift" in modifiers:
            cef_modifiers |= self.cefpython.EVENTFLAG_SHIFT_DOWN
        if "ctrl" in modifiers:
            cef_modifiers |= self.cefpython.EVENTFLAG_CONTROL_DOWN
        if "alt" in modifiers:
            cef_modifiers |= self.cefpython.EVENTFLAG_ALT_DOWN
        if "capslock" in modifiers:
            cef_modifiers |= self.cefpython.EVENTFLAG_CAPS_LOCK_ON

        try:
            native_key_code = keycodes.get_unix_from_native(keycode[0])
            windows_key_code = keycodes.get_windows_from_native(keycode[0])
            character = keycodes.get_character_native(keycode[0],
                                                      modifiers=modifiers)
            unmodified_character = keycodes.get_character_native(keycode[0])
        except KeyError:
            native_key_code = keycode[0]
            windows_key_code = keycode[0]
            character = keycode[1]
            unmodified_character = keycode[1]

        # Only send KEYEVENT_KEYDOWN if it is a special key (tab, return ...)
        # Eh? Convert every other key to it's utf8 int value and send this as the key
        if keycodes.check_is_special(native_key_code):
            event_type = self.cefpython.KEYEVENT_KEYDOWN
            character = ''
            unmodified_character = ''
        else:
            # # cef_key_code = ord(text)
            # # We have to convert the apostrophes as the utf8 key-code somehow don't get recognized by cef
            # if cef_key_code == 96:
            #     cef_key_code = 39
            # if cef_key_code == 8220:
            #     cef_key_code = 34
            event_type = self.cefpython.KEYEVENT_CHAR

        # When the key is the return key, send it as a KEYEVENT_CHAR as it will not work in textinputs
        # TODO This thing doesnt work
        # if keycodes.get_character_native(native_key_code) == "enter":
        #     event_type = self.cefpython.KEYEVENT_CHAR

        key_event = {
            "type": event_type,
            "native_key_code": native_key_code,
            "modifiers": cef_modifiers,
            "is_system_key": False,
            "windows_key_code": windows_key_code,
        }

        if character and len(character) == 1:
            key_event.update({
                "character": ord(character),
                "unmodified_character": ord(unmodified_character),
            })

        if self._use_textinput and key_event['type'] == self.cefpython.KEYEVENT_CHAR:
            pass
        else:
            # print("keydown keyEvent: %s" % key_event)
            browser.SendKeyEvent(key_event)

        if keycodes.get_character_native(native_key_code) == 'lshift':
            self.is_lshift = True
        if keycodes.get_character_native(native_key_code) == 'rshift':
            self.is_rshift = True
        if keycodes.get_character_native(native_key_code) == 'lctrl':
            self.is_lctrl = True
        if keycodes.get_character_native(native_key_code) == 'rctrl':
            self.is_rctrl = True
        if keycodes.get_character_native(native_key_code) == 'lalt':
            self.is_lalt = True
        if keycodes.get_character_native(native_key_code) == 'ralt':
            self.is_ralt = True
        if keycodes.get_character_native(native_key_code) == 'alt-gr':
            self.is_altgr = True

    def on_key_up(self, browser, keyboard, keycode):
        # if self._use_textinput:
        #     return
        # print("keyup keyEvent %s" % (keycode,))
        cef_modifiers = self.cefpython.EVENTFLAG_NONE
        if self.is_lshift or self.is_rshift:
            cef_modifiers |= self.cefpython.EVENTFLAG_SHIFT_DOWN
        if self.is_lctrl or self.is_rctrl:
            cef_modifiers |= self.cefpython.EVENTFLAG_CONTROL_DOWN
        if self.is_lalt or self.is_ralt or self.is_altgr:
            cef_modifiers |= self.cefpython.EVENTFLAG_ALT_DOWN

        try:
            native_key_code = keycodes.get_unix_from_native(keycode[0])
            windows_key_code = keycodes.get_windows_from_native(keycode[0])
        except KeyError:
            native_key_code = keycode[0]
            windows_key_code = keycode[0]

        if keycodes.check_is_special(native_key_code):
            key_event = {
                "type": self.cefpython.KEYEVENT_KEYUP,
                "native_key_code": native_key_code,
                "modifiers": cef_modifiers,
                "is_system_key": False,
                "windows_key_code": windows_key_code,
            }
            browser.SendKeyEvent(key_event)

        if keycodes.get_character_native(native_key_code) == 'lshift':
            self.is_lshift = False
        if keycodes.get_character_native(native_key_code) == 'rshift':
            self.is_rshift = False
        if keycodes.get_character_native(native_key_code) == 'lctrl':
            self.is_lctrl = False
        if keycodes.get_character_native(native_key_code) == 'rctrl':
            self.is_rctrl = False
        if keycodes.get_character_native(native_key_code) == 'lalt':
            self.is_lalt = False
        if keycodes.get_character_native(native_key_code) == 'ralt':
            self.is_ralt = False
        if keycodes.get_character_native(native_key_code) == 'alt-gr':
            self.is_altgr = False

    def on_textinput(self, browser, keyboard, character):
        key_event = {
            "type": cefpython3.cefpython_py37.KEYEVENT_CHAR,
            "character": ord(character),
            # "native_key_code": native_key_code,
            # "modifiers": cef_modifiers,
            # "is_system_key": False,
            # "windows_key_code": windows_key_code,
        }
        browser.SendKeyEvent(key_event)
