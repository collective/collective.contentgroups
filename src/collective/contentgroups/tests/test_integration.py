# -*- coding: utf-8 -*-
from collective.contentgroups import testing
from Products.PlonePAS.plugins.ufactory import PloneUser

import unittest


class IntegrationTestCase(unittest.TestCase):
    """Test how our plugin integrated in PAS."""

    layer = testing.COLLECTIVE_CONTENT_GROUPS_CREATED_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.pas = self.portal.acl_users

    def _makeUser(self, userid="general"):
        # Create a transient/temporary user (much like our GroupAdapter is transient/temporary).
        # Note that the "general" user is a member of all our extra groups.
        return PloneUser(userid)

    def test_searchGroups(self):
        # PAS.searchGroups looks for IGroupEnumerationPlugin plugins
        # and calls enumerateGroups on them with some keywords.
        # Without keyword arguments, we expect our groups plus Administrators, etc.
        groups = self.pas.searchGroups()
        self.assertGreaterEqual(len(groups), 10)
        ids = [g["groupid"] for g in groups]
        self.assertIn("Administrators", ids)
        self.assertIn("casual", ids)
        self.assertIn("content1", ids)
        # Strangely, max_results returns one result more than asked.
        self.assertEqual(len(self.pas.searchGroups(max_results=5)), 6)
        # Searching for name returns anything with content in the title,
        # so also our sub groups with 'Sub Content' in the title.
        self.assertEqual(len(self.pas.searchGroups(name="content")), 4)
        self.assertEqual(len(self.pas.searchGroups(name="sub content")), 2)
        # id is pickier:
        self.assertEqual(len(self.pas.searchGroups(id="content")), 0)
        self.assertEqual(len(self.pas.searchGroups(id="content1")), 1)
        self.assertEqual(len(self.pas.searchGroups(id="Content1")), 0)
        # We can have multiple ids though:
        self.assertEqual(len(self.pas.searchGroups(id=("content1", "sub2a"))), 2)
        # sort_by and max_results are not passed from PAS to the plugins,
        # but that seems wrong to me.  Let's test it anyway.
        groups = self.pas.searchGroups(name="content", sort_by="title", max_results=2)
        self.assertEqual(len(groups), 3)
        ids = [g["groupid"] for g in groups]
        self.assertListEqual(ids, ["sub2a", "sub2b", "content1"])

    def test_getGroupsForPrincipal(self):
        # PAS._getGroupsForPrincipal looks for IGroupsPlugin plugins
        # and calls_getGroupsForPrincipal on them with principal and request.
        general = self._makeUser()
        groups = self.pas._getGroupsForPrincipal(general)
        # Apparently the auto_group AuthenticatedUsers is always in there.
        self.assertListEqual(
            sorted(groups),
            [
                "AuthenticatedUsers",
                "casual",
                "content1",
                "content2",
                "sub2a",
                "sub2b",
                "subcasual",
            ],
        )
        self.assertListEqual(
            sorted(self.pas._getGroupsForPrincipal(self._makeUser("casual-ann"))),
            ["AuthenticatedUsers", "casual"],
        )
        self.assertListEqual(
            sorted(self.pas._getGroupsForPrincipal(self._makeUser("content1-corey"))),
            ["AuthenticatedUsers", "content1"],
        )
        # Bert is member of subcasual, which is sub group of casual.  Both non-content.
        self.assertListEqual(
            sorted(self.pas._getGroupsForPrincipal(self._makeUser("subcasual-bert"))),
            ["AuthenticatedUsers", "casual", "subcasual"],
        )
        # Does this work for our content groups too?
        # Eddy is a member of sub2a, and that is a sub group of content2.
        self.assertListEqual(
            sorted(self.pas._getGroupsForPrincipal(self._makeUser("sub2a-eddy"))),
            ["AuthenticatedUsers", "content2", "sub2a"],
        )
        # TODO Nope, not yet.
