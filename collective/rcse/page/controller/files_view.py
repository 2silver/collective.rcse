from plone.namedfile.field import NamedBlobFile
from zope import interface
from zope import schema
from zope import component
from z3c.form import button

from collective.rcse.i18n import _
from collective.rcse.page.controller import group_base
from collective.rcse.page.controller.navigationroot import \
    NavigationRootBaseView

CONTENT_TYPE = 'File'


class AddFormSchema(group_base.BaseAddFormSchema):
    """Add form"""
    file = NamedBlobFile(title=_(u"File"))
    title = schema.TextLine(
        title=_(u"Title"),
        required=False,
    )
    description = schema.Text(
        title=_(u"Description"),
        required=False
    )


class AddFormAdapter(group_base.BaseAddFormAdapter):
    interface.implements(AddFormSchema)
    component.adapts(interface.Interface)

    def __init__(self, context):
        group_base.BaseAddFormAdapter.__init__(self, context)
        self.title = None
        self.description = ''
        self.file = None


class AddForm(group_base.BaseAddForm):
    schema = AddFormSchema
    msg_added = _(u"File added")
    label = _(u"Add File")
    CONTENT_TYPE = CONTENT_TYPE

    @button.buttonAndHandler(_(u"Add file"))
    def handleAdd(self, action):
        group_base.BaseAddForm.handleAdd(self, action)


class FilesView(group_base.BaseAddFormView):
    """A filterable timeline"""
    filter_type = [CONTENT_TYPE]
    form = AddForm


class NavigationRootFilesView(FilesView, NavigationRootBaseView):
    def update(self):
        FilesView.update(self)
        NavigationRootBaseView.update(self)
