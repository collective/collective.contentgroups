# -*- coding: utf-8 -*-
from collective.contentgroups import testing
from collective.contentgroups.adapters import GroupAdapter
from collective.contentgroups.config import PLUGIN_ID
from plone import api
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


class PluginWithGroupsTestCase(unittest.TestCase):
    """Test our plugin with groups."""

    layer = testing.COLLECTIVE_CONTENT_GROUPS_CREATED_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.plugin = self.portal.acl_users[PLUGIN_ID]

    def test_enumerateGroups(self):
        self.assertTupleEqual(
            self.plugin.enumerateGroups(),
            (
                {"id": "content1", "pluginid": "contentgroups", "title": "Content 1"},
                {"id": "content2", "pluginid": "contentgroups", "title": "Content 2"},
                {"id": "sub2a", "pluginid": "contentgroups", "title": "2A Sub Content"},
                {"id": "sub2b", "pluginid": "contentgroups", "title": "2B Sub Content"},
            ),
        )
        # max_results is not passed to the plugin by PAS, but it is part of the interface,
        # so let's test it
        self.assertTupleEqual(
            self.plugin.enumerateGroups(max_results=2),
            (
                {"id": "content1", "pluginid": "contentgroups", "title": "Content 1"},
                {"id": "content2", "pluginid": "contentgroups", "title": "Content 2"},
            ),
        )
        # sort_by is not passed to the plugin by PAS, but it is part of the interface,
        # so let's test it
        self.assertTupleEqual(
            self.plugin.enumerateGroups(sort_by="title"),
            (
                {"id": "sub2a", "pluginid": "contentgroups", "title": "2A Sub Content"},
                {"id": "sub2b", "pluginid": "contentgroups", "title": "2B Sub Content"},
                {"id": "content1", "pluginid": "contentgroups", "title": "Content 1"},
                {"id": "content2", "pluginid": "contentgroups", "title": "Content 2"},
            ),
        )
        # Combine them
        self.assertTupleEqual(
            self.plugin.enumerateGroups(sort_by="title", max_results=3),
            (
                {"id": "sub2a", "pluginid": "contentgroups", "title": "2A Sub Content"},
                {"id": "sub2b", "pluginid": "contentgroups", "title": "2B Sub Content"},
                {"id": "content1", "pluginid": "contentgroups", "title": "Content 1"},
            ),
        )

    def test_get_single_group_brain(self):
        self.assertEqual(
            self.plugin._get_single_group_brain("content1").getPath(), "/plone/content1"
        )
        self.assertEqual(
            self.plugin._get_single_group_brain("sub2a").getPath(), "/plone/sub2a"
        )

    def test_getGroupsForPrincipal(self):
        # Note that our plugin only reports on content groups, not standard groups.
        self.assertTupleEqual(
            self.plugin.getGroupsForPrincipal(api.user.get("casual-ann")), ()
        )
        self.assertTupleEqual(
            self.plugin.getGroupsForPrincipal(api.user.get("content1-corey")),
            ("content1",),
        )
        self.assertTupleEqual(
            self.plugin.getGroupsForPrincipal(api.user.get("sub2a-eddy")), ("sub2a",)
        )
        self.assertTupleEqual(
            self.plugin.getGroupsForPrincipal(api.user.get("general")),
            ("content1", "content2", "sub2a", "sub2b"),
        )

    def test_getGroupById(self):
        self.assertIsNone(self.plugin.getGroupById("casual"))
        group = self.plugin.getGroupById("content1")
        self.assertIsInstance(group, GroupAdapter)
        self.assertEqual(group.getGroupId(), "content1")
        group = self.plugin.getGroupById("sub2a")
        self.assertIsInstance(group, GroupAdapter)
        self.assertEqual(group.getGroupId(), "sub2a")

    def test_getGroups(self):
        groups = self.plugin.getGroups()
        self.assertEqual(len(groups), 4)
        ids = []
        for group in groups:
            self.assertIsInstance(group, GroupAdapter)
            ids.append(group.getGroupId())
        self.assertListEqual(ids, ["content1", "content2", "sub2a", "sub2b"])

    def test_getGroupIds(self):
        self.assertTupleEqual(
            self.plugin.getGroupIds(), ("content1", "content2", "sub2a", "sub2b")
        )

    def test_getGroupMembers(self):
        self.assertTupleEqual(self.plugin.getGroupMembers("casual"), ())
        self.assertTupleEqual(self.plugin.getGroupMembers("subcasual"), ())
        self.assertTupleEqual(
            self.plugin.getGroupMembers("content1"), ("content1-corey", "general")
        )
        self.assertTupleEqual(
            self.plugin.getGroupMembers("content2"),
            ("content2-donna", "general", "sub2a", "sub2b"),
        )
        self.assertTupleEqual(
            self.plugin.getGroupMembers("sub2a"), ("general", "sub2a-eddy")
        )
        self.assertTupleEqual(
            self.plugin.getGroupMembers("sub2b"), ("general", "sub2b-fiona")
        )
