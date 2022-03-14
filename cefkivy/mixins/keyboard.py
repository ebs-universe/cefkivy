

from kivy.logger import Logger
from kivy.properties import OptionProperty

from ..browser import cefpython
from ..inputs.keyboard import KeystrokeEventProcessor
from ..components.keyboard import KeyboardManager


class KeyboardMixin(object):
    keyboard_mode = OptionProperty("global", options=("global", "local"))

    def __init__(self, **kwargs):
        Logger.debug("cefkivy: Starting the Keystroke Processor")
        self.keystroke_processor = KeystrokeEventProcessor(
            cefpython=cefpython, browser_widget=self
        )
        Logger.debug("cefkivy: Starting the Keyboard Manager")
        self.keyboard_manager = KeyboardManager(self, self.browser, **kwargs)

        def _propagate_mode(_, mode):
            self.keyboard_manager.keyboard_mode = mode
        self.bind(keyboard_mode=_propagate_mode)

    def on_key_down(self, *args):
        # print("Kivy Down Event : ", args)
        self.keystroke_processor.on_key_down(self.browser, *args)

    def on_key_up(self, *args):
        # print("Kivy Up Event : ", args)
        self.keystroke_processor.on_key_up(self.browser, *args)
