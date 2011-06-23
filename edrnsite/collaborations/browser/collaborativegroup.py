# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''EDRN Site Collaborations: collaborative group view
'''

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class CollaborativeGroupView(BrowserView):
    '''Default view for a Collaborative Group.'''
    index = ViewPageTemplateFile('templates/collaborativegroup.pt')
