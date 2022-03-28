
from kivy_garden.ebs.cefkivy.handlers.base import ClientHandlerBase


class LoadHandler(ClientHandlerBase):
    # https://github.com/cztomczak/cefpython/blob/master/api/LoadHandler.md
    def OnLoadingStateChange(self, browser, is_loading, can_go_back, can_go_forward):
        self._widget.dispatch("on_loading_state_change", is_loading, can_go_back, can_go_forward)
        if self._widget.reset_js_bindings and not is_loading:
            self._widget.set_js_bindings()
        if is_loading and self._widget.keyboard_mode == "local":
            # Release keyboard when navigating to a new page.
            self._widget.release_keyboard()

    def OnLoadStart(self, browser, frame):
        self._widget.dispatch("on_load_start", frame)

    def OnLoadEnd(self, browser, frame, http_code):
        self._widget.dispatch("on_load_end", frame, http_code)

    def OnLoadError(self, browser, frame, error_code, error_text_out, failed_url):
        self._widget.dispatch("on_load_error", frame, error_code, error_text_out, failed_url)
