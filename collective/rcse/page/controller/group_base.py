from plone.app.search.browser import quote_chars
from Products.CMFCore.interfaces._tools import ICatalogTool
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from Products.Five.browser import BrowserView
from zope import interface
from zope import schema


class IBaseView(interface.Interface):
    """Base view for group, has builtin feature like filter"""

    filter_type = schema.ASCIILine(title=u"Filter on portal_type")
    query = schema.Dict(title=u"query for the catalog")
    catalog = schema.Object(title=u"Portal catalog",
                            schema=ICatalogTool)

    def get_items():
        """return catalog query results"""


class BaseView(BrowserView):
    """Base view for other group views.
    Filter based on GET parameters and filter_type."""
    interface.implements(IBaseView)

    filter_type = None
    valid_keys = ('sort_on', 'sort_order', 'sort_limit')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.query = {}

        self.catalog = None
        self.portal_state = None
        self.context_path = None
        self.context_state = None
        self.authenticated_member = None

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        if self.catalog is None:
            self.catalog = getToolByName(self.context, "portal_catalog")
        if self.context_path is None:
            self.context_path = '/'.join(self.context.getPhysicalPath())
        self._update_query()

    def _update_query(self):
        """build query from request"""
        self.query = {
            #"path": {'query': self.context_path, 'depth': 1},
            "path": self.context_path,
            "sort_on": "modified",
            "sort_order": "reverse",
            "sort_limit": 20,
            }
        self._update_query_portal_type()
        text = self.request.get('SearchableText', None)
        if text is not None:
            self.query["SearchableText"] = quote_chars(text)
        for k, v in self.request.form.items():
            if v and k in self.valid_keys:
                self.query[k] = v
        if self.query['sort_on'] == 'relevance':
            del self.query['sort_on']

    def _update_query_portal_type(self):
        types = self.request.get('portal_type', None)
        if types is not None and len(types) > 0:
            self.query["portal_type"] = set(types.split(','))
        if self.filter_type is not None and len(self.filter_type) > 0:
            if self.query.get('portal_type'):
                portal_type = self.query["portal_type"] & set(self.filter_type)
                self.query["portal_type"] = portal_type
            else:
                self.query["portal_type"] = self.filter_type
        if self.query.get("portal_type"):
            self.query["portal_type"] = list(self.query["portal_type"])

    def get_content(self, batch=True, b_size=10, b_start=0, pagerange=7, full=False):
        brains = self.catalog(self.query)
        if batch:
            results = Batch(brains, b_size, start=b_start)#, pagerange=pagerange)
        if full and batch:
            results = [brain.getObject() for brain in results]
        elif full and not batch:
            results = [brain.getObject() for brain in brains]
        elif not full and not batch:
            results = brains
        return results
