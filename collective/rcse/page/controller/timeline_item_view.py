from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.uuid.interfaces import IUUID


class TimelineItemView(BrowserView):
    """generic view to display an item in the timeline"""

    def __call__(self):
        self.update()
        return self.index()

    def __init__(self, context, request):
        super(TimelineItemView, self).__init__(context, request)
        self.membership = None
        self.portal_url = None
        self.tileid = None
        self.group = None
        self.group_url = None
        self.group_title = None
        self.effective_date = None

    def update(self):
        if self.membership is None:
            self.membership = getToolByName(self.context, "portal_membership")
        if self.portal_url is None:
            self.portal_url = getToolByName(self.context, 'portal_url')()
        if self.tileid is None:
            self.tileid = IUUID(self.context)
        if self.group is None:
            self.group = self.context.aq_inner.aq_parent
        if self.group_url is None:
            self.group_url = self.group.absolute_url()
        if self.group_title is None:
            self.group_title = self.group.Title()
        if self.effective_date is None:
            self.effective_date = self.get_effective_date()

    def get_content(self):
        return self.context.restrictedTraverse('tile_view')()

    def get_effective_date(self):
        effective = None
        if self.context.effective_date is not None:
            effective = self.context.effective_date
        elif self.context.modification_date is not None:
            effective = self.context.modification_date
        elif self.context.creation_date is not None:
            effective = self.context.creation_date

        if effective is not None:
            return effective.strftime("%d-%m-%Y")
        return ""
