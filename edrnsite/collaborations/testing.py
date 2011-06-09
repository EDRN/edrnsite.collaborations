# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from eke.ecas.testing import EKE_ECAS_FIXTURE
from eke.knowledge.testing import EKE_KNOWLEDGE_FIXTURE
from eke.biomarker.testing import EKE_BIOMARKER_FIXTURE
from eke.study.testing import EKE_STUDY_FIXTURE
from plone.app.testing import PloneSandboxLayer, IntegrationTesting, FunctionalTesting
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.testing import z2
from zope.publisher.browser import TestRequest
from zope.component import getMultiAdapter
from plone.app.testing import login
from plone.app.testing import setRoles

class EDRNSiteCollaborations(PloneSandboxLayer):
    defaultBases = (EKE_ECAS_FIXTURE, EKE_BIOMARKER_FIXTURE, EKE_STUDY_FIXTURE, EKE_KNOWLEDGE_FIXTURE,)
    def setUpZope(self, app, configurationContext):
        import edrnsite.collaborations
        self.loadZCML(package=edrnsite.collaborations)
        z2.installProduct(app, 'edrnsite.collaborations')
    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'edrnsite.collaborations:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        organs = portal[portal.invokeFactory(
            'Knowledge Folder', 'basic-body-systems', title=u'Organs', rdfDataSource=u'testscheme://localhost/bodysystems/b'
        )]
        resources = portal[portal.invokeFactory(
            'Knowledge Folder', 'basic-resources', title=u'Resources', rdfDataSource=u'testscheme://localhost/resources/b'
        )]
        protocols = portal[portal.invokeFactory(
            'Study Folder', 'protocols', title=u'Protocols', rdfDataSource=u'testscheme://localhost/protocols/a'
        )]
        biomarkers = portal[portal.invokeFactory(
            'Biomarker Folder', 'biomarkers', title=u'Biomarkers', rdfDataSource=u'testscheme://localhost/biomarkers/a',
            bmoDataSource=u'testscheme://localhost/biomarkerorgans/a'
        )]
        datasets = portal[portal.invokeFactory(
            'Dataset Folder', 'datasets', title=u'Datasets', rdfDataSource=u'testscheme://localhost/datasets/a',
        )]
        sites = portal[portal.invokeFactory(
            'Site Folder', 'sites', title=u'Sites',
            rdfDataSource=u'testscheme://localhost/sites/d', peopleDataSource=u'testscheme://localhost/people/many'
        )]
        for folder in (organs, resources, protocols, biomarkers, datasets, sites):
            ingestor = getMultiAdapter((folder, TestRequest()), name=u'ingest')
            ingestor.render = False
            ingestor()
        protocol = protocols['ps-public-safety']
        protocol.project = True
        protocol.reindexObject(idxs=['project'])
    def tearDownZope(self, app):
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
