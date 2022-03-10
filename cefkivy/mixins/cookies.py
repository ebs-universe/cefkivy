

import os
from kivy.logger import Logger
from kivy.properties import StringProperty

from ..browser import cefpython


class CookieManagerMixin(object):
    resources_dir = StringProperty("")

    def __init__(self, resources_dir):
        self.resources_dir = resources_dir
        # Set cookie manager
        # Determine if default resources dir should be used or a custom
        if self.resources_dir:
            resources = self.resources_dir
        else:
            resources = cefpython.GetModuleDirectory()

        Logger.debug("cefkivy: Using Resource Directory <{}>".format(resources))
        Logger.debug("cefkivy: Creating the CookieManager")
        cookie_manager = cefpython.CookieManager.GetGlobalManager()
        cookie_path = os.path.join(resources, "cookies")
        cookie_manager.SetStoragePath(cookie_path, True)

    def delete_cookie(self, url=""):
        """ Deletes the cookie with the given url. If url is empty all cookies get deleted.
        """
        cookie_manager = cefpython.CookieManager.GetGlobalManager()
        if cookie_manager:
            cookie_manager.DeleteCookies(url, "")
        else:
            print("No cookie manager found!, Can't delete cookie(s)")
