

from ..inputs.touch import TouchProcessor


class TouchMixin(object):
    def __init__(self):
        self._touch_processor = TouchProcessor(self, self.browser)

    def on_touch_down(self, touch, **kwargs):
        self._touch_processor.on_touch_down(touch, **kwargs)

    def on_touch_move(self, touch, **kwargs):
        self._touch_processor.on_touch_move(touch, **kwargs)

    def on_touch_up(self, touch, **kwargs):
        self._touch_processor.on_touch_up(touch, **kwargs)
