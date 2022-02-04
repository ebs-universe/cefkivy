
from cefkivy.browser import CefBrowser, cefpython
from kivy.app import App


class CefBrowserApp(App):
    def build(self):
        return CefBrowser(start_url='http://kivy.org')


def run():
    CefBrowserApp().run()
    cefpython.Shutdown()


if __name__ == '__main__':
    run()