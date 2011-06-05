# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Collaborative Group implementation'''

from edrnsite.collaborations import PackageMessageFactory as _
from edrnsite.collaborations.config import PROJECTNAME
from edrnsite.collaborations.interfaces import ICollaborativeGroup
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from zope.interface import implements

CollaborativeGroupSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.ReferenceField(
        'protocols',
        storage=atapi.AnnotationStorage(),
        enforceVocabulary=True,
        multiValued=True,
        vocabulary_factory=u'eke.study.ProtocolsVocabulary',
        relationship='protocolsExecutedByThisGroup',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Biomarkers'),
            description=_(u'Biomarkers of which this collaborative group is fond.'),
        ),
    ),
    atapi.ReferenceField(
        'biomarkers',
        storage=atapi.AnnotationStorage(),
        enforceVocabulary=True,
        multiValued=True,
        vocabulary_factory=u'eke.biomarker.BiomarkersVocabulary',
        relationship='biomarkersThisGroupLikes',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Protocols & Studies'),
            description=_(u'Protocols and studies that are executed (and studied) by this collaborative group.'),
        ),
    ),
    atapi.ReferenceField(
        'datasets',
        storage=atapi.AnnotationStorage(),
        enforceVocabulary=True,
        multiValued=True,
        vocabulary_factory=u'eke.ecas.DatasetsVocabulary',
        relationship='datasetsPreferredByThisGroup',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Datasets'),
            description=_(u'Datasets of interest to this collaborative group.'),
        ),
    ),
    atapi.ReferenceField(
        'projects',
        storage=atapi.AnnotationStorage(),
        enforceVocabulary=True,
        multiValued=True,
        vocabulary_factory=u'eke.study.TeamProjectsVocabulary',
        relationship='teamsThisGroupIsOn',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Projects'),
            description=_(u'Team projects (which are just special protocols) of which this collaborative group is part.'),
        ),
    ),
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
    protocols   = atapi.ATReferenceFieldProperty('protocols')
    biomarkers  = atapi.ATReferenceFieldProperty('biomarkers')
    datasets    = atapi.ATReferenceFieldProperty('datasets')
    projects    = atapi.ATReferenceFieldProperty('projects')

atapi.registerType(CollaborativeGroup, PROJECTNAME)
