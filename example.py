

from kivy.config import Config
Config.set('kivy', 'log_level', 'debug')
Config.set('kivy', 'keyboard_mode', 'systemandmulti')

from kivy_garden.ebs.cefkivy.browser import CefBrowser, cefpython
from kivy.app import App


class CefBrowserApp(App):
    def build(self):
        return CefBrowser(start_url='https://india.gov.in/')


def run():
    CefBrowserApp().run()
    cefpython.Shutdown()


if __name__ == '__main__':
    run()
