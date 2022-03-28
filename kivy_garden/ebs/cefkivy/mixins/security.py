

from ..browser import cefpython
from ..components.blockdialog import BlockDialog


class CertificateErrorDialog(BlockDialog):
    def __init__(self, **kwargs):
        kwargs.setdefault('title', "SSL Certificate Error")
        kwargs['message_text'] = "The website at {} presented an invalid certificate " \
                                 "and has been blocked.\n" \
                                 "Please use the back or home buttons to return to " \
                                 "where you were.\n" \
                                 "".format(kwargs['message_text'])
        super(CertificateErrorDialog, self).__init__(**kwargs)


class SecurityMixin(object):
    def __init__(self, ssl_verification_disabled=False):
        self.ssl_verification_disabled = ssl_verification_disabled
        # Bind callback to the OnCertificateError cefpython event
        cefpython.SetGlobalClientCallback("OnCertificateError", self.on_certificate_error)

    def on_certificate_error(self, cert_error, request_url, callback):
        # Check if cert verification is disabled
        if self.ssl_verification_disabled:
            callback.Continue(True)
        else:
            block_dialog = CertificateErrorDialog(browser=self.browser, callback=None,
                                                  message_text=request_url, autoclose=0)
            self.dialog_show(block_dialog)
            callback.Continue(False)
