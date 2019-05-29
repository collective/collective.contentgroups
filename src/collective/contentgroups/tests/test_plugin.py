# -*- coding: utf-8 -*-
from collective.contentgroups import testing
from collective.contentgroups.config import PLUGIN_ID
from Products.PlonePAS.plugins.ufactory import PloneUser

import unittest


class PluginEmptyTestCase(unittest.TestCase):
    """Test our plugin without any groups."""

    layer = testing.COLLECTIVE_CONTENT_GROUPS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.plugin = self.portal.acl_users[PLUGIN_ID]

    def _makeUser(self, userid="who"):
        # Create a transient/temporary user (much like our GroupAdapter is transient/temporary).
        return PloneUser(userid)

    def test_enumerateGroups_empty(self):
        self.assertTupleEqual(self.plugin.enumerateGroups(), ())

    def test_get_single_group_brain_empty(self):
        self.assertIsNone(self.plugin._get_single_group_brain("who"))

    def test_getGroupsForPrincipal_empty(self):
        user = self._makeUser()
        self.assertTupleEqual(self.plugin.getGroupsForPrincipal(user), ())

    def test_getGroupById_empty(self):
        self.assertIsNone(self.plugin.getGroupById("who"))
        marker = object()
        self.assertEqual(self.plugin.getGroupById("who", marker), marker)

    def test_getGroups_empty(self):
        self.assertTupleEqual(self.plugin.getGroups(), ())

    def test_getGroupIds_empty(self):
        self.assertTupleEqual(self.plugin.getGroupIds(), ())

    def test_getGroupMembers_empty(self):
        self.assertTupleEqual(self.plugin.getGroupMembers("who"), ())
