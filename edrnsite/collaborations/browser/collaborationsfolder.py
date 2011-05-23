# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''EDRN Site Collaborations: collaborations folder view
'''

from Acquisition import aq_inner
from edrnsite.collaborations.interfaces import ICollaborativeGroup
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class CollaborationsFolderView(BrowserView):
    '''Default view for a Collaborations Folder.'''
    __call__ = ViewPageTemplateFile('templates/collaborationsfolder.pt')
    def haveGroups(self):
        return len(self.groups()) > 0
    @memoize
    def groups(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(
            object_provides=ICollaborativeGroup.__identifier__,
            path=dict(query='/'.join(context.getPhysicalPath()), depth=1)
        )
        return [dict(title=i.Title, description=i.Description, url=i.getURL()) for i in results]
    
