from kivy.uix.widget import Widget
from cefpython3.cefpython_py37 import PyBrowser
from ..browser import cefpython


class KivyTouchProcessor(object):
    def __init__(self, widget: Widget = None, **kwargs):
        if not widget:
            raise AttributeError("Widget is a required argument")
        self._touches = []
        self._widget = widget
        self._mouse_scroll_step = 40
        self._enable_dragging = kwargs.pop('enable_dragging', False)
        self._enable_right_click = kwargs.pop('enable_right_click', False)
        self._debug_touch = kwargs.pop('debug_touch', False)

    def _print_current_touches(self):
        print("Current Touches :")
        keys = ['button    ', 'is_dragging', 'is_scrolling', 'multitouch_sim', 'is_right_click', 'is_mouse_scrolling', 'is_double_tap']
        fstring = "  "
        ctitles = []
        for key in keys:
            if key.startswith('is_'):
                ctitle = key.replace('is_', "", 1)
            else:
                ctitle = key
            fstring += "{{:{}}}|".format(len(ctitle))
            ctitles.append(ctitle)

        print(fstring.format(*ctitles))
        for touch in self._touches:
            _spec = []
            for k in keys:
                if hasattr(touch, k.strip()):
                    _spec.append(getattr(touch, k.strip()))
                else:
                    _spec.append('-')
            print(fstring.format(*_spec))

    def _print_touch_event(self, touch, t):
        print(t, touch.button, touch.pos)
        for is_attr in []:
            try:
                print("  {:>15} : {}".format(is_attr, getattr(touch, "is_{}".format(is_attr))))
            except AttributeError:
                pass
        self._print_current_touches()
        print('----------------')

    def _translate_to_widget(self, x, y):
        # Widget coordinates === Browser coordinates
        y = self._widget.height - y + self._widget.pos[1]
        x = x - self._widget.pos[0]
        return x, y

    def _reset_touch_modifiers(self, touch):
        touch.is_dragging = False
        touch.is_scrolling = False
        touch.is_right_click = False

    def _prefilter_touch_start(self, touch):
        if self._widget.disabled:
            return True
        if not self._widget.collide_point(*touch.pos):
            return True
        if not self._enable_right_click and touch.button == 'right':
            return True

    def _prefilter_touch_continuation(self, touch):
        if touch.grab_current is not self._widget:
            return True

    def _accept_touch_start(self, touch):
        self._touches.append(touch)
        touch.grab(self._widget)

    def _touch_finish(self, touch):
        self._touches.remove(touch)
        touch.ungrab(self._widget)

    def on_touch_down(self, touch, **kwargs):
        if self._debug_touch:
            self._print_touch_event(touch, 'DOWN')
        if self._prefilter_touch_start(touch):
            return
        self._reset_touch_modifiers(touch)
        self._accept_touch_start(touch)
        return True

    def _process_touch_scroll(self, touch):
        # Scroll only if a given distance is passed once (could be right click)
        dx = sum([t.dx / len(self._touches) for t in self._touches])
        dy = sum([t.dy / len(self._touches) for t in self._touches])
        if (abs(dx) > 5 or abs(dy) > 5) or touch.is_scrolling:
            touch.is_scrolling = True
            self._dispatch_scroll_event(touch.x, self._widget.height - touch.pos[1], dx, -dy)

    def _process_touch_drag(self, touch, x, y):
        if (abs(touch.dx) > 5 or abs(touch.dy) > 5) or touch.is_dragging:
            if touch.is_dragging:
                self._dispatch_drag_move_event(x, y)
            else:
                self._dispatch_drag_start_event(x, y)
                touch.is_dragging = True

    def on_touch_move(self, touch, **kwargs):
        if self._debug_touch:
            self._print_touch_event(touch, 'MOVE')
        if self._prefilter_touch_continuation(touch):
            return
        x, y = self._translate_to_widget(touch.x, touch.y)

        if len(self._touches) == 1:
            if self._enable_dragging:
                self._process_touch_drag(touch, x, y)
            else:
                self._process_touch_scroll(touch)
        elif len(self._touches) == 2:
            self._process_touch_scroll(touch)
        return True

    def on_touch_up(self, touch, **kwargs):
        if self._debug_touch:
            self._print_touch_event(touch, 'UP')
        if self._prefilter_touch_continuation(touch):
            return
        x, y = self._translate_to_widget(touch.x, touch.y)

        if len(self._touches) == 2:
            if not touch.is_scrolling:
                self._touches[0].is_right_click = self._touches[1].is_right_click = True
                self._dispatch_right_click_event(x, y)
        else:
            if touch.is_scrolling:
                pass
            elif touch.is_dragging:
                self._dispatch_drag_end_event(x, y)
            elif touch.is_mouse_scrolling:
                if touch.button == 'scrolldown':
                    dy = +1
                elif touch.button == 'scrollup':
                    dy = -1
                else:
                    raise ValueError("Got mouse_scrolling with button {}".format(touch.button))
                self._dispatch_scroll_event(x, y, 0, dy * self._mouse_scroll_step)
            elif not touch.is_right_click:
                if touch.is_double_tap:
                    self._dispatch_double_click_event(x, y)
                else:
                    self._dispatch_single_click_event(x, y)
            elif touch.is_right_click or touch.button == 'right':
                self._dispatch_right_click_event(x, y)
        self._touch_finish(touch)
        return True

    def _dispatch_click_event(self, x, y, count):
        raise NotImplementedError

    def _dispatch_single_click_event(self, x, y):
        self._dispatch_click_event(x, y, 1)

    def _dispatch_double_click_event(self, x, y):
        self._dispatch_click_event(x, y, 2)

    def _dispatch_scroll_event(self, x, y, dx, dy):
        raise NotImplementedError

    def _dispatch_drag_start_event(self, x, y):
        raise NotImplementedError

    def _dispatch_drag_move_event(self, x, y):
        raise NotImplementedError

    def _dispatch_drag_end_event(self, x, y):
        raise NotImplementedError

    def _dispatch_right_click_event(self, x, y):
        raise NotImplementedError


