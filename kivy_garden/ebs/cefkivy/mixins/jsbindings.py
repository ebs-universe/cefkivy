

from ..browser import cefpython


class JSBindingsMixin(object):
    def __init__(self):
        self._reset_js_bindings = False
        self._current_js_bindings = None
        self._js_bindings = [('test_binding', self._test_binding)]
        self._js_codes = []

    @property
    def reset_js_bindings(self):
        return self._reset_js_bindings

    @property
    def js_bindings(self):
        return self._js_bindings

    def preinstall_js_binding(self, name, target):
        self._js_bindings.append((name, target))

    def preinstall_js_code(self, code):
        self._js_codes.append(code)

    def _test_binding(self, *args, **kwargs):
        print("BINDING", args, kwargs)

    def set_js_bindings(self):
        # Needed to introduce set_js_bindings again because the freeze of sites at load took over.
        # As an example 'http://www.htmlbasix.com/popup.shtml' freezed every time. By setting the js
        # bindings again, the freeze rate is at about 35%. Check git to see how it was done, before using
        # this function ...
        # I (jegger) have to be honest, that I don't have a clue why this is acting like it does!
        # I hope simon (REN-840) can resolve this once in for all...
        #
        # ORIGINAL COMMENT:
        # When browser.Navigate() is called, some bug appears in CEF
        # that makes CefRenderProcessHandler::OnBrowserDestroyed()
        # is being called. This destroys the javascript bindings in
        # the Render process. We have to make the js bindings again,
        # after the call to Navigate() when OnLoadingStateChange()
        # is called with isLoading=False. Problem reported here:
        # http://www.magpcss.org/ceforum/viewtopic.php?f=6&t=11009
        if not self._current_js_bindings:
            self._current_js_bindings = cefpython.JavascriptBindings(bindToFrames=True, bindToPopups=True)
            for name, target in self.js_bindings:
                self._current_js_bindings.SetFunction(name, target)
        self.browser.SetJavascriptBindings(self._current_js_bindings)

    def inject_js_code(self, browser, is_loading, can_go_back, can_go_forward):
        frame = browser.browser.GetMainFrame()
        for code in self._js_codes:
            frame.ExecuteJavascript(code)
