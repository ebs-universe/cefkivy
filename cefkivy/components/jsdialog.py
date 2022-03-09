

from urllib.parse import urlparse
from .dialog import MessageDialogBase


class JSDialogBase(MessageDialogBase):
    def __init__(self, **kwargs):
        self._origin_url = kwargs.pop('origin_url')
        kwargs['title'] = "The website at {} says :".format(
            urlparse(self._origin_url).netloc
        )
        super(JSDialogBase, self).__init__(**kwargs)

    def cancel(self, *_):
        if self._when_done:
            self._when_done(self)
        self._callback.Continue(False, "")

    def ok(self, *_):
        if self._when_done:
            self._when_done(self)
        self._callback.Continue(True, "")


class JSDialogAlert(JSDialogBase):
    def __init__(self, **kwargs):
        kwargs.setdefault('button_specs', [
            ('OK', self.ok),
        ])
        super(JSDialogAlert, self).__init__(**kwargs)


class JSDialogConfirm(JSDialogBase):
    def __init__(self, **kwargs):
        kwargs.setdefault('button_specs', [
            ('OK', self.ok),
            ('Cancel', self.cancel)
        ])
        super(JSDialogConfirm, self).__init__(**kwargs)


class JSDialogPrompt(JSDialogBase):
    def __init__(self, default_prompt_text, **kwargs):
        kwargs.setdefault('button_specs', [
            ('OK', self.ok),
            ('Cancel', self.cancel)
        ])
        # TODO Add user_input support
        super(JSDialogPrompt, self).__init__(**kwargs)
        self._default_prompt_text = default_prompt_text

    def ok(self, user_input=""):
        if self._when_done:
            self._when_done(self)
        self._callback.Continue(True, user_input)
