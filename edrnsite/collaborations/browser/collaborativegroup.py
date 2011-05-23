# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''EDRN Site Collaborations: collaborative group view
'''

from Acquisition import aq_inner
# from edrnsite.collaborations import PackageMessageFactory as _
# from edrnsite.collaborations.interfaces import
# from plone.memoize.instance import memoize
# from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import urllib

class CollaborativeGroupView(BrowserView):
    '''Default view for a Collaborative Group.'''
    __call__ = ViewPageTemplateFile('templates/collaborativegroup.pt')
    def facebookURL(self):
        context = aq_inner(self.context)
        return u'http://facebook.com/sharer.php?' + urllib.urlencode(dict(t=context.title, u=context.absolute_url()))
    def twitterURL(self):
        context = aq_inner(self.context)
        return u'http://twitter.com/share?' + urllib.urlencode(dict(text=context.title, url=context.absolute_url()))
