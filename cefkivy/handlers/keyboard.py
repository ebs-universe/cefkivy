
from cefkivy.handlers.base import ClientHandlerBase


class KeyboardHandler(ClientHandlerBase):
    # https://github.com/cztomczak/cefpython/blob/master/api/KeyboardHandler.md
    def OnPreKeyEvent(self, browser, event, event_handle, is_keyboard_shortcut_out):
        return False

    def OnKeyEvent(self, browser, event, event_handle):
        return False
