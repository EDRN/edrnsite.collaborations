# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Collaborative Group implementation'''

from edrnsite.collaborations.config import PROJECTNAME
from edrnsite.collaborations.interfaces import ICollaborativeGroup
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from zope.interface import implements

CollaborativeGroupSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    # No other fields at this time.
))
CollaborativeGroupSchema['title'].storage = atapi.AnnotationStorage()
CollaborativeGroupSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(CollaborativeGroupSchema, folderish=True, moveDiscussion=False)

class CollaborativeGroup(folder.ATFolder):
    '''A collaborative group'''
    implements(ICollaborativeGroup)
    schema      = CollaborativeGroupSchema
    portal_type = 'Collaborative Group'
    description = atapi.ATFieldProperty('description')
    title       = atapi.ATFieldProperty('title')

atapi.registerType(CollaborativeGroup, PROJECTNAME)
