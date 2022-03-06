
from cefkivy.handlers.base import ClientHandlerBase


class LifespanHandler(ClientHandlerBase):
    # https://github.com/cztomczak/cefpython/blob/master/api/LifespanHandler.md
    def OnBeforePopup(self, *args, **kwargs):
        self._widget.dispatch("on_before_popup", *args, **kwargs)
        return True