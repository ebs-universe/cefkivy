

from kivy.core.window import Window
from ..browser import cefpython


class TouchMixin(object):
    def __init__(self):
        self.touches = []

    def on_touch_down(self, touch, *kwargs):
        if self.disabled:
            return
        if not self.collide_point(*touch.pos):
            return
        if self.keyboard_mode == "global":
            self.request_keyboard()
        else:
            Window.release_all_keyboards()

        touch.is_dragging = False
        touch.is_scrolling = False
        touch.is_right_click = False
        self.touches.append(touch)
        touch.grab(self)

        return True

    def on_touch_move(self, touch, *kwargs):
        if touch.grab_current is not self:
            return

        y = self.height-touch.pos[1] + self.pos[1]
        x = touch.x - self.pos[0]

        if len(self.touches) == 1:
            # Dragging
            if (abs(touch.dx) > 5 or abs(touch.dy) > 5) or touch.is_dragging:
                if touch.is_dragging:
                    self.browser.SendMouseMoveEvent(x, y, mouseLeave=False)
                else:
                    self.browser.SendMouseClickEvent(x, y, cefpython.MOUSEBUTTON_LEFT,
                                                     mouseUp=False, clickCount=1)
                    touch.is_dragging = True
        elif len(self.touches) == 2:
            # Scroll only if a given distance is passed once (could be right click)
            touch1, touch2 = self.touches[:2]
            dx = touch2.dx / 2. + touch1.dx / 2.
            dy = touch2.dy / 2. + touch1.dy / 2.
            if (abs(dx) > 5 or abs(dy) > 5) or touch.is_scrolling:
                # Scrolling
                touch.is_scrolling = True
                self.browser.SendMouseWheelEvent(touch.x, self.height-touch.pos[1], dx, -dy)
        return True

    def on_touch_up(self, touch, *kwargs):
        if touch.grab_current is not self:
            return

        y = self.height-touch.pos[1] + self.pos[1]
        x = touch.x - self.pos[0]

        if len(self.touches) == 2:
            if not touch.is_scrolling:
                # Right click (mouse down, mouse up)
                self.touches[0].is_right_click = self.touches[1].is_right_click = True
                self.browser.SendMouseClickEvent(
                    x, y, cefpython.MOUSEBUTTON_RIGHT,
                    mouseUp=False, clickCount=1
                )
                self.browser.SendMouseClickEvent(
                    x, y, cefpython.MOUSEBUTTON_RIGHT,
                    mouseUp=True, clickCount=1
                )
        else:
            if touch.is_dragging:
                # Drag end (mouse up)
                self.browser.SendMouseClickEvent(
                    x, y, cefpython.MOUSEBUTTON_LEFT,
                    mouseUp=True, clickCount=1
                )
            elif not touch.is_right_click:
                # Left click (mouse down, mouse up)
                count = 1
                if touch.is_double_tap:
                    count = 2
                self.browser.SendMouseClickEvent(
                    x, y, cefpython.MOUSEBUTTON_LEFT,
                    mouseUp=False, clickCount=count
                )
                self.browser.SendMouseClickEvent(
                    x, y, cefpython.MOUSEBUTTON_LEFT,
                    mouseUp=True, clickCount=count
                )

        self.touches.remove(touch)
        touch.ungrab(self)
        return True
