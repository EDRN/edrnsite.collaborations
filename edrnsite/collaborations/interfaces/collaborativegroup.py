# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Interface for a collaborative group'''

from edrnsite.collaborations import PackageMessageFactory as _
from zope import schema
from zope.app.container.constraints import contains
from zope.interface import Interface

class ICollaborativeGroup(Interface):
    '''A collaborative group serves the needs of those working towards a common goal.'''
    contains('edrnsite.collaborations.interfaces.ICollaborativeGroupIndex')
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'The name of this collaborative group.'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of this group.'),
        required=False,
    )
    updateNotifications = schema.Bool(
        title=_(u'Update Notifications'),
        description=_(u'Enable notifying members (by email) of updates to this collaborative group.'),
        required=False,
    )
    
    