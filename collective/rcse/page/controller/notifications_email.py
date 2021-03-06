from email.header import Header

from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.browser.interfaces import IBrowserView

from collective.whathappened.gatherer_manager import GathererManager
from collective.whathappened.storage_manager import StorageManager
from collective.whathappened.browser.notifications import (
    _redirectUrl, _getLastCheck, show, validateNotification,
    )
from collective.whathappened.exceptions import NotificationValueError

from collective.rcse.page.controller.person_view import GetMemberInfoView
from collective.rcse.utils import sudo


class SendEmail(BrowserView):
    """
    Send an email with unseen notification to a specific user.
    User is passed as a GET parameter "user".
    Key from collective.rcse.security is required as a "key" GET parameter.
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.check_key()
        self.get_user()
        if not self.check_setting():
            return "IGNORE"
        self.get_portal_url()
        self.get_notifications()
        if self.notificationsCount > 0:
            self.send_email()
        return "OK"

    def check_key(self):
        registry = getToolByName(self.context, 'portal_registry')
        key = registry.get(
            'collective.rcse.security.ISecuritySettings.cronKey', ''
            )
        key_get = self.request.get('key', '')
        if not key or key != key_get:
            raise Unauthorized

    def get_user(self):
        user_id = self.request.get('user', None)
        if user_id is None:
            raise ValueError("User parameter is required")
        self.user = user_id
        self._get_memberinfo()

    @sudo()
    def check_setting(self):
        return self.memberview.get_settings()\
            .get('receive_email_notifications')

    @sudo()
    def _get_memberinfo(self):
        self.memberview = GetMemberInfoView(self.context, self.request)
        self.memberview(self.user)
        self.memberinfo = self.memberview.get_membrane()

    def get_portal_url(self):
        portal_state = self.context.restrictedTraverse('plone_portal_state')
        navigation_root = portal_state.navigation_root()
        self.portal_url = navigation_root.absolute_url()

    def get_notifications(self):
        self.gatherer = GathererManager(self.context, self.request)
        self.storage = StorageManager(self.context, self.request)
        self.gatherer.setUser(self.user)
        self.storage.setUser(self.user)
        self.storage.initialize()
        self._updateNotifications()
        notifications = self.storage.getUnseenNotifications()
        self.storage.terminate()
        self.notifications = []
        for notification in notifications:
            self._append_notification(notification)
        self.notificationsCount = len(self.notifications)

    @sudo()
    def _append_notification(self, notification):
        try:
            content = validateNotification(self.context, notification)
        except NotificationValueError:
            return
        if IBrowserView.providedBy(content):
            url = content.context.absolute_url() + '/@@' + content.__name__
        else:
            context_state = content.restrictedTraverse('plone_context_state')
            url = context_state.view_url()

        self.notifications.append({
                'title': show(self.context, self.request, notification),
                'url': _redirectUrl(
                    self.context, self.request,
                    url, notification.where
                    )
                })

    def _updateNotifications(self):
        lastCheck = _getLastCheck(self.context, self.storage)
        newNotifications = self.gatherer.getNewNotifications(lastCheck)
        if newNotifications is not None:
            for notification in newNotifications:
                self.storage.storeNotification(notification)

    def send_email(self):
        host = getToolByName(self.context, 'MailHost')
        from_email = host.email_from_address
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        subject = Header(portal.Title(), 'utf-8').encode()
        mail_template = portal.email_notifications
        mail_text = mail_template(
            from_email=from_email,
            subject=subject,
            email=self.memberinfo.email,
            notifications=self.notifications,
            notificationsCount=self.notificationsCount,
            portal_url=self.portal_url,
            request=self.request
        )
        host.send(mail_text.encode('utf8'))


class GetMemberWithNewNotifications(BrowserView):
    def __call__(self):
        membrane_tool = getToolByName(self.context, 'membrane_tool')
        workflow_tool = getToolByName(self.context, "portal_workflow")
        brains = membrane_tool.unrestrictedSearchResults()
        members = []
        for brain in brains:
            member = self.context.unrestrictedTraverse(brain.getPath())
            status = workflow_tool.getStatusOf(
                "collective_rcse_member_workflow", member
                )
            if status['review_state'] == 'enabled':
                members.append(member.username)
        return '\n'.join(members)
