

if (__keyboard_trigger_injected === undefined){
    var __keyboard_trigger_injected = true;

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
    attributes = getAttributes(e.target);
    rect = e.target.getBoundingClientRect();
    if (isKeyboardElement(e.target)) {
        __kivy__keyboard_update(true, rect, attributes);
    }
    else {
        __kivy__keyboard_update(false, rect, attributes);
    }
}, true);

window.addEventListener("blur", function (e) {
    attributes = getAttributes(e.target)
    rect = e.target.getBoundingClientRect();
    __kivy__keyboard_update(false, rect, attributes);
}, true);


//function __kivy__on_escape() {
//    if (document.activeElement) {
//        document.activeElement.blur();
//    }
//}

}
