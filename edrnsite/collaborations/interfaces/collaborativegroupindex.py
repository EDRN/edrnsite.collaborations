# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Interface for a collaborative group index'''

from edrnsite.collaborations import PackageMessageFactory as _
from eke.biomarker.interfaces import IBiomarker
from eke.ecas.interfaces import IDataset
from eke.study.interfaces import IProtocol
from eke.site.interfaces import IPerson
from zope import schema
from zope.interface import Interface

class ICollaborativeGroupIndex(Interface):
    '''A collaborative group index provides the view and discussion for a collaborative group.'''
    protocols = schema.List(
        title=_(u'Protocols & Studies'),
        description=_(u'Protocols and studies that are executed (and studied) by this collaborative group.'),
        required=False,
        value_type=schema.Object(
            title=_(u'Study'),
            description=_(u'A study or protocol executed (and studies) by this collaborative group.'),
            schema=IProtocol
        )
    )
    biomarkers = schema.List(
        title=_(u'Biomarkers'),
        description=_(u'Biomarkers of which this collaborative group is fond.'),
        required=False,
        value_type=schema.Object(
            title=_(u'Biomarker'),
            description=_(u'A biomarker of which this collaborative group is fond.'),
            schema=IBiomarker
        )
    )
    datasets = schema.List(
        title=_(u'Datasets'),
        description=_(u'Datasets of interest to this collaborative group.'),
        required=False,
        value_type=schema.Object(
            title=_(u'Dataset'),
            description=_(u'A dataset of interest to this collaborative group.'),
            schema=IDataset
        )
    )
    projects = schema.List(
        title=_(u'Projects'),
        description=_(u'Team projects (which are just special protocols) of which this collaborative group is part.'),
        required=False,
        value_type=schema.Object(
            title=_(u'Project'),
            description=_(u'Team project (which is just a special protocol) of which this collaborative group is part.'),
            schema=IProtocol
        )
    )
    chair = schema.Object(
        title=_(u'Chair'),
        description=_(u'The person in charge of this collaborative group.'),
        required=False,
        schema=IPerson
    )
    coChair = schema.Object(
        title=_(u'Co-Chair'),
        description=_(u'The assistant to the person in charge of this collaborative group.'),
        required=False,
        schema=IPerson
    )
    members = schema.List(
        title=_(u'Members'),
        description=_(u'Members of this collaborative group.'),
        required=False,
        value_type=schema.Object(
            title=_(u'Member'),
            description=_(u'A member of this collaborative group.'),
            schema=IPerson
        )
    )
