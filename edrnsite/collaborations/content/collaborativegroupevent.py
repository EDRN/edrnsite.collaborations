# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.


'''Collaborative Group Event implementation'''

from edrnsite.collaborations.config import PROJECTNAME
from edrnsite.collaborations.interfaces import ICollaborativeGroupEvent
from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata, folder, event
from zope.interface import implements

CollaborativeGroupEventSchema = folder.ATFolderSchema.copy() + event.ATEventSchema.copy() + atapi.Schema((
    # Nothing else needed for now
))

schemata.finalizeATCTSchema(CollaborativeGroupEventSchema, folderish=True, moveDiscussion=True)
# finalizeATCTSchema moves 'location' into 'categories', we move it back:
CollaborativeGroupEventSchema.changeSchemataForField('location', 'default')
CollaborativeGroupEventSchema.moveField('location', before='startDate')

class CollaborativeGroupEvent(folder.ATFolder):
    '''A collaborative group event'''
    implements(ICollaborativeGroupEvent)
    schema         = CollaborativeGroupEventSchema
    archetype_name = 'Collaborative Group Event'
    portal_type    = 'Collaborative Group Event'

atapi.registerType(CollaborativeGroupEvent, PROJECTNAME)
