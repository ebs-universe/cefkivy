

import os
from kivy.base import EventLoop
from kivy.core.window import Window
from kivy.uix.vkeyboard import VKeyboard


class FixedKeyboard(VKeyboard):
    def __init__(self, **kwargs):
        super(FixedKeyboard, self).__init__(**kwargs)

    def setup_mode_free(self):
        """Overwrite free function to set fixed pos"""
        self.do_rotation = False
        self.do_scale = False
        self.scale = 1.2
        target = self.target
        if not target:
            return
        self.center_x = Window.width/2
        self.y = 230


Window.set_vkeyboard_class(FixedKeyboard)


class KeyboardManager(object):
    # Keyboard mode: "global" or "local".
    # 1. Global mode forwards keys to CEF all the time.
    # 2. Local mode forwards keys to CEF only when an editable
    #    control is focused (input type=text|password or textarea).
    __keyboard = None

    def __init__(self, widget, browser, keyboard_mode='local'):
        self._widget = widget
        self._browser = browser
        self._install()
        self.keyboard_mode = keyboard_mode

    def _install(self):
        self._widget.preinstall_js_binding('__kivy__keyboard_update', self.keyboard_update)
        with open(os.path.join(os.path.dirname(__file__), 'keyboard_trigger.js'), 'r') as f:
            js_code = f.read()
            self._widget.preinstall_js_code(js_code)

    @property
    def keyboard_mode(self):
        return self._keyboard_mode

    @keyboard_mode.setter
    def keyboard_mode(self, value):
        if value not in ('global', 'local'):
            raise ValueError("Invalid keyboard mode : {}".format(value))
        self._keyboard_mode = value
        if self._keyboard_mode == "global":
            self.request_keyboard()
        else:
            self.release_keyboard()

    def request_keyboard(self):
        if not self.__keyboard:
            print("Requesting Keyboard")
            self.__keyboard = EventLoop.window.request_keyboard(self.release_keyboard, self._widget)
            self.__keyboard.bind(on_key_down=self._widget.on_key_down)
            self.__keyboard.bind(on_key_up=self._widget.on_key_up)
        self._widget.keystroke_processor.reset_all_modifiers()
        # Not sure if it is still required to send the focus
        # (some earlier bug), but it shouldn't hurt to call it.
        self._browser.SendFocusEvent(True)

    def release_keyboard(self):
        # When using local keyboard mode, do all the request
        # and releases of the keyboard through js bindings,
        # otherwise some focus problems arise.
        self._widget.keystroke_processor.reset_all_modifiers()
        if not self.__keyboard:
            return
        # If we blur the field on keyboard release, jumping between form
        # fields with tab won't work.
        # self.browser.GetFocusedFrame().ExecuteJavascript("__kivy__on_escape()")
        self.__keyboard.unbind(on_key_down=self._widget.on_key_down)
        self.__keyboard.unbind(on_key_up=self._widget.on_key_up)
        print("Releasing Keyboard")
        self.__keyboard.release()
        self.__keyboard = None

    def keyboard_update(self, show, rect, attributes):
        """
        :param show: Show keyboard if true, hide if false (blur)
        :param rect: [x,y,width,height] of the input element
        :param attributes: Attributes of HTML element
        """
        if self.keyboard_mode == 'global':
            return
        if show:
            self.request_keyboard()
        else:
            self.release_keyboard()
