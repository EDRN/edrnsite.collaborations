The package ``edrnsite.collaborations`` provides Plone-based content types to
enable EDRN collaborative groups to share information, calendars, comments,
and to keep track of biomarkers, datasets, and other information elsewhere in
the EDRN public portal that's of interest to the collaborative group.

This document documents and demonstrates the content types as a series of
functional tests using a test browser.

First we have to set up some things and login to the site::

    >>> app = layer['app']
    >>> from plone.testing.z2 import Browser
    >>> from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
    >>> browser = Browser(app)
    >>> browser.handleErrors = False
    >>> browser.addHeader('Authorization', 'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
    >>> portal = layer['portal']    
    >>> portalURL = portal.absolute_url()

Now we can check out the new types introduced in this package.


Collaborations Folder
=====================

A Collaborations Folder's sole purpose is to hold onto Collaborative Groups.
They may be created anywhere within the site::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='collaborations-folder')
    >>> l.url.endswith('createObject?type_name=Collaborations+Folder')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'My Groups'
    >>> browser.getControl(name='description').value = u'Groups that like to collaborate on stuff.'
    >>> browser.getControl(name='form.button.save').click()
    >>> 'my-groups' in portal.keys()
    True
    >>> cf = portal['my-groups']
    >>> cf.title
    'My Groups'
    >>> cf.description
    'Groups that like to collaborate on stuff.'

And viewing this empty folder::

    >>> browser.open(portalURL + '/my-groups')
    >>> browser.contents
    '...Groups...There are no collaborative groups in this folder...'

We'll soon remedy that.


Collaborative Group
===================

A Collaborative Group is the point of all this: a place where a group of
people can come together and share everything important to them, collect
things of interest to them elsewhere in the portal, add their own content, and
so forth.  Collaborative Groups can be added solely within Collaborations
Folders::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='collaborative-group')
    Traceback (most recent call last):
    ...
    LinkNotFoundError
    >>> browser.open(portalURL + '/my-groups')
    >>> l = browser.getLink(id='collaborative-group')
    >>> l.url.endswith('createObject?type_name=Collaborative+Group')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'My Fun Group'
    >>> browser.getControl(name='description').value = u'A group dedicated towards the common goal of "fun".'
    >>> browser.getControl(name='form.button.save').click()
    >>> 'my-fun-group' in cf.keys()
    True
    >>> group = cf['my-fun-group']
    >>> group.title
    'My Fun Group'
    >>> group.description
    'A group dedicated towards the common goal of "fun".'

Notice now that the Collaborations Folder is no longer empty::

    >>> browser.open(portalURL + '/my-groups')
    >>> browser.contents
    '...Groups...My Fun Group...'

Meanwhile, the Collaborative Group is pretty fancy.  First off, it turns off
the right-side portlets (news feeds) since we need the space::

    >>> 'portal-column-two' in browser.contents
    False

Collaborative Groups are all about the new social media, so see that it has
Facebook and Twitter buttons::

    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> browser.contents
    '...facebook.com/sharer.php?u=http...my-groups%2Fmy-fun-group...twitter.com/share...http...my-groups%2Fmy-fun-group...'

There's a list of members::

    >>> browser.contents
    '...<h2>Members</h2>...'

TODO: Add members and check for them.

And there's a set of tabs providing access to an overview, biomarkers,
protocols, team projects, data, and a calendar, (in that order)::

    >>> overview = browser.contents.index('fieldset-overview')
    >>> biomarkers = browser.contents.index('fieldset-biomarkers')
    >>> protocols = browser.contents.index('fieldset-protocols')
    >>> projects = browser.contents.index('fieldset-projects')
    >>> data = browser.contents.index('fieldset-data')
    >>> calendar = browser.contents.index('fieldset-calendar')
    >>> overview < biomarkers < protocols < projects < data < calendar
    True

However, none of it is terribly interesting!  What we need is some actual
information in this group.  So, let's revisit and update::

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='members:list').displayValue = ['Flora, Quake', 'Starseraph, Amber']
    >>> browser.getControl(name='protocols:list').displayValue = ['Public Safety']
    >>> browser.getControl(name='biomarkers:list').displayValue = ['Apogee 1']
    >>> browser.getControl(name='datasets:list').displayValue = ['Get Bent']
    >>> browser.getControl(name='projects:list').displayValue = ['Public Safety']
    >>> browser.getControl(name='form.button.save').click()

Now check it out::

    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> browser.contents
    '...Members...Flora, Quake...Starseraph, Amber...'
    >>> browser.contents
    '...Biomarkers...Apogee 1...Protocols...Public Safety...Projects...Public Safety...Data...Get Bent...'

In particular, the "Overview" tab has a nice listing of the top three
biomarkers and protocols on it::

    >>> browser.contents
    '...Overview...Apogee 1...Public Safety...Biomarkers...Apogee 1...Protocols...Public Safety...'

