import logging
from Acquisition import aq_inner
from zope import component
from zope import schema
from plone.app.layout.viewlets.common import ViewletBase
from collective.rcse.content.member import IMember
from collective.rcse.content.company import ICompany
from dexterity.membrane.behavior.membraneuser import IMembraneUser
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from collective.rcse.i18n import _
logger = logging.getLogger("collective.rcse")


class ValidateAuthenticatedMember(ViewletBase):
    """This viewlet will redirect to @@personal_information if the user
    miss some information
    """
    member_schema = IMember
    company_schema = ICompany
    viewname = "@@personal-information"
    blacklist_views = [
        #login / logout
        'login', 'login_form', 'logout', 'logged_out',
        #registration
        '@@register', '@@personal-information', '@@register_information'
    ]

    def update(self):
        super(ValidateAuthenticatedMember, self).update()
        self.context_state = component.getMultiAdapter(
            (self.context, self.request), name=u'plone_context_state'
        )
        self.member = self.portal_state.member()
        #get member data
        catalog = getToolByName(self.context, 'membrane_tool')
        self.username = self.member.getUserName()
        self.member_data = None
        if self.username:
            results = catalog(getUserName=self.username)
            if results:
                self.member_data = results[0].getObject()
        self.company = None
        if self.member_data is not None:
            directory = self.portal_state.portal()['companies_directory']
            if self.member_data.company_id in directory:
                self.company = directory[self.member_data.company_id]
        self.status = IStatusMessage(self.request)

    def index(self):
        if self.testUser() or self.testMember() or self.testCompany():
            return ''
        return ''

    def testUser(self):
        if self.portal_state.anonymous():
            return True
        elif self.username == 'admin':
            return True
        elif self.view_in_blacklist():
            return True
        elif not self.is_registred():
            msg = _(u"You are not registred, please proceed")
            self.status.add(msg)
            url = '%s/@@register_information' % \
                (self.portal_state.portal_url())
            self.lock_rendering_and_redirect(url=url)
            return True
        return False

    def testMember(self):
        if IMembraneUser.providedBy(self.context) and \
                self.context.username == self.member.getUserName():
            return True
        elif not self.has_required_info():
            msg = _(u"Your profile is missing some required information")
            self.status.add(msg)
            url = '%s/edit' % (self.member_data.absolute_url())
            self.lock_rendering_and_redirect(url=url)
            return True
        elif self.is_disabled_user():
            msg = _(u"Your profile has been disabled.")
            self.status.add(msg)
            url = self.member_data.absolute_url()
            self.lock_rendering_and_redirect(url=url)
            return True
        elif not self.is_validated_user():
            msg = _(u"Your profile is waiting for approval")
            self.status.add(msg)
            url = self.member_data.absolute_url()
            self.lock_rendering_and_redirect(url=url)
            return True
        return False

    def testCompany(self):
        if ICompany.providedBy(self.context) and \
                self.context.id == self.member_data.company_id:
            return True
        elif not self.has_company_info() and self.is_company_owner():
            msg = _(u"Please complete your company information")
            self.status.add(msg)
            url = '%s/edit' % self.company.absolute_url()
            self.lock_rendering_and_redirect(url=url)
            return True
        return False

    def has_company_info(self):
        fields = schema.getFields(self.company_schema)
        for field_name, field in fields.iteritems():
            if field.required:
                if getattr(self.company, field_name, None) is None:
                    return False
        return True

    def is_company_owner(self):
        for user, roles in self.company.get_local_roles():
            if self.username == user and 'Owner' in roles:
                return True
        return False

    def has_required_info(self):
        #we will check all required field against the schema
        fields = schema.getFields(self.member_schema)
        for field_name, field in fields.iteritems():
            if field.required:
                if getattr(self.member_data, field_name, None) is None:
                    return False
        return True

    def is_registred(self):
        return self.member_data and self.member_data.company_id is not None

    def is_disabled_user(self):
        tool = getToolByName(self.context, "portal_workflow")
        data = aq_inner(self.member_data)
        return tool.getInfoFor(data, 'review_state', None) == "disabled"

    def is_validated_user(self):
        tool = getToolByName(self.context, "portal_workflow")
        data = aq_inner(self.member_data)
        return tool.getInfoFor(data, 'review_state', None) == "enabled"

    def lock_rendering_and_redirect(self, url):
        self.request.response.redirect(url, lock=True)
        self.request.response.setBody('', lock=True)

    def view_in_blacklist(self):
        viewname = self.request.get('URL').split('/')[-1]
        if viewname in self.blacklist_views:
            return True
        if viewname == self.viewname:
            return True
        return False
