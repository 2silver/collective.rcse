from zope import interface
from zope import schema
from zope import component
from z3c.form import button

from plone.namedfile.field import NamedBlobImage

from collective.rcse.i18n import _
from collective.rcse.page.controller import group_base
from collective.rcse.page.controller.navigationroot import \
    NavigationRootBaseView

CONTENT_TYPE = "collective.rcse.article"


class AddFormSchema(group_base.BaseAddFormSchema):
    """Add form"""
    title = schema.TextLine(title=_(u"Title"))
    description = schema.Text(
        title=_(u"Description"),
        required=False
    )
    image = NamedBlobImage(
        title=_(u"Image"),
        description=_(u"Please put an image file here"),
        required=False
    )


class AddFormAdapter(group_base.BaseAddFormAdapter):
    interface.implements(AddFormSchema)
    component.adapts(interface.Interface)

    def __init__(self, context):
        group_base.BaseAddFormAdapter.__init__(self, context)
        self.title = None
        self.image = None
        self.description = ''


class AddForm(group_base.BaseAddForm):
    schema = AddFormSchema
    CONTENT_TYPE = CONTENT_TYPE
    msg_added = _(u"Article added")
    label = _(u"Add article")

    @button.buttonAndHandler(_(u"Add Article"))
    def handleAdd(self, action):
        group_base.BaseAddForm.handleAdd(self, action)


class ArticlesView(group_base.BaseAddFormView):
    """A filterable blog view"""
    filter_type = [CONTENT_TYPE]
    form = AddForm


class NavigationRootArticlesView(ArticlesView, NavigationRootBaseView):
    def update(self):
        ArticlesView.update(self)
        NavigationRootBaseView.update(self)
