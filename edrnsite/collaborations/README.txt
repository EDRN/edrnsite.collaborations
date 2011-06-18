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

We'll also have a second browser that's unprivileged for some later
demonstrations::

    >>> unprivilegedBrowser = Browser(app)

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
    >>> browser.getControl(name='updateNotifications:boolean').value = True
    >>> browser.getControl(name='form.button.save').click()
    >>> 'my-fun-group' in cf.keys()
    True
    >>> group = cf['my-fun-group']
    >>> group.title
    'My Fun Group'
    >>> group.description
    'A group dedicated towards the common goal of "fun".'
    >>> group.updateNotifications
    True

Notice now that the Collaborations Folder is no longer empty::

    >>> browser.open(portalURL + '/my-groups')
    >>> browser.contents
    '...Groups...My Fun Group...'

Meanwhile, the Collaborative Group is pretty fancy.  First off, it turns off
the right-side portlets (news feeds) since we need the space::

    >>> 'portal-column-two' in browser.contents
    False

Collaborative Groups are all about the new social media, so see that it has
Facebook and Twitter buttons .  .  .  actually, no.  Turns out old doctors
hate new media.  So let's make sure that there are NOT any Facebook or Twitter
buttons::

    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> 'facebook.com' in browser.contents
    False
    >>> 'twitter.com' in browser.contents
    False

There's a list of members::

    >>> browser.contents
    '...<h2>Members</h2>...'

And there's a set of tabs providing access to an overview, biomarkers,
protocols, team projects, data, and a calendar, (in that order)::

    >>> overview = browser.contents.index('fieldset-overview')
    >>> biomarkers = browser.contents.index('fieldset-biomarkers')
    >>> protocols = browser.contents.index('fieldset-protocols')
    >>> data = browser.contents.index('fieldset-data')
    >>> calendar = browser.contents.index('fieldset-calendar')
    >>> documents = browser.contents.index('fieldset-documents')
    >>> overview < biomarkers < protocols < data < calendar < documents
    True

Note also that, due to lack of room, we've combined Projects and Protocols::

    >>> browser.contents
    '...Projects/Protocols...'

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
    '...Biomarkers...Apogee 1...Projects/Protocols...Public Safety...Data...Get Bent...'

In particular, the "Overview" tab has a nice listing of the top three
biomarkers and protocols on it::

    >>> browser.contents
    '...Overview...Apogee 1...Public Safety...Biomarkers...Apogee 1...Protocols...Public Safety...'

There's a "Documents" tab which has bright shiny buttons::

    >>> browser.contents
    '...Documents...New Page...New File...New Image...'

Those shiny buttons enable users who otherwise wouldn't realize there's an
"Add new" menu that lets them add new items.  Moreover, they appear because
we're logged in as someone with privileges.  If we log out, they'll go away::

    >>> unprivilegedBrowser.open(portalURL + '/my-groups/my-fun-group')
    >>> 'New Page' in unprivilegedBrowser.contents
    False
    >>> 'New File' in unprivilegedBrowser.contents
    False
    >>> 'New Image' in unprivilegedBrowser.contents
    False

Let's press 'em and add some items.  First, a web page::

    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> l = browser.getLink('New Page')
    >>> l.url.endswith('createObject?type_name=Document')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'New Web Page'
    >>> browser.getControl(name='description').value = u'A page for functional tests.'
    >>> browser.getControl(name='text').value = u'Seriously, this is just a test page to test adding pages to collaborative groups.'
    >>> browser.getControl(name='form.button.save').click()

And a file::

    >>> from StringIO import StringIO
    >>> fakeFile = StringIO('%PDF-1.5\nThis is sample PDF file in disguise.\nDo not try to render it.')
    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> l = browser.getLink('New File')
    >>> l.url.endswith('createObject?type_name=File')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'New File'
    >>> browser.getControl(name='description').value = u'A file for functional tests.'
    >>> browser.getControl(name='file_file').add_file(fakeFile, 'application/pdf', 'test.pdf')
    >>> browser.getControl(name='form.button.save').click()

And finally, an image::

    >>> import base64
    >>> fakeImage = StringIO(base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='))
    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> l = browser.getLink('New Image')
    >>> l.url.endswith('createObject?type_name=Image')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'New Image'
    >>> browser.getControl(name='description').value = u'An image for functional tests.'
    >>> browser.getControl(name='image_file').add_file(fakeImage, 'image/png', 'test.png')
    >>> browser.getControl(name='form.button.save').click()

These items should all appear on the Documents tab now::

    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> browser.contents
    '...New Web Page...New File...New Image...'

TODO: functional testing of updateNotifications:
- add content rules to a collaborative group, test mail host
- add content, and see if email gets sent when updateNotifications = true
- ensure mail not sent when updateNotifications = false
