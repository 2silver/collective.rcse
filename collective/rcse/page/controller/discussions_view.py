from zope import component
from zope import interface
from zope import schema
from z3c.form import form, field, button

from Products.CMFPlone import PloneMessageFactory
from Products.CMFPlone.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from plone.autoform.form import AutoExtensibleForm
from plone.dexterity import utils
from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model
from plone.z3cform.layout import FormWrapper

from collective.rcse.i18n import _
from collective.rcse.page.controller.group_base import BaseView
from collective.rcse.page.controller.navigationroot import NavigationRootBaseView

CONTENT_TYPE = "collective.rcse.discussion"

class AddDiscussionFormSchema(model.Schema):
    """Add form"""
    title = schema.TextLine(title=PloneMessageFactory(u"Title"))
    body = schema.Text(title=_(u"Subject"))
    file = NamedBlobFile(title=_(u"Attachment"),
                         required=False)


class AddDiscussionFormAdapter(object):
    interface.implements(AddDiscussionFormSchema)
    component.adapts(interface.Interface)

    def __init__(self, context):
        self.context = context
        self.image = None
        self.description = None

class AddDiscussionForm(AutoExtensibleForm, form.Form):
    schema = AddDiscussionFormSchema
    enableCSRFProtection = True

    @button.buttonAndHandler(_(u"Add Discussion"))
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            return False
        self.doAdd(data)

    def doAdd(self, data):
        container = self.context
        item = utils.createContentInContainer(
            container,
            CONTENT_TYPE,
            checkConstraints=True,
            **data)

        IStatusMessage(self.request).add(_(u"Discussion added"))
        referer = self.request.get("HTTP_REFERER")
        if not referer:
            referer = self.context.absolute_url()
        self.request.response.redirect(referer)


class DiscussionsView(BaseView, FormWrapper):
    """A filterable timeline"""
    filter_type = [CONTENT_TYPE]
    form = AddDiscussionForm

    def __init__(self, context, request):
        BaseView.__init__(self, context, request)
        FormWrapper.__init__(self, context, request)

    def update(self):
        BaseView.update(self)
        FormWrapper.update(self)


class NavigationRootDiscussionsView(DiscussionsView, NavigationRootBaseView):

    def update(self):
        DiscussionsView.update(self)
        NavigationRootBaseView.update(self)