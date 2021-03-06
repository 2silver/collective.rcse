from Products.Five.browser import BrowserView

from collective.rcse.content.settings import ISettings
from collective.rcse.content.settings import getDefaultSettings


class GetSettings(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.settings = ISettings(self.context).settings
        self.default_settings = getDefaultSettings()

    def __call__(self):
        return self

    def get(self, key):
        if key in self.settings.keys():
            return self.settings[key]
        if key in self.default_settings.keys():
            return self.default_settings[key]
        raise KeyError

    def set(self, key, value):
        self.settings[key] = value
