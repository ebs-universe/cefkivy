
from kivy_garden.ebs.cefkivy.handlers.base import ClientHandlerBase


class NavigationHandler(ClientHandlerBase):
    def OnAddressChange(self, browser, frame, url):
        self._widget.dispatch("on_address_change", frame, url)

    def OnTitleChange(self, browser, title):
        self._widget.dispatch("on_title_change", title)


class DisplayMessageHandler(ClientHandlerBase):
    def OnTooltip(self, browser, text_out):
        _ = text_out[0]
        # Let the browser deal with tooltips.
        return False

    def OnStatusMessage(self, browser, value):
        pass

    def OnConsoleMessage(self, browser, level, message, source, line):
        pass


class DisplayHandler(NavigationHandler,
                     DisplayMessageHandler):
    # https://github.com/cztomczak/cefpython/blob/master/api/DisplayHandler.md
    def __init__(self, browser_widget):
        NavigationHandler.__init__(self, browser_widget)
        DisplayMessageHandler.__init__(self, browser_widget)
