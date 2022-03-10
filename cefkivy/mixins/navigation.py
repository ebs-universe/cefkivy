

from kivy.properties import StringProperty
from kivy.properties import BooleanProperty


class NavigationMixin(object):
    url = StringProperty("about:blank")
    current_url = StringProperty("")
    is_loading = BooleanProperty(True)

    def __init__(self, start_url):
        self.url = start_url
        self.register_event_type("on_loading_state_change")
        self.register_event_type("on_address_change")
        self.register_event_type("on_title_change")
        self.register_event_type("on_load_start")
        self.register_event_type("on_load_end")
        self.register_event_type("on_load_error")

    def on_url(self, instance, value):
        if self.browser and value:
            self.browser.Navigate(self.url)
            # self._reset_js_bindings = True

    def go_back(self):
        self.browser.GoBack()

    def go_forward(self):
        self.browser.GoForward()

    def on_loading_state_change(self, isLoading, canGoBack, canGoForward):
        self.is_loading = isLoading

    def on_address_change(self, frame, url):
        self.current_url = url

    def on_title_change(self, new_title):
        pass

    def on_load_start(self, frame):
        pass

    def on_load_end(self, frame, httpStatusCode):
        pass

    def on_load_error(self, frame, errorCode, errorText, failedUrl):
        pass
