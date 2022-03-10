

class DialogMixin(object):
    def __init__(self, dialog_target=None):
        self._dialog_target = dialog_target
        self._current_dialog = None

    @property
    def dialog_target(self):
        return self._dialog_target

    @dialog_target.setter
    def dialog_target(self, value):
        self._dialog_target = value

    def dialog_finish(self, dialog):
        self.dialog_target.remove_widget(self._current_dialog)
        self.disabled = False
        self.opacity = 1
        self._current_dialog = None

    def dialog_show(self, dialog):

        if not self.dialog_target:
            print("WARNING: Dialog Target not Specified. Auto Accepting!")
            dialog.skip()
            return

        if self._current_dialog:
            dialog.cancel()
            return

        self._current_dialog = dialog.build()
        dialog.when_done = self.dialog_finish
        self.opacity = 0.3
        self.disabled = True
        self.dialog_target.add_widget(self._current_dialog)
