# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Interface for a collaborative group event'''

from Products.ATContentTypes.interfaces import IATEvent
from zope.app.container.constraints import contains

class ICollaborativeGroupEvent(IATEvent):
    '''A collaborative group event is like a regular Plone event but is also a container.'''
    contains('Protocols.ATContentTypes.interfaces.IATFile')
