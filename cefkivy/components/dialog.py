

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
# TODO Make the ebs dependency installable or just include the code directly
from ebs.iot.linuxnode.widgets.colors import ColorBoxLayout


class MessageDialogBase(object):
    def __init__(self, browser, message_text, callback,
                 button_specs=None, user_input=False, when_done=None, title=None,
                 bgcolor=None, icon=None, fgcolor=None):
        self._when_done = when_done
        self._browser = browser
        self._message_text = message_text
        self._callback = callback
        self._bgcolor = bgcolor or (0.8, 0.8, 0.8, 1)
        self._fgcolor = fgcolor or (0, 0, 0, 1)
        self._icon = icon
        self._button_specs = button_specs or []
        self._user_input = user_input
        self._title = title

    def build(self):
        dialog_widget = ColorBoxLayout(
            bgcolor=self._bgcolor, orientation='vertical',
            size_hint=(0.5, None), pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=[10],
        )

        if self._title:
            title = Label(text=self._title, color=self._fgcolor)
            dialog_widget.add_widget(title)

        rich_layout = BoxLayout(orientation='horizontal')
        if self._icon:
            pass

        uix_layout = BoxLayout(orientation='vertical', spacing=10, padding=[10])
        label = Label(text=self._message_text, color=self._fgcolor)
        uix_layout.add_widget(label)
        if self._user_input:
            pass

        rich_layout.add_widget(uix_layout)
        dialog_widget.add_widget(rich_layout)

        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        for text, action in self._button_specs:
            lbutton = Button(text=text)
            lbutton.bind(on_press=action)
            button_layout.add_widget(lbutton)

        dialog_widget.add_widget(button_layout)

        return dialog_widget

    def skip(self):
        self.ok()

    def cancel(self, *_):
        if self._when_done:
            self._when_done(self)
        self._callback(False)

    def ok(self, *_):
        if self._when_done:
            self._when_done(self)
        self._callback(True)

    @property
    def when_done(self):
        return self._when_done

    @when_done.setter
    def when_done(self, value):
        self._when_done = value
