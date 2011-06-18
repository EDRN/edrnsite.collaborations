# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from edrnsite.collaborations.testing import EDRNSITE_COLLABORATIONS_INTEGRATION_TESTING
from plone.app.contentrules.actions.mail import IMailAction
from plone.app.testing import TEST_USER_ID, setRoles
from plone.contentrules.engine.interfaces import IRuleStorage
from zope.component import getUtility
import unittest2 as unittest

_email = 'edrn-ic@jpl.nasa.gov'

class ContentRulesTest(unittest.TestCase):
    layer = EDRNSITE_COLLABORATIONS_INTEGRATION_TESTING
    def setUp(self):
        super(ContentRulesTest, self).setUp()
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.ruleStorage = getUtility(IRuleStorage)
    def testActiveRules(self):
        '''Ensure content rules are active'''
        self.failUnless(self.ruleStorage.active)
    def testAddEvent(self):
        '''Check the event trigger for adding items to a collaborative group'''
        e = self.ruleStorage['cb-add-event']
        self.assertEquals(u'EDRN Collaborations Event: Item Added', e.title)
        self.assertEquals(u'Event triggered when an item is added (created or pasted) to a Collaborative Group.', e.description)
        self.assertEquals(0, len(e.conditions))
        self.assertEquals(1, len(e.actions))
        a = e.actions[0]
        self.failUnless(IMailAction.providedBy(a))
        self.assertEquals(u'EDRN Collaborative Groups: new item added', a.subject)
        self.assertEquals(_email, a.recipients)
        self.failUnless(u'A new item has been added' in a.message)
    def testModifiedEvent(self):
        '''Verify the event trigger for modified items in a collaborative group'''
        e = self.ruleStorage['cb-mod-event']
        self.assertEquals(u'EDRN Collaborations Event: Item Modified', e.title)
        self.assertEquals(u'Event triggered when an item is modified (edited or altered) in a Collaborative Group.', e.description)
        self.assertEquals(0, len(e.conditions))
        self.assertEquals(1, len(e.actions))
        a = e.actions[0]
        self.failUnless(IMailAction.providedBy(a))
        self.assertEquals(u'EDRN Collaborative Groups: an item has been modified', a.subject)
        self.assertEquals(_email, a.recipients)
        self.failUnless(u'has been modified' in a.message)
    def testStateChangeEvent(self):
        '''Confirm the event trigger for when an item has its publication state adjusted'''
        e = self.ruleStorage['cb-pub-event']
        self.assertEquals(u'EDRN Collaborations Event: Publication State Changed', e.title)
        self.assertEquals(u"Event triggered when an item's publication state is changed in a Collaborative Group.", e.description)
        self.assertEquals(0, len(e.conditions))
        self.assertEquals(1, len(e.actions))
        a = e.actions[0]
        self.failUnless(IMailAction.providedBy(a))
        self.assertEquals(u'EDRN Collaborative Groups: publication state changed', a.subject)
        self.assertEquals(_email, a.recipients)
        self.failUnless(u'had its publication state changed' in a.message)

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
