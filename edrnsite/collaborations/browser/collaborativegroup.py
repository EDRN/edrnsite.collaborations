# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''EDRN Site Collaborations: collaborative group view
'''

from Acquisition import aq_inner
# from edrnsite.collaborations import PackageMessageFactory as _
# from edrnsite.collaborations.interfaces import
# from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize.instance import memoize
import urllib

_top = 3

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
        members.sort()
        half = len(members)/2 + 1
        left, right = members[:half], members[half:]
        return left, right
