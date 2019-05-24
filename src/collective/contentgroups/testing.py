# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer

import collective.contentgroups


class ContentGroupsLayer(PloneSandboxLayer):
    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.contentgroups)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.contentgroups:default")


COLLECTIVE_CONTENT_GROUPS_FIXTURE = ContentGroupsLayer()


COLLECTIVE_CONTENT_GROUPS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_CONTENT_GROUPS_FIXTURE,),
    name="ContentGroupsLayer:IntegrationTesting",
)


COLLECTIVE_CONTENT_GROUPS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_CONTENT_GROUPS_FIXTURE,),
    name="ContentGroupsLayer:FunctionalTesting",
)
