

from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from kivy_garden.ebs.core.colors import ColorBoxLayout
from kivy_garden.ebs.core.labels import WrappingLabel


class MessageDialogBase(object):
    def __init__(self, browser, message_text, callback,
                 button_specs=None, user_input=False, when_done=None, title=None,
                 bgcolor=None, icon=None, fgcolor=None, autoclose=0):
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
        self._autoclose = autoclose
        self._finished = False

    def build(self, text_font_params):
        if self._autoclose:
            self._message_text = self._message_text + \
                                 "\nThis message will close in {} seconds.".format(self._autoclose)

            def _autoclose(*_):
                if not self._finished:
                    self.cancel()
            Clock.schedule_once(_autoclose, self._autoclose)

        dialog_widget = ColorBoxLayout(
            bgcolor=self._bgcolor, orientation='vertical',
            size_hint=(0.5, None), pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=[10],
        )

        if self._title:
            title = Label(text=self._title, color=self._fgcolor, **text_font_params)
            dialog_widget.add_widget(title)

        rich_layout = BoxLayout(orientation='horizontal', size_hint_y=None)
        if self._icon:
            pass

        uix_layout = BoxLayout(orientation='vertical', spacing=10, padding=[10], size_hint_y=None)
        label = WrappingLabel(text=self._message_text, color=self._fgcolor, size_hint=(1, None), **text_font_params)
        uix_layout.add_widget(label)

        if self._user_input:
            pass

        def _uix_resize(_, l_h):
            uix_layout.height = l_h + 20
        label.bind(height=_uix_resize)

        rich_layout.add_widget(uix_layout)

        def _rich_resize(_, u_h):
            rich_layout.height = u_h
        uix_layout.bind(height=_rich_resize)

        dialog_widget.add_widget(rich_layout)

        button_layout = BoxLayout(orientation='horizontal', spacing=10, height=35)
        for text, action in self._button_specs:
            lbutton = Button(text=text, **text_font_params)
            lbutton.bind(on_press=action)
            button_layout.add_widget(lbutton)

        dialog_widget.add_widget(button_layout)

        def _dialog_resize(_, r_h):
            dialog_widget.height = r_h + 35 + title.height + 20
        rich_layout.bind(height=_dialog_resize)
        self._finished = False
        return dialog_widget

    def skip(self):
        self.ok()

    def cancel(self, *_):
        self._finished = True
        if self._when_done:
            self._when_done(self)
        if self._callback:
            self._callback(False)

    def ok(self, *_):
        self._finished = True
        if self._when_done:
            self._when_done(self)
        if self._callback:
            self._callback(True)

    @property
    def when_done(self):
        return self._when_done

    @when_done.setter
    def when_done(self, value):
        self._when_done = value
