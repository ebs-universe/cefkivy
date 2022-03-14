

from kivy.config import Config
Config.set('kivy', 'log_level', 'debug')
Config.set('kivy', 'keyboard_mode', 'systemandmulti')

from cefkivy.browser import CefBrowser, cefpython
from kivy.app import App


class CefBrowserApp(App):
    def build(self):
        return CefBrowser(start_url='http://google.com')


def run():
    CefBrowserApp().run()
    cefpython.Shutdown()


if __name__ == '__main__':
    run()