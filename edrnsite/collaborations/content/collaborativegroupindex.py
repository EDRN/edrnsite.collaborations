# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.


'''Collaborative Group index implementation'''

from edrnsite.collaborations import PackageMessageFactory as _
from edrnsite.collaborations.config import PROJECTNAME
from edrnsite.collaborations.interfaces import ICollaborativeGroupIndex
from Products.Archetypes import atapi
from Products.ATContentTypes.content import base, schemata
from zope.interface import implements

CollaborativeGroupIndexSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    atapi.ReferenceField(
        'members',
        storage=atapi.AnnotationStorage(),
        enforceVocabulary=True,
        multiValued=True,
        vocabulary_factory=u'eke.site.People',
        relationship='membersOfThisGroup',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            title=_(u'Members'),
            description=_(u'Members of this collaborative group.'),
        )
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
            label=_(u'Biomarkers'),
            description=_(u'Biomarkers of which this collaborative group is fond.'),
        ),
    ),
    atapi.ReferenceField(
        'protocols',
        storage=atapi.AnnotationStorage(),
        enforceVocabulary=True,
        multiValued=True,
        vocabulary_factory=u'eke.study.ProtocolsVocabulary',
        relationship='protocolsExecutedByThisGroup',
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
CollaborativeGroupIndexSchema['title'].storage = atapi.AnnotationStorage()
CollaborativeGroupIndexSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(CollaborativeGroupIndexSchema, folderish=False, moveDiscussion=True)

class CollaborativeGroupIndex(base.ATCTContent):
    '''A collaborative group'''
    implements(ICollaborativeGroupIndex)
    schema      = CollaborativeGroupIndexSchema
    portal_type = 'Collaborative Group Index'
    biomarkers  = atapi.ATReferenceFieldProperty('biomarkers')
    datasets    = atapi.ATReferenceFieldProperty('datasets')
    description = atapi.ATFieldProperty('description')
    members     = atapi.ATReferenceFieldProperty('members')
    projects    = atapi.ATReferenceFieldProperty('projects')
    protocols   = atapi.ATReferenceFieldProperty('protocols')
    title       = atapi.ATFieldProperty('title')

atapi.registerType(CollaborativeGroupIndex, PROJECTNAME)