class CefTouchProcessor(KivyTouchProcessor):
    def __init__(self, browser: PyBrowser = None, **kwargs):
        if not browser:
            raise AttributeError("Browser is a required argument")
        super(CefTouchProcessor, self).__init__(**kwargs)
        self._browser = browser

    def _dispatch_click_event(self, x, y, count):
        # Left Mouse Down, Left Mouse Up
        self._browser.SendMouseClickEvent(
            x, y, cefpython.MOUSEBUTTON_LEFT,
            mouseUp=False, clickCount=count
        )
        self._browser.SendMouseClickEvent(
            x, y, cefpython.MOUSEBUTTON_LEFT,
            mouseUp=True, clickCount=count
        )

    def _dispatch_scroll_event(self, x, y, dx, dy):
        self._browser.SendMouseWheelEvent(x, y, dx, dy)

    def _dispatch_drag_start_event(self, x, y):
        self._browser.SendMouseClickEvent(x, y, cefpython.MOUSEBUTTON_LEFT,
                                          mouseUp=False, clickCount=1)

    def _dispatch_drag_move_event(self, x, y):
        self._browser.SendMouseMoveEvent(x, y, mouseLeave=False)

    def _dispatch_drag_end_event(self, x, y):
        # Drag end (mouse up)
        self._browser.SendMouseClickEvent(
            x, y, cefpython.MOUSEBUTTON_LEFT,
            mouseUp=True, clickCount=1
        )

    def _dispatch_right_click_event(self, x, y):
        # Right click (mouse down, mouse up)
        self._browser.SendMouseClickEvent(
            x, y, cefpython.MOUSEBUTTON_RIGHT,
            mouseUp=False, clickCount=1
        )
        self._browser.SendMouseClickEvent(
            x, y, cefpython.MOUSEBUTTON_RIGHT,
            mouseUp=True, clickCount=1
        )
