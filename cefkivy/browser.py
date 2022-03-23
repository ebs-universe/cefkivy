# Import cef as first module! (it's important)

import ctypes
import sys
import os
import platform

libcef_so = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libcef.so')
if os.path.exists(libcef_so):
    # Import local module
    ctypes.CDLL(libcef_so, ctypes.RTLD_GLOBAL)
    if 0x02070000 <= sys.hexversion < 0x03000000:
        import cefpython_py27 as cefpython
    else:
        raise Exception("Unsupported python version: %s" % sys.version)
else:
    # Import from package
    from cefpython3 import cefpython

from kivy.app import App

from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.logger import Logger

from .mixins.keyboard import KeyboardMixin
from .mixins.touch import TouchMixin
from .mixins.navigation import NavigationMixin
from .mixins.cookies import CookieManagerMixin
from .mixins.security import SecurityMixin
from .mixins.dialogs import DialogMixin
from .mixins.popup import PopupMixin
from .mixins.jsbindings import JSBindingsMixin

from .handlers.display import DisplayHandler
from .handlers.download import DownloadHandler
from .handlers.jsdialog import JavascriptDialogHandler
from .handlers.keyboard import KeyboardHandler
from .handlers.lifespan import LifespanHandler
from .handlers.load import LoadHandler
from .handlers.render import RenderHandler
from .handlers.request import RequestHandler


class CefBrowser(PopupMixin,
                 DialogMixin,
                 TouchMixin,
                 KeyboardMixin,
                 JSBindingsMixin,
                 CookieManagerMixin,
                 SecurityMixin,
                 NavigationMixin,
                 Widget):
    browser = None

    # Subclass CefBrowser and override this list to implement custom
    # event handlers and behaviors. In general, when you subclass one of these,
    # call the parent handler before or after you have done whatever you need to
    # do. This will be required to correctly fire kivy events for the few event
    # types which are defined in the various Mixins. If you're developing a custom
    # embedded browser and aren't using the kivy events yourself, then you can
    # safely ignore them - most aren't used internally. Just ensure that any code
    # present in the built-in handlers is accounted for in terms of the
    # functionality it provides.
    _handlers = [
        DisplayHandler,
        DownloadHandler,
        JavascriptDialogHandler,
        KeyboardHandler,
        LifespanHandler,
        LoadHandler,
        RenderHandler,
        RequestHandler,
    ]

    def __init__(self, **kwargs):
        switches = kwargs.pop("switches", {'remote-debugging-port': '9222'})

        self.__rect = None
        self.browser = None
        start_url = kwargs.pop('start_url', 'about:blank')
        dialog_target = kwargs.pop('dialog_target', None)
        keyboard_mode = kwargs.pop('keyboard_mode', 'local')
        resources_dir = kwargs.pop("resources_dir", "")
        ssl_verification_disabled = kwargs.pop("ssl_verification_disabled", False)
        Widget.__init__(self, **kwargs)

        self.check_versions()

        # Create the base texture
        self.texture = Texture.create(size=self.size, colorfmt='rgba', bufferfmt='ubyte')
        self.texture.flip_vertical()
        with self.canvas:
            Color(1, 1, 1)
            self.__rect = Rectangle(pos=self.pos, size=self.size, texture=self.texture)

        def cef_loop(*_):
            cefpython.MessageLoopWork()
        Clock.schedule_interval(cef_loop, 0)

        settings = {
            # "debug": True,
            "log_severity": cefpython.LOGSEVERITY_WARNING,
            # "log_file": "debug.log",
            "persist_session_cookies": True,
            # "release_dcheck_enabled": True,  # Enable only when debugging.
            "locales_dir_path": os.path.join(cefpython.GetModuleDirectory(), "locales"),
            "browser_subprocess_path": "%s/%s" % (cefpython.GetModuleDirectory(), "subprocess"),
            'background_color': 0xFFFFFFFF,
        }

        Logger.debug("cefkivy: Intializing cefpython with \n"
                     "   settings : %s \n"
                     "   switches : %s", settings, switches)
        cefpython.Initialize(settings, switches)

        # Disable Windowed rendering and and bind to parent window 0
        # TODO Set a proper parent?
        # See https://github.com/cztomczak/cefpython/blob/master/api/WindowInfo.md#setasoffscreen
        windowInfo = cefpython.WindowInfo()
        windowInfo.SetAsOffscreen(0)

        SecurityMixin.__init__(self, ssl_verification_disabled)
        NavigationMixin.__init__(self, start_url)

        # Create the Synchronous Browser
        Logger.debug("cefkivy: Creating the Browser")
        self.browser = cefpython.CreateBrowserSync(windowInfo, {}, navigateUrl=self.url)

        CookieManagerMixin.__init__(self, resources_dir)

        self.browser.SendFocusEvent(True)

        Logger.debug("cefkivy: Installing Client Handlers")
        for handler in self._handlers:
            self.install_handler(handler)

        Logger.debug("cefkivy: Binding the Browser Size and Resizing")
        self.browser.WasResized()
        self.bind(size=self.realign)
        self.bind(pos=self.realign)

        JSBindingsMixin.__init__(self)
        KeyboardMixin.__init__(self, keyboard_mode=keyboard_mode)
        TouchMixin.__init__(self)
        DialogMixin.__init__(self, dialog_target)
        PopupMixin.__init__(self)

        Logger.debug("cefkivy: Setting JS Bindings")
        self.set_js_bindings()

        Logger.debug("cefkivy: Injecting JS Code")
        self.bind(on_loading_state_change=self.inject_js_code)

    def check_versions(self):
        md = cefpython.GetModuleDirectory()
        Logger.debug("cefkivy: Using cefpython from <{}>".format(md))
        ver = cefpython.GetVersion()
        Logger.info("cefkivy: CEF Python : {ver}".format(ver=ver["version"]))
        Logger.info("cefkivy:   Chromium : {ver}".format(ver=ver["chrome_version"]))
        Logger.info("cefkivy:        CEF : {ver}".format(ver=ver["cef_version"]))
        Logger.info("cefkivy:     Python : {ver} {arch}".format(
            ver=platform.python_version(),
            arch=platform.architecture()[0]))

    def install_handler(self, handler):
        Logger.debug("cefkivy: Installing ClientHandler <Class {}>".format(handler.__name__))
        self.browser.SetClientHandler(handler(self))

    def realign(self, *_):
        ts = self.texture.size
        ss = self.size
        schg = (ts[0] != ss[0] or ts[1] != ss[1])
        if schg:
            self.texture = Texture.create(size=self.size, colorfmt='rgba', bufferfmt='ubyte')
            self.texture.flip_vertical()
        if self.__rect:
            with self.canvas:
                Color(1, 1, 1)
                self.__rect.pos = self.pos
                if schg:
                    self.__rect.size = self.size
            if schg:
                self.update_rect()
        if self.browser:
            self.browser.WasResized()
            self.browser.NotifyScreenInfoChanged()
        # TODO : Update this to the new keyboard when implemented
        try:
            k = self.__keyboard.widget
            p = k.parent
            p.remove_widget(k)
            p.add_widget(k)
        except:
            pass

    def update_rect(self):
        if self.__rect:
            self.__rect.texture = self.texture
