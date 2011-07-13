# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''EDRN Site Collaborations: collaborative group event browser views
'''

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize.instance import memoize

_atFilePerm = 'ATContentTypes: Add File'

class CollaborativeGroupEventView(BrowserView):
    '''Default view for a Collaborative Group Event.'''
    __call__ = ViewPageTemplateFile('templates/collaborativegroupevent.pt')
    def showNewFileButton(self):
        context = aq_inner(self.context)
        mtool = getToolByName(context, 'portal_membership')
        return mtool.checkPermission(_atFilePerm, context)
    def newFileButtonLink(self):
        return aq_inner(self.context).absolute_url() + '/createObject?type_name=File'
    def haveFiles(self):
        return len(self.files()) > 0
    @memoize
    def files(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(path=dict(query='/'.join(context.getPhysicalPath()), depth=1), sort_on='sortable_title')
        return [dict(title=i.Title, description=i.Description, url=i.getURL()) for i in results]
    
