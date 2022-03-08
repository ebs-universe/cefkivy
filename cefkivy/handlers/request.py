from cefpython3 import cefpython
from kivy import Logger

from cefkivy.handlers.base import ClientHandlerBase


class RequestHandler(ClientHandlerBase):
    def GetAuthCredentials(self, *args, **kwargs):
        pass

    def GetCookieManager(self, browser, main_url):
        cookie_manager = cefpython.CookieManager.GetGlobalManager()
        if cookie_manager:
            return cookie_manager
        else:
            Logger.warn("No cookie manager found!")

    def GetResourceHandler(self, browser, frame, request):
        pass

    def OnBeforeBrowse(self, browser, frame, request, user_gesture, is_redirect):
        pass

    def OnBeforeResourceLoad(self, browser, frame, request):
        pass

    def OnQuotaRequest(self, *args, **kwargs):
        pass

    def OnResourceRedirect(self, *args, **kwargs):
        pass

    def OnProtocolExecution(self, browser, url, allow_execution_out):
        pass

    def OnRendererProcessTerminated(self, browser, status):
        pass
