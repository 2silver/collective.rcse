import datetime

from zope import interface
from zope import schema
from zope import component
from z3c.form import button

from plone.app.event.portlets import portlet_calendar
from plone.app.event import messageFactory as _pae
from plone.app.event.browser.event_listing import EventListing
from plone.z3cform.layout import FormWrapper
from Products.Five.browser import BrowserView
from Products.CMFPlone.utils import getToolByName

from collective.rcse.i18n import _
from collective.rcse.page.controller import group_base

CONTENT_TYPE = "collective.rcse.event"


#class AddFormSchema(IEventBasic):
class AddFormSchema(group_base.BaseAddFormSchema):
    """Add form"""

    title = schema.TextLine(title=_(u"Title"))
    description = schema.Text(
        title=_(u"Description"),
        required=False
    )

    start = schema.Datetime(
        title=_pae(
            u'label_event_start',
            default=u'Event Starts'
        ),
        description=_pae(
            u'help_event_start',
            default=u'Date and Time, when the event begins.'
        ),
        required=True
    )

    end = schema.Datetime(
        title=_pae(
            u'label_event_end',
            default=u'Event Ends'
        ),
        description=_pae(
            u'help_event_end',
            default=u'Date and Time, when the event ends.'
        ),
        required=True
    )

    whole_day = schema.Bool(
        title=_pae(
            u'label_event_whole_day',
            default=u'Whole Day'
        ),
        description=_pae(
            u'help_event_whole_day',
            default=u'Event lasts whole day.'
        ),
        required=False
    )

    open_end = schema.Bool(
        title=_pae(
            u'label_event_open_end',
            default=u'Open End'
        ),
        description=_pae(
            u'help_event_open_end',
            default=u"This event is open ended."
        ),
        required=False
    )

    timezone = schema.Choice(
        title=_pae(
            u'label_event_timezone',
            default=u'Timezone'
        ),
        description=_pae(
            u'help_event_timezone',
            default=u'Select the Timezone, where this event happens.'
        ),
        required=True,
        vocabulary="plone.app.event.AvailableTimezones",
        default="Europe/Paris"
    )


class AddFormAdapter(group_base.BaseAddFormAdapter):
    interface.implements(AddFormSchema)
    component.adapts(interface.Interface)

    def __init__(self, context):
        group_base.BaseAddFormAdapter.__init__(self, context)
        self.title = None
        self.description = ''
        self.start = datetime.datetime.now()
        self.end = datetime.datetime.now() + datetime.timedelta(hours=1)
        self.whole_day = None
        self.open_end = None
        self.timezone = None


class AddForm(group_base.BaseAddForm):
    schema = AddFormSchema
    CONTENT_TYPE = CONTENT_TYPE
    msg_added = _(u"Event added")
    label = _(u"Add event")

#    ignoreContext = True

    @button.buttonAndHandler(_(u"Add event"))
    def handleAdd(self, action):
        group_base.BaseAddForm.handleAdd(self, action)


class CalendarEventsView(BrowserView):
    def update(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        portal_url = '/'.join(portal.getPhysicalPath())
        search_base = '/'.join(self.context.getPhysicalPath())
        search_base = search_base[len(portal_url):]
        data = type('Dummy', (object,), {'state': None,
                                         'search_base': search_base})
        self.renderer = portlet_calendar.Renderer(self.context, self.request,
                                                  None, None, data)
        self.renderer.update()

    def __call__(self):
        self.update()
        return self.renderer.render()


class EventsView(FormWrapper, EventListing):
    """A filterable blog view"""
    form = AddForm
    portlets_show = {
        'plone.leftcolumn': True,
        'plone.rightcolumn': False,
    }

    def __init__(self, context, request):
        FormWrapper.__init__(self, context, request)
        EventListing.__init__(self, context, request)

    def __call__(self):
        self.update()
        return self.index()


class NavigationRootEventsView(EventsView):
    pass
