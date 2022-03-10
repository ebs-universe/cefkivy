

from ..browser import cefpython


class SecurityMixin(object):
    def __init__(self, ssl_verification_disabled=False):
        self.ssl_verification_disabled = ssl_verification_disabled
        self.register_event_type("on_certificate_error")
        # Bind callback to the OnCertificateError cefpython event
        cefpython.SetGlobalClientCallback("OnCertificateError", self.on_certificate_error)

    def on_certificate_error(self, err, url, cb):
        print(err, url, cb)
        # Check if cert verification is disabled
        if self.ssl_verification_disabled:
            cb.Continue(True)
        else:
            cb.Continue(False)
            self.dispatch("on_certificate_error")
