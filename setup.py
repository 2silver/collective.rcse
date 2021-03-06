from setuptools import setup, find_packages

version = '1.0'

setup(
    name='collective.rcse',
    version=version,
    description="Project based on Plone",
    long_description=open("README.rst").read() + "\n" +
                     open("CHANGES.txt").read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Framework :: Zope2",
        "Framework :: Plone",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='plone',
    author='JeanMichel aka toutpt',
    author_email='toutpt@gmail.com',
    url='https://github.com/makinacorpus/collective.rcse',
    license='gpl',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Plone',
        'cioppino.twothumbs',
        'collective.etherpad',
        'collective.favoriting',
        'collective.history',
        'collective.js.datatables',
        'collective.localrolesdatatables',
        'collective.mediaelementjs',
        'collective.memberdatatables',
        'collective.oembed',
        'collective.picturefill',
        'collective.polls',
        'collective.portlet.embed',
        'collective.portlet.favoriting',
        'collective.portlet.localusers',
        'collective.portlet.oembed',
        'collective.readitlater',
        'collective.themeswitcher',
        'collective.transcode.star',
        'collective.watcherlist',
        'collective.whathappened',
        'collective.z3cform.html5widgets',
        'dexterity.membrane',
        'plone.app.async',
        'plone.app.dexterity',
        'plone.app.versioningbehavior',
        'plone.app.contenttypes',
        'plone.app.event[dexterity]',
        'plone.app.collection',
        'plone.namedfile[blobs]',
        'python-memcached',
        'plonetheme.jquerymobile',
        'icalendar',
        'z3c.unconfigure',
        'python-memcached',
        'Products.MemcachedManager',
        # -*- Extra requirements: -*-
    ],
    extras_require=dict(
        test=['plone.app.testing', 'plone.app.robotframework', 'plone.api', 'selenium'],
    ),
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
    setup_requires=[],
)
