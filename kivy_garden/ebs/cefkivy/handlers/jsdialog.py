

from kivy_garden.ebs.cefkivy.handlers.base import ClientHandlerBase
from ..components import jsdialog

from kivy_garden.ebs.cefkivy.browser import cefpython


class JavascriptDialogHandler(ClientHandlerBase):
    # https://github.com/cztomczak/cefpython/blob/master/api/JavascriptDialogHandler.md
    def OnJavascriptDialog(self, browser, origin_url, dialog_type,
                           message_text, default_prompt_text, callback,
                           suppress_message_out):
        kwargs = {
            'browser': browser,
            'origin_url': origin_url,
            'message_text': message_text,
            'callback': callback
        }
        dialog = None
        if dialog_type == cefpython.JSDIALOGTYPE_ALERT:
            dialog = jsdialog.JSDialogAlert(**kwargs)
        elif dialog_type == cefpython.JSDIALOGTYPE_CONFIRM:
            dialog = jsdialog.JSDialogConfirm(**kwargs)
        elif dialog_type == cefpython.JSDIALOGTYPE_PROMPT:
            kwargs['default_prompt_text'] = default_prompt_text
            dialog = jsdialog.JSDialogPrompt(**kwargs)
        if dialog:
            self._widget.dialog_show(dialog)
        suppress_message_out.append(True)
        return True

    def OnBeforeUnloadJavascriptDialog(self, browser, message_text, is_reload, callback):
        return False

    def OnResetJavascriptDialogState(self, browser):
        pass

    def OnJavascriptDialogClosed(self, browser):
        pass
