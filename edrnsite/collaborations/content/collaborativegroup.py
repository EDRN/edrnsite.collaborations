# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Collaborative Group implementation'''

from edrnsite.collaborations import PackageMessageFactory as _
from edrnsite.collaborations.config import PROJECTNAME
from edrnsite.collaborations.interfaces import ICollaborativeGroup
from plone.app.contentrules.rule import get_assignments
from plone.contentrules.engine.assignments import RuleAssignment
from plone.contentrules.engine.interfaces import IRuleAssignmentManager, IRuleStorage
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.interface import implements

CollaborativeGroupSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.BooleanField(
        'updateNotifications',
        required=False,
        storage=atapi.AnnotationStorage(),
        widget=atapi.BooleanWidget(
            label=_(u'Update Notifications'),
            description=_(u'Enable notifying members (by email) of updates to this collaborative group.'),
        ),
    ),
))
CollaborativeGroupSchema['title'].storage = atapi.AnnotationStorage()
CollaborativeGroupSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(CollaborativeGroupSchema, folderish=True, moveDiscussion=False)

class CollaborativeGroup(folder.ATFolder):
    '''A collaborative group'''
    implements(ICollaborativeGroup)
    schema              = CollaborativeGroupSchema
    portal_type         = 'Collaborative Group'
    description         = atapi.ATFieldProperty('description')
    title               = atapi.ATFieldProperty('title')
    updateNotifications = atapi.ATFieldProperty('updateNotifications')

atapi.registerType(CollaborativeGroup, PROJECTNAME)

def addContentRules(obj, event):
    '''For newly-created collaborative groups, add content rules to handle notifications and an index page.'''
    if not ICollaborativeGroup.providedBy(obj): return
    factory = getToolByName(obj, 'portal_factory')
    if factory.isTemporary(obj): return
    # First, the index
    if obj.Title():
        if 'index_html' not in obj.keys():
            index = obj[obj.invokeFactory('Collaborative Group Index', 'index_html')]
        else:
            index = obj['index_html']
        index.setTitle(obj.title)
        index.setDescription(obj.description)
        index.reindexObject()
        obj.setDefaultPage('index_html')
    # Now the content rules
    assignable, storage, path = IRuleAssignmentManager(obj), getUtility(IRuleStorage), '/'.join(obj.getPhysicalPath())
    for ruleName in ('cb-add-event', 'cb-mod-event', 'cb-pub-event'):
        if ruleName not in assignable:
            assignable[ruleName] = RuleAssignment(ruleName)
            get_assignments(storage[ruleName]).insert(path)
        