

from kivy_garden.ebs.cefkivy.components.dialog import MessageDialogBase


class BlockDialog(MessageDialogBase):
    def __init__(self, **kwargs):
        kwargs.setdefault('button_specs', [
            ('OK', self.ok),
        ])
        kwargs.setdefault('autoclose', 8)
        super(BlockDialog, self).__init__(**kwargs)


class PopupBlockDialog(BlockDialog):
    def __init__(self, **kwargs):
        kwargs.setdefault('title', "Popup Blocked")
        kwargs['message_text'] = "The website attempted to open a popup to {} which was blocked." \
                                 "".format(kwargs['message_text'])
        super(PopupBlockDialog, self).__init__(**kwargs)
