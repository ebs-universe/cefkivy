from cefpython3 import cefpython

from cefkivy.handlers.base import ClientHandlerBase


class RenderHandler(ClientHandlerBase):
    # https://github.com/cztomczak/cefpython/blob/master/api/RenderHandler.md
    def GetRootScreenRect(self, browser, rect_out):
        pass

    def GetViewRect(self, browser, rect_out):
        width, height = self._widget.texture.size
        rect_out.append(0)
        rect_out.append(0)
        rect_out.append(width)
        rect_out.append(height)
        return True

    def GetScreenRect(self, browser, rect_out):
        pass

    def GetScreenPoint(self, browser, view_x, view_y, screen_coordinates_out):
        pass

    def OnPopupShow(self, browser, show):
        self._widget.remove_widget(self._widget.popup)
        if show:
            self._widget.add_widget(self._widget.popup)

    def OnPopupSize(self, browser, rect_out):
        self._widget.popup.rpos = (rect_out[0], rect_out[1])
        self._widget.popup.size = (rect_out[2], rect_out[3])

    def OnPaint(self, browser, element_type, dirty_rects, paint_buffer, width, height):
        b = paint_buffer.GetString(mode="bgra", origin="top-left")

        if element_type != cefpython.PET_VIEW:
            popup = self._widget.popup
            if popup.texture.width * popup.texture.height * 4 != len(b):
                return  # prevent segfault
            popup.texture.blit_buffer(b, colorfmt='bgra', bufferfmt='ubyte')
            popup.update_rect()
            return

        if self._widget.texture.width * self._widget.texture.height * 4 != len(b):
            return  # prevent segfault
        self._widget.texture.blit_buffer(b, colorfmt='bgra', bufferfmt='ubyte')
        self._widget.update_rect()
        return

    def OnCursorChange(self, browser, cursor):
        pass

    def OnScrollOffsetChanged(self, browser):
        pass

    def OnTextSelectionChanged(self, browser, selected_text, selected_range):
        pass
