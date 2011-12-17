-*- coding: utf-8 -*-

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

It also automatically created an index page and set it as the default view of
the Collaborative Group container::

    >>> 'index_html' in group.keys()
    True

This item is set as the default view of the Collaborative Group::

    >>> group.getDefaultPage()
    'index_html'

We do this because comments can't be applied to folders in Plone, but they can
appear on non-folder objects.  Speaking of, check out the comment box::

    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> browser.contents
    '...Add comment...'

However, you've got to have privileges to get that button, see::

    >>> unprivilegedBrowser.open(browser.url)
    >>> 'Add comment' in unprivilegedBrowser.contents
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

There's a chair, co-chair, and list of members::

    >>> browser.contents
    '...Chair:...Co-Chair:...Members...'

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

Since we're logged in, the special note about logging in to view additional
information doesn't appear::

    >>> 'If you are a member of this group,' in browser.contents
    False

But an unprivileged user does get it::

    >>> unprivilegedBrowser.open(portalURL + '/my-groups/my-fun-group')
    >>> unprivilegedBrowser.contents
    '...If you are a member of this group...log in...'


Referenced Items
----------------

However, none of it is terribly interesting!  What we need is some actual
information in this group.  So, let's revisit and update::

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='chair:list').displayValue = ['Steeldevil, Cloud']
    >>> browser.getControl(name='coChair:list').displayValue = ['Magicsoul, Jackal']
    >>> browser.getControl(name='members:list').displayValue = ['Flora, Quake', 'Starseraph, Amber']
    >>> browser.getControl(name='protocols:list').displayValue = ['Public Safety', 'Protocol Two']
    >>> browser.getControl(name='biomarkers:list').displayValue = ['Apogee 1']
    >>> browser.getControl(name='datasets:list').displayValue = ['Get Bent', 'Dataset 0', 'Dataset 1', 'Dataset 2', 'Dataset 3', 'Dataset 4', 'Dataset 5']
    >>> browser.getControl(name='projects:list').displayValue = ['Public Safety']
    >>> browser.getControl(name='form.button.save').click()

Now check it out::

    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> browser.contents
    '...Chair...Steeldevil, Cloud...Co-Chair...Magicsoul, Jackal...'
    >>> browser.contents
    '...Members...Flora, Quake...Starseraph, Amber...'
    >>> browser.contents
    '...Biomarkers...Apogee 1...Projects/Protocols...Public Safety...Data...Get Bent...'

Heather wants datasets to link to ECAS like they do on the "Science Data" tab.
Do they?  Check it out::

    >>> browser.contents
    '...Data...href="urn:edrn:top-secret-data"...Get Bent...'

But by the way, CA-513 suggested that the list of datasets, which show
collaborative groups, should make those groups linkable to the groups'
descriptions.  Well, that was before we had full-fledged Collaborative Group
objects!  Now we can link 'em directly::

    >>> browser.open(portalURL + '/datasets')
    >>> browser.contents
    '...<a href="http://nohost/my-groups/my-fun-group">My Fun Group</a>...'
    
Christos suggested that the remaining members be in a collapsible section::

    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> browser.contents
    '...collapsibleHeader...Members...collapsibleContent...Flora, Quake...'

In particular, the "Overview" tab has a nice listing of the top three
team projects and upcoming events on it::

    >>> browser.contents
    '...Overview...Upcoming Events...No upcoming events...Projects...Public Safety...Biomarkers...Apogee 1...Protocols...Public Safety...'

Notice that on the Projects/Protocols tab the PI of each protocol is mentioned
(and is a clickable link):

    >>> browser.contents
    '...Projects/Protocols...Projects...Public Safety...PI...Starseraph...Protocols...Public Safety...PI...Starseraph...'

Also, Heather wants datasets to be arranged by protocol::

    >>> browser.contents
    '...fieldset-data...Protocol Three...Dataset 1...Dataset 3...Dataset 5...Protocol Two...Dataset 2...Dataset 4...Public Safety...Get Bent...Datasets Outside of any Protocol...Dataset 0...'

And for the protocols to be clickable::

    >>> browser.contents
    '...href...protocols/p3...Protocol Three...protocols/p2...Protocol Two...protocols/ps-public-safety...Public Safety...'

There's a "Documents" tab which has bright shiny buttons::

    >>> browser.contents
    '...Documents...New Folder...New File...'

Those shiny buttons enable users who otherwise wouldn't realize there's an
"Add new" menu that lets them add new items.  Moreover, they appear because
we're logged in as someone with privileges.  If we log out, they'll go away::

    >>> unprivilegedBrowser.open(portalURL + '/my-groups/my-fun-group')
    >>> 'New Folder' in unprivilegedBrowser.contents
    False
    >>> 'New File' in unprivilegedBrowser.contents
    False

