from kivy.core.window import Window
from kivy.uix.vkeyboard import VKeyboard


class FixedKeyboard(VKeyboard):
    def __init__(self, **kwargs):
        super(FixedKeyboard, self).__init__(**kwargs)

    def setup_mode_free(self):
        """Overwrite free function to set fixed pos
        """
        self.do_rotation = False
        self.do_scale = False
        self.scale = 1.2
        target = self.target
        if not target:
            return
        self.center_x = Window.width/2
        self.y = 230


Window.set_vkeyboard_class(FixedKeyboard)
