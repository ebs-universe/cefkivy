

from kivy.base import EventLoop
from kivy.logger import Logger
from kivy.properties import OptionProperty

from ..browser import cefpython
from ..inputs.keyboard import KeystrokeEventProcessor


class KeyboardMixin(object):
    # Keyboard mode: "global" or "local".
    # 1. Global mode forwards keys to CEF all the time.
    # 2. Local mode forwards keys to CEF only when an editable
    #    control is focused (input type=text|password or textarea).
    keyboard_mode = OptionProperty("global", options=("global", "local"))
    __keyboard = None

    def __init__(self, keyboard_mode='global'):
        self.keyboard_mode = keyboard_mode
        self.keystroke_processor = KeystrokeEventProcessor(
            cefpython=cefpython, browser_widget=self
        )
        Logger.debug("cefkivy: Starting the Keyboard Manager")
        self.bind(keyboard_mode=self.set_keyboard_mode)
        if self.keyboard_mode == "global":
            self.request_keyboard()

    def set_keyboard_mode(self, *_):
        if self.keyboard_mode == "global":
            self.request_keyboard()
        else:
            self.release_keyboard()

    def request_keyboard(self):
        if not self.__keyboard:
            self.__keyboard = EventLoop.window.request_keyboard(self.release_keyboard, self)
            self.__keyboard.bind(on_key_down=self.on_key_down)
            self.__keyboard.bind(on_key_up=self.on_key_up)
        self.keystroke_processor.reset_all_modifiers()
        # Not sure if it is still required to send the focus
        # (some earlier bug), but it shouldn't hurt to call it.
        self.browser.SendFocusEvent(True)

    def release_keyboard(self, *kwargs):
        # When using local keyboard mode, do all the request
        # and releases of the keyboard through js bindings,
        # otherwise some focus problems arise.
        self.keystroke_processor.reset_all_modifiers()
        if not self.__keyboard:
            return
        # If we blur the field on keyboard release, jumping between form
        # fields with tab won't work.
        # self.browser.GetFocusedFrame().ExecuteJavascript("__kivy__on_escape()")
        self.__keyboard.unbind(on_key_down=self.on_key_down)
        self.__keyboard.unbind(on_key_up=self.on_key_up)
        self.__keyboard.release()
        self.__keyboard = None

    # def keyboard_update(self, shown, rect, attributes):
    #     """
    #     :param shown: Show keyboard if true, hide if false (blur)
    #     :param rect: [x,y,width,height] of the input element
    #     :param attributes: Attributes of HTML element
    #     """
    #     if shown:
    #         # Check if keyboard should get displayed above
    #         above = False
    #         if 'class' in attributes:
    #             if attributes['class'] in self.keyboard_above_classes:
    #                 above = True
    #
    #         self.request_keyboard()
    #         kb = self.__keyboard.widget
    #         if len(rect) < 4:
    #             kb.pos = ((Window.width-kb.width*kb.scale)/2, 10)
    #         else:
    #             x = self.x+rect[0]+(rect[2]-kb.width*kb.scale)/2
    #             y = self.height+self.y-rect[1]-rect[3]-kb.height*kb.scale
    #             if above:
    #                 # If keyboard should displayed above the input field
    #                 # Above is good on e.g. search boxes with results displayed
    #                 # bellow the input field
    #                 y = self.height+self.y-rect[1]
    #             if y < 0:
    #                 # If keyboard is bellow the window height
    #                 rightx = self.x+rect[0]+rect[2]
    #                 spleft = self.x+rect[0]
    #                 spright = Window.width-rightx
    #                 y = 0
    #                 if spleft <= spright:
    #                     x = rightx
    #                 else:
    #                     x = spleft-kb.width*kb.scale
    #             elif y+kb.height*kb.scale > Window.height:
    #                 # If keyboard is above the window height
    #                 rightx = self.x+rect[0]+rect[2]
    #                 spleft = self.x+rect[0]
    #                 spright = Window.width-rightx
    #                 y = Window.height-kb.height*kb.scale
    #                 if spleft <= spright:
    #                     x = rightx
    #                 else:
    #                     x = spleft-kb.width*kb.scale
    #             else:
    #                 if x < 0:
    #                     x = 0
    #                 elif Window.width < x+kb.width*kb.scale:
    #                     x = Window.width-kb.width*kb.scale
    #             kb.pos = (x, y)
    #     else:
    #         self.release_keyboard()

    def on_key_down(self, *args):
        # print("Kivy Down Event : ", args)
        self.keystroke_processor.on_key_down(self.browser, *args)

    def on_key_up(self, *args):
        # print("Kivy Up Event : ", args)
        self.keystroke_processor.on_key_up(self.browser, *args)
