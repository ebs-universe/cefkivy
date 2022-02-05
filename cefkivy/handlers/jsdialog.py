
from cefkivy.handlers.base import ClientHandlerBase


class JavascriptDialogHandler(ClientHandlerBase):
    # https://github.com/cztomczak/cefpython/blob/master/api/JavascriptDialogHandler.md
    def OnJavascriptDialog(self, browser, origin_url, dialog_type,
                           message_text, default_prompt_text, callback,
                           suppress_message_out):
        # Let the browser deal with this for the moment
        suppress_message_out.append(False)
        return False

    def OnBeforeUnloadJavascriptDialog(self, browser, message_text, is_reload, callback):
        return False

    def OnResetJavascriptDialogState(self, browser):
        pass

    def OnJavascriptDialogClosed(self, browser):
        pass
