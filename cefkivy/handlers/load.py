
from cefkivy.handlers.base import ClientHandlerBase


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
        if self._widget.keyboard_mode == "local":
            lrectconstruct = "var rect = e.target.getBoundingClientRect();var lrect = [rect.left, rect.top, rect.width, rect.height];"
            if frame.GetParent():
                lrectconstruct = "var lrect = [];"
            jsCode = """
window.print=function(){console.log("Print dialog blocked")}
function isKeyboardElement(elem) {
    var tag = elem.tagName.toUpperCase();
    if (tag=="INPUT") return (["TEXT", "PASSWORD", "DATE", "DATETIME", "DATETIME-LOCAL", "EMAIL", "MONTH", "NUMBER", "SEARCH", "TEL", "TIME", "URL", "WEEK"].indexOf(elem.type.toUpperCase())!=-1);
    else if (tag=="TEXTAREA") return true;
    else {
        var tmp = elem;
        while (tmp && tmp.contentEditable=="inherit") {
            tmp = tmp.parentElement;
        }
        if (tmp && tmp.contentEditable) return true;
    }
    return false;
}

function getAttributes(elem){
    var attributes = {}
    for (var att, i = 0, atts = elem.attributes, n = atts.length; i < n; i++){
        att = atts[i];
        attributes[att.nodeName] = att.nodeValue
    }
    return attributes
}

window.addEventListener("focus", function (e) {
    """ + lrectconstruct + """
    attributes = getAttributes(e.target)
    if (isKeyboardElement(e.target)) __kivy__keyboard_update(true, lrect, attributes);
}, true);

window.addEventListener("blur", function (e) {
    """ + lrectconstruct + """
    attributes = getAttributes(e.target)
    __kivy__keyboard_update(false, lrect, attributes);
}, true);

function __kivy__on_escape() {
    if (document.activeElement) {
        document.activeElement.blur();
    }
}
            """
            frame.ExecuteJavascript(jsCode)

    def OnLoadEnd(self, browser, frame, http_code):
        self._widget.dispatch("on_load_end", frame, http_code)
        # largs[0].SetZoomLevel(2.0) # this works at this point

    def OnLoadError(self, browser, frame, error_code, error_text_out, failed_url):
        self._widget.dispatch("on_load_error", frame, error_code, error_text_out, failed_url)
