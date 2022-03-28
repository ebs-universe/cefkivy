
from kivy_garden.ebs.cefkivy.handlers.base import ClientHandlerBase


class LifespanHandler(ClientHandlerBase):
    # https://github.com/cztomczak/cefpython/blob/master/api/LifespanHandler.md
    def OnBeforePopup(self, *args, **kwargs):
        result = self._widget.dispatch("on_before_popup", *args, **kwargs)
        return result
