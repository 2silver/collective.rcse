from plone.namedfile.field import NamedBlobFile
from collective.rcse.i18n import RCSEMessageFactory
from collective.rcse.content import common

_ = RCSEMessageFactory


class FileSchema(common.RCSEContent):
    """A conference session. Sessions are managed inside Programs.
    """

    file = NamedBlobFile(title=_(u"File"))
