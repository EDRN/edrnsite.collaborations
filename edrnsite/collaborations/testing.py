# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from plone.app.testing import PloneSandboxLayer, PLONE_FIXTURE, IntegrationTesting, FunctionalTesting
from plone.testing import z2

class EDRNSiteCollaborations(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)
    def setUpZope(self, app, configurationContext):
        import edrnsite.collaborations
        self.loadZCML(package=edrnsite.collaborations)
        z2.installProduct(app, 'edrnsite.collaborations')
    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'edrnsite.collaborations:default')
    def teatDownZope(self, app):
        z2.uninstallProduct(app, 'edrnsite.collaborations')
    
EDRNSITE_COLLABORATIONS_FIXTURE = EDRNSiteCollaborations()
EDRNSITE_COLLABORATIONS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EDRNSITE_COLLABORATIONS_FIXTURE,),
    name='EDRNSiteCollaborations:Integration',
)
EDRNSITE_COLLABORATIONS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EDRNSITE_COLLABORATIONS_FIXTURE,),
    name='EDRNSiteCollaborations:Functional',
)
