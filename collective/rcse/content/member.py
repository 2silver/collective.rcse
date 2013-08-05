from plone.autoform import directives as form
from plone.app.textfield import RichText
from plone.namedfile import field
from plone.supermodel import model
from z3c.form.browser.select import SelectFieldWidget
from zope import schema

from collective.rcse.i18n import _
from collective.rcse.content import vocabularies


class IMember(model.Schema):
    """This is a high level schema of info"""

    model.fieldset(
        'personal',
        label=_(u'Personal information'),
        fields=[
            'gender',
            'bio',
            'lang',
            'birthdate',
            'avatar',
            'areas_of_expertise',
            'interests',
            ]
        )

    model.fieldset(
        'contact',
        label=_(u'Contact information'),
        fields=[
            'professional_email',
            'personal_email',
            'professional_mobile_phone',
            'personal_mobile_phone',
            'professional_landline_phone',
            'personal_landline_phone',
            'skype',
            'website',
            'blog',
            'viadeo',
            'linkedin',
            'google',
            'twitter',
            ]
        )

    username = schema.ASCIILine(
        title=_(u"Username"),
        readonly=True
    )
    settings = schema.Dict(
        title=_(u"Settings"),
        key_type=schema.ASCIILine(),
        value_type=schema.Bool(),
        readonly=True,
    )
    email = schema.TextLine(
        title=_(u"E-mail"),
        required=True,
    )
    first_name = schema.TextLine(
        title=_(u"First Name"),
        required=True,
    )
    last_name = schema.TextLine(
        title=_(u"Last Name"),
        required=True,
    )

    company = schema.ASCIILine(
        title=_(u"Company")
    )  # ID
    function = schema.TextLine(
        title=_(u"Function"),
    )

    bio = RichText(
        title=_(u"Presentation"),
        required=False
    )
    form.widget('lang', SelectFieldWidget, multiple="multiple")
    lang = schema.List(
        title=_(u"Spoken languages"),
        required=False,
        value_type=schema.Choice(
            vocabulary=vocabularies.languages
        ),
    )
    birthdate = schema.Date(
        title=_(u"Birthdate"),
        required=False
    )
    gender = schema.Choice(
        title=_(u"Gender"),
        vocabulary=vocabularies.gender,
        required=False
    )
    avatar = field.NamedBlobImage(
        title=_(u"Avatar"),
        required=False
    )

    areas_of_expertise = schema.List(
        title=_(u"Areas of expertise"),
        value_type=schema.TextLine(
            title=_(u"Expertise"),
        ),
        required=False
    )
    interests = schema.List(
        title=_(u"Interests"),
        value_type=schema.TextLine(
            title=_(u"Interest"),
        ),
        required=False
    )

    professional_email = schema.TextLine(
        title=_(u"Professional e-mail"),
        required=False
    )
    personal_email = schema.TextLine(
        title=_(u"Personal e-mail"),
        required=False
    )
    professional_mobile_phone = schema.TextLine(
        title=_(u"Professional mobile phone"),
        required=False
    )
    personal_mobile_phone = schema.TextLine(
        title=_(u"Personal mobile phone"),
        required=False
    )
    professional_landline_phone = schema.TextLine(
        title=_(u"Professional landline phone"),
        required=False
    )
    personal_landline_phone = schema.TextLine(
        title=_(u"Personal landline phone"),
        required=False
    )
    skype = schema.TextLine(
        title=_(u"Skype"),
        required=False
    )

    website = schema.URI(title=_(u"Website"), required=False)
    blog = schema.URI(title=_(u"Blog"), required=False)
    viadeo = schema.URI(title=_(u"Viadeo"), required=False)
    linkedin = schema.URI(title=_(u"LinkedIn"), required=False)
    google = schema.URI(title=_(u"Google+"), required=False)
    twitter = schema.URI(title=_(u"Twitter"), required=False)