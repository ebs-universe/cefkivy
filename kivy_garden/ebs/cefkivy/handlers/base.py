

from twisted import logger


class ClientHandlerBase(object):
    def __init__(self, browser_widget):
        self._log = None
        self._widget = browser_widget

    @property
    def log(self):
        if not self._log:
            self._log = logger.Logger(namespace="cefkivy.handlers.{0}"
                                                "".format(self.__class__.__name__), source=self)
        return self._log
