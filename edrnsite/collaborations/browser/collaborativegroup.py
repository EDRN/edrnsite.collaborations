# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''EDRN Site Collaborations: collaborative group view
'''

from Acquisition import aq_inner
from DateTime import DateTime
from plone.memoize.instance import memoize
from Products.ATContentTypes.interface.event import IATEvent
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import urllib

_top = 3

# Why aren't these permission names defined as constants somewhere in ATContentTypes?
_addableContent = {
    # Add type   Permission name                    Type name
    'event':    ('ATContentTypes: Add Event',       'Event'),
    'file':     ('ATContentTypes: Add File',        'File'),
    'image':    ('ATContentTypes: Add Image',       'Image'),
    'page':     ('ATContentTypes: Add Document',    'Document'),
}

class CollaborativeGroupView(BrowserView):
    '''Default view for a Collaborative Group.'''
    index = ViewPageTemplateFile('templates/collaborativegroup.pt')
    def __call__(self):
        return self.index()
    def facebookURL(self):
        context = aq_inner(self.context)
        return u'http://facebook.com/sharer.php?' + urllib.urlencode(dict(t=context.title, u=context.absolute_url()))
    def twitterURL(self):
        context = aq_inner(self.context)
        return u'http://twitter.com/share?' + urllib.urlencode(dict(text=context.title, url=context.absolute_url()))
    @memoize
    def topBiomarkers(self):
        context = aq_inner(self.context)
        return context.biomarkers[0:_top]
    @memoize
    def topProtocols(self):
        context = aq_inner(self.context)
        return context.protocols[0:_top]
    @memoize
    def numBiomarkers(self):
        context = aq_inner(self.context)
        return len(context.biomarkers)
    @memoize
    def numProtocols(self):
        context = aq_inner(self.context)
        return len(context.protocols)
    def numTops(self):
        return _top
    @memoize
    def membersColumns(self):
        members = aq_inner(self.context).members
        members.sort(lambda a, b: cmp(a.title, b.title))
        half = len(members)/2 + 1
        left, right = members[:half], members[half:]
        return left, right
    def showNewButton(self, buttonType):
        if buttonType not in _addableContent: return False
        context = aq_inner(self.context)
        mtool = getToolByName(context, 'portal_membership')
        return mtool.checkPermission(_addableContent[buttonType][0], context)
    def newButtonLink(self, buttonType):
        return aq_inner(self.context).absolute_url() + '/createObject?type_name=' + _addableContent[buttonType][1]
    def haveEvents(self):
        return len(self.currentEvents()) > 0
    def havePastEvents(self):
        return len(self.pastEvents()) > 0
    @memoize
    def currentEvents(self):
        return self._getEvents(end={'query': DateTime(), 'range': 'min'})
    @memoize
    def pastEvents(self):
        return self._getEvents(end={'query': DateTime(), 'range': 'max'})
    def _getEvents(self, **criteria):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IATEvent.__identifier__, sort_on='start', **criteria)
        return [dict(title=i.Title, description=i.Description, start=i.start, url=i.getURL()) for i in results]
    