Let's press 'em and add some items.  First, a file::

    >>> from StringIO import StringIO
    >>> fakeFile = StringIO('%PDF-1.5\nThis is sample PDF file in disguise.\nDo not try to render it.')
    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> l = browser.getLink('New File')
    >>> l.url.endswith('createObject?type_name=File')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'My New File'
    >>> browser.getControl(name='description').value = u'A file for functional tests.'
    >>> browser.getControl(name='file_file').add_file(fakeFile, 'application/pdf', 'test.pdf')
    >>> browser.getControl(name='form.button.save').click()

And also a folder::

    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> l = browser.getLink('New Folder')
    >>> l.url.endswith('createObject?type_name=Folder')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'My New Folder'
    >>> browser.getControl(name='description').value = u'A foder for functional tests.'
    >>> browser.getControl(name='form.button.save').click()
    
These items should appear on the Documents tab now::

    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> browser.contents
    '...My New File...My New Folder...'


Update Notifications
--------------------

You may have noticed that when we first created this fun group (Rebecca Black
would've been proud), we enabled the "updateNotifications" setting.  That
settings tells collaborative groups to let their mailing lists know that stuff
has been added, edited, or had its publication state change.  Just above we
added three items, so our test mail host should have sent three messages::

    >>> from Products.CMFCore.utils import getToolByName
    >>> mailHost = getToolByName(portal, 'MailHost')
    >>> len(mailHost.getSentMessages()) >= 3
    True

The message typically tells what was added and gives a URL to it::

    >>> message = mailHost.getSentMessages()[1]
    >>> 'A new item has been added to your collaborative group' in message
    True
    >>> portalURL + '/my-groups/my-fun-group/my-new-file' in message
    True

Let's turn off the updateNotifications setting::

    >>> browser.open(portalURL + '/my-groups/my-fun-group/edit')
    >>> browser.getControl(name='updateNotifications:boolean').value = False
    >>> browser.getControl(name='form.button.save').click()
    >>> mailHost.resetSentMessages()

And then add a new item::

    >>> browser.getLink(id='folder').click()
    >>> browser.getControl(name='title').value = u'Another New Folder'
    >>> browser.getControl(name='description').value = u'Yet another folder for functional tests.'
    >>> browser.getControl(name='form.button.save').click()

Now take note of the sent messages::

    >>> len(mailHost.getSentMessages())
    0

Perfect.


Highlights (CA-806)
-------------------

Highlights are news items that are deemed worthy of special announcement for a
collaborative group.  They get their own special place on the Overview tab::

    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> browser.contents
    '...Highlights...This group has not yet published any highlights...'

To get them there we had to re-arrange the overview tab so that it's arranged
like this:

+------------+-----------------+
| Highlights | Upcoming Events |
+------------+-----------------+
| Projects                     |
+------------+-----------------+

And so it is::

    browser.contents
    '...Highlights...Upcoming Events...Projects...'

Adding a highlight is like adding any other content::

    >>> l = browser.getLink(id='highlight')
    >>> l.url.endswith('createObject?type_name=Highlight')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'Validated Marker Woot!'
    >>> browser.getControl(name='description').value = u'We validated a marker, woot!'
    >>> browser.getControl(name='text').value = u'<p>Yeah baby, <em>validated</em>!</p>'
    >>> import base64
    >>> fakeImage = StringIO(base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='))
    >>> browser.getControl(name='image_file').add_file(fakeImage, 'image/png', 'fakeImage.png')
    >>> browser.getControl(name='imageCaption').value = u'Yo.'
    >>> browser.getControl(name='form.button.save').click()
    >>> highlight = group['validated-marker-woot']
    >>> highlight.Title()
    'Validated Marker Woot!'
    >>> highlight.Description()
    'We validated a marker, woot!'
    >>> highlight.getText()
    '<p>Yeah baby, <em>validated</em>!</p>'
    >>> highlight.getImageCaption()
    'Yo.'

Highlights appear in the group's overview tab once they're published.  The one
we created just above wasn't published, so it shouldn't be there::

    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> 'Validated Marker Woot!' in browser.contents
    False

So, we'll publish it::

    >>> browser.open(portalURL + '/my-groups/my-fun-group/validated-marker-woot/content_status_modify?workflow_action=publish')
    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> 'Validated Marker Woot!' in browser.contents
    True

Much better.


Event Calendar
--------------

You can add events (meetings, conferences, telecons, etc.) to Collaborative
Groups.  Look at the Calendar tab::

    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> browser.contents
    '...Calendar...New Event...'

Yes, that's another big shiny button that allows privileged users to create
new events in the calendar.  Unprivileged users get no button::

    >>> unprivilegedBrowser.open(portalURL + '/my-groups/my-fun-group')
    >>> 'New Event' in unprivilegedBrowser.contents
    False

Note also::

    >>> browser.contents
    '...There are no current events...'

We can fix that by hitting that big shiny button::

    >>> l = browser.getLink('New Event')
    >>> l.url.endswith('createObject?type_name=Collaborative%20Group%20Event')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'Fun Meeting'
    >>> browser.getControl(name='description').value = u'Gonna be lots of fun'

When should this meeting occur?  Let's say in a few days::

    >>> from datetime import datetime, timedelta
    >>> fewDays = datetime.now() + timedelta(6)
    >>> browser.getControl(name='startDate_year').displayValue = [str(fewDays.year)]
    >>> browser.getControl(name='startDate_month').value = ['%02d' % fewDays.month]
    >>> browser.getControl(name='startDate_day').value = ['%02d' % fewDays.day]

And we'll make it last a day::

    >>> dayAfter = fewDays + timedelta(1)
    >>> browser.getControl(name='endDate_year').displayValue = [str(dayAfter.year)]
    >>> browser.getControl(name='endDate_month').value = ['%02d' % dayAfter.month]
    >>> browser.getControl(name='endDate_day').value = ['%02d' % dayAfter.day]
    >>> browser.getControl(name='form.button.save').click()
    
The event appears on the calendar::

    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> browser.contents
    '...Calendar...Fun Meeting...'

The event itself is a container, and it has a big shiny button to add new
files to it (things like meeting agenda)::

    >>> browser.open(portalURL + '/my-groups/my-fun-group/fun-meeting')
    >>> browser.contents
    '...Attach File...'

Of course, there are no files yet::

    >>> browser.contents
    '...There are no files attached to this event...'

Pressing that "Attach File" button lets you upload a file to the event::

    >>> l = browser.getLink('Attach File')
    >>> l.url.endswith('createObject?type_name=File')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'Meeting Agenda'
    >>> browser.getControl(name='description').value = u'Agenda for the fun meeting.'
    >>> fakeFile = StringIO('%PDF-1.5\nThis is another sample PDF file in disguise.\nDo not try to render it.')
    >>> browser.getControl(name='file_file').add_file(fakeFile, 'application/pdf', 'test.pdf')
    >>> browser.getControl(name='form.button.save').click()

Now you can grab the agenda easily::

    >>> browser.open(portalURL + '/my-groups/my-fun-group/fun-meeting')
    >>> browser.contents
    '...meeting-agenda...Meeting Agenda...'

Looks fine.  Now, let's make another event that's tomorrow::

    >>> tomorrow = datetime.now() + timedelta(1)
    >>> dayAfter = fewDays + timedelta(1)
    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> browser.getLink('New Event').click()
    >>> browser.getControl(name='title').value = u'Yet Another Fun Meeting'
    >>> browser.getControl(name='description').value = u'Gonna be less fun.'
    >>> browser.getControl(name='startDate_year').displayValue = [str(tomorrow.year)]
    >>> browser.getControl(name='startDate_month').value = ['%02d' % tomorrow.month]
    >>> browser.getControl(name='startDate_day').value = ['%02d' % tomorrow.day]
    >>> browser.getControl(name='endDate_year').displayValue = [str(dayAfter.year)]
    >>> browser.getControl(name='endDate_month').value = ['%02d' % dayAfter.month]
    >>> browser.getControl(name='endDate_day').value = ['%02d' % dayAfter.day]
    >>> browser.getControl(name='form.button.save').click()
    
This event should before the "Fun Meeting" since it happens tomorrow, while
the "Fun Meeting" isn't for a few days::

    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> browser.contents
    '...Calendar...Yet Another Fun Meeting...Fun Meeting...'

Also take note::

    >>> browser.contents
    '...Calendar...There are no past events...'

Let's see if adding another event that already took place changes that::

    >>> past = datetime.now() - timedelta(3)
    >>> dayAfter = past + timedelta(1)
    >>> browser.getLink('New Event').click()
    >>> browser.getControl(name='title').value = u'Old Meeting'
    >>> browser.getControl(name='description').value = u"This meeting wasn't that much fun."
    >>> browser.getControl(name='startDate_year').displayValue = [str(past.year)]
    >>> browser.getControl(name='startDate_month').value = ['%02d' % past.month]
    >>> browser.getControl(name='startDate_day').value = ['%02d' % past.day]
    >>> browser.getControl(name='endDate_year').displayValue = [str(dayAfter.year)]
    >>> browser.getControl(name='endDate_month').value = ['%02d' % dayAfter.month]
    >>> browser.getControl(name='endDate_day').value = ['%02d' % dayAfter.day]
    >>> browser.getControl(name='form.button.save').click()

And now::

    >>> browser.open(portalURL + '/my-groups/my-fun-group')
    >>> browser.contents
    '...Calendar...Yet Another Fun Meeting...Fun Meeting...Past Events...Old Meeting...'

Also notice the "Overview" tab::

    >>> browser.contents
    '...Overview...Upcoming Events...Yet Another Fun Meeting...Fun Meeting...Calendar...'

Woot!

In a future release we'll change from a list of events to an actual calendar.
