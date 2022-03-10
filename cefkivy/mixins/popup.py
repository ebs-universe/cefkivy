

from ..components.blockdialog import PopupBlockDialog


class PopupMixin(object):
    popup = None

    def __init__(self):
        self.register_event_type("on_before_popup")
        # Logger.debug("cefkivy: Instantiating Browser Popup")
        # self.popup = CefBrowserPopup(self)

    def on_before_popup(self, browser, frame, target_url, target_frame_name, target_disposition,
                        user_gesture, popup_features, window_info_out, client, browser_settings_out,
                        no_javascript_access_out):
        # TODO Implement popups here. Suppressed for now.
        print("Opening Popup : ", target_url, user_gesture, target_disposition)
        block_dialog = PopupBlockDialog(browser=self.browser, callback=None,
                                        message_text=target_url)
        self.dialog_show(block_dialog)
        return True


# class CefBrowserPopup(Widget):
#     rx = NumericProperty(0)
#     ry = NumericProperty(0)
#     rpos = ReferenceListProperty(rx, ry)
#
#     def __init__(self, parent, *args, **kwargs):
#         super(CefBrowserPopup, self).__init__()
#         self.browser_widget = parent
#         self.__rect = None
#         self.texture = Texture.create(size=self.size, colorfmt='rgba', bufferfmt='ubyte')
#         self.texture.flip_vertical()
#         with self.canvas:
#             Color(1, 1, 1)
#             self.__rect = Rectangle(pos=self.pos, size=self.size, texture=self.texture)
#         self.bind(rpos=self.realign)
#         self.bind(size=self.realign)
#         parent.bind(pos=self.realign)
#         parent.bind(size=self.realign)
#
#     def realign(self, *args):
#         self.x = self.rx+self.browser_widget.x
#         self.y = self.browser_widget.height-self.ry-self.height+self.browser_widget.y
#         ts = self.texture.size
#         ss = self.size
#         schg = (ts[0] != ss[0] or ts[1] != ss[1])
#         if schg:
#             self.texture = Texture.create(size=self.size, colorfmt='rgba', bufferfmt='ubyte')
#             self.texture.flip_vertical()
#         if self.__rect:
#             with self.canvas:
#                 Color(1, 1, 1)
#                 self.__rect.pos = self.pos
#                 if schg:
#                     self.__rect.size = self.size
#             if schg:
#                 self.update_rect()
#
#     def update_rect(self):
#         if self.__rect:
#             self.__rect.texture = self.texture



