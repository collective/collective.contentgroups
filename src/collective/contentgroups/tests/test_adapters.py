# -*- coding: utf-8 -*-
from collective.contentgroups.adapters import GroupAdapter
from Products.PlonePAS.plugins.ufactory import PloneUser

import unittest


class DummyGroup(object):
    def __init__(self, id, title=None, users=""):
        self.id = id
        if title is None:
            self.title = id.capitalize()
        else:
            self.title = title
        self.users = users

    def Title(self):
        return self.title


class GroupAdapterUnitTestCase(unittest.TestCase):
    """Test our GroupAdapter without Plone integration, using a dummy group."""

    def _makeGroup(self, groupid="group1", title=None):
        return DummyGroup(groupid, title=title)

    def _makeAdapter(self, group=None):
        if group is None:
            group = self._makeGroup()
        return GroupAdapter(group)

    def _makeUser(self, userid="who"):
        # Create a transient/temporary user (much like our GroupAdapter is transient/temporary).
        return PloneUser(userid)

    def test_getId(self):
        adapter = self._makeAdapter()
        self.assertEqual(adapter.getId(), "group1")

    def test_getMemberIds_empty(self):
        adapter = self._makeAdapter()
        with self.assertRaises(NotImplementedError):
            # default argument transitive=1 is not supported for now
            adapter.getMemberIds()
        self.assertListEqual(adapter.getMemberIds(transitive=0), [])

    def test_getMemberIds_filled(self):
        group = self._makeGroup()
        group.users = "arthur\n\n\nbetty"
        adapter = self._makeAdapter(group)
        with self.assertRaises(NotImplementedError):
            # default argument transitive=1 is not supported for now
            adapter.getMemberIds()
        self.assertListEqual(adapter.getMemberIds(transitive=0), ["arthur", "betty"])

    def test_getRolesInContext(self):
        adapter = self._makeAdapter()
        context = object()
        self.assertListEqual(adapter.getRolesInContext(context), [])

    def test_allowed(self):
        adapter = self._makeAdapter()
        context = object()
        self.assertEqual(adapter.allowed(context), 0)

    def test_isGroup(self):
        adapter = self._makeAdapter()
        self.assertTrue(adapter.isGroup())

    def test_getUserId(self):
        adapter = self._makeAdapter()
        self.assertEqual(adapter.getUserId(), "group1")

    def test_getUserName(self):
        adapter = self._makeAdapter()
        self.assertEqual(adapter.getUserName(), "group1")

    def test_getUserRoles(self):
        adapter = self._makeAdapter()
        self.assertListEqual(adapter.getRoles(), [])

    def test_getDomains(self):
        adapter = self._makeAdapter()
        self.assertListEqual(adapter.getDomains(), [])

    def test_getGroups(self):
        adapter = self._makeAdapter()
        self.assertListEqual(adapter.getGroups(), [])

    def test_addGroups(self):
        adapter = self._makeAdapter()
        self.assertListEqual(adapter.getGroups(), [])
        adapter._addGroups([])
        self.assertListEqual(adapter.getGroups(), [])
        # list is good
        adapter._addGroups(["birds"])
        self.assertListEqual(adapter.getGroups(), ["birds"])
        # tuple is good
        adapter._addGroups(("pelicans", "penguins"))
        self.assertListEqual(adapter.getGroups(), ["birds", "pelicans", "penguins"])
        # set is good
        adapter._addGroups(set(["eagles"]))
        self.assertListEqual(
            adapter.getGroups(), ["birds", "eagles", "pelicans", "penguins"]
        )
        # duplicates are fine
        adapter._addGroups(("birds", "penguins", "eagles"))
        self.assertListEqual(
            adapter.getGroups(), ["birds", "eagles", "pelicans", "penguins"]
        )

    def test_addRoles(self):
        adapter = self._makeAdapter()
        self.assertListEqual(adapter.getRoles(), [])
        adapter._addRoles([])
        self.assertListEqual(adapter.getRoles(), [])
        # list is good
        adapter._addRoles(["Editor"])
        self.assertListEqual(adapter.getRoles(), ["Editor"])
        # tuple is good
        adapter._addRoles(("cook", "Manager"))
        self.assertListEqual(adapter.getRoles(), ["Editor", "Manager", "cook"])
        # set is good
        adapter._addRoles(set(["foodie"]))
        self.assertListEqual(
            adapter.getRoles(), ["Editor", "Manager", "cook", "foodie"]
        )
        # duplicates are fine
        adapter._addRoles(("cook", "Editor"))
        self.assertListEqual(
            adapter.getRoles(), ["Editor", "Manager", "cook", "foodie"]
        )

    def test_setProperties(self):
        # We do not support this method.
        adapter = self._makeAdapter()
        with self.assertRaises(NotImplementedError):
            adapter.setProperties(properties={"email": "oops@example.org"})
        with self.assertRaises(NotImplementedError):
            adapter.setProperties(email="oops@example.org")
        # But if nothing is set, it is not useful to complain.
        adapter.setProperties()

    def test_getProperty(self):
        # only title is available as property
        adapter = self._makeAdapter()
        self.assertEqual(adapter.getProperty("title"), "Group1")
        self.assertIsNone(adapter.getProperty("email"))
        self.assertEqual(adapter.getProperty("email", "default"), "default")

    def test_getProperties(self):
        adapter = self._makeAdapter()
        self.assertDictEqual(adapter.getProperties(), {"title": "Group1"})

    def test_getGroupId(self):
        adapter = self._makeAdapter()
        self.assertEqual(adapter.getGroupId(), "group1")

    def test_getMemberId(self):
        adapter = self._makeAdapter()
        self.assertEqual(adapter.getMemberId(), "group1")

    def test_getGroupName(self):
        adapter = self._makeAdapter()
        self.assertEqual(adapter.getGroupName(), "group1")

    def test_getGroupMembers_empty(self):
        # Note: we cannot test this with a group that has users,
        # because then we need the portal, which is not available in this test case.
        # We need an integration test for that.
        adapter = self._makeAdapter()
        self.assertListEqual(adapter.getGroupMembers(), [])

    def test_getAllGroupMembers_empty(self):
        # Same remark as in test_getGroupMembers_empty:
        # we can only test this with an empty group in this test case
        adapter = self._makeAdapter()
        self.assertListEqual(adapter.getAllGroupMembers(), [])

    def test_addMember(self):
        adapter = self._makeAdapter()
        with self.assertRaises(NotImplementedError):
            # not supported through the controlpanel UI
            adapter.addMember("fluffy")

    def test_removeMember(self):
        adapter = self._makeAdapter()
        with self.assertRaises(NotImplementedError):
            # not supported through the controlpanel UI
            adapter.removeMember("fluffy")

    def test_getGroup(self):
        group = self._makeGroup()
        adapter = self._makeAdapter(group)
        self.assertEqual(adapter.getGroup(), group)

    def test_getGroupTitleOrName(self):
        adapter = self._makeAdapter()
        self.assertEqual(adapter.getGroupTitleOrName(), "Group1")
        group = self._makeGroup(groupid="one", title="")
        adapter = self._makeAdapter(group)
        self.assertEqual(adapter.getGroupTitleOrName(), "one")
        # Setting the title afterwards does not help, unless you create the adapter again.
        group.title = "Two"
        self.assertEqual(adapter.getGroupTitleOrName(), "one")
        adapter = self._makeAdapter(group)
        self.assertEqual(adapter.getGroupTitleOrName(), "Two")

    def test_setGroupProperties(self):
        # We do not support this method.
        adapter = self._makeAdapter()
        with self.assertRaises(NotImplementedError):
            adapter.setGroupProperties({"email": "oops@example.org"})
        # But if nothing is set, it is not useful to complain.
        adapter.setGroupProperties({})

    def test_canDelete(self):
        adapter = self._makeAdapter()
        self.assertFalse(adapter.canDelete())

    def test_canPasswordSet(self):
        adapter = self._makeAdapter()
        self.assertFalse(adapter.canPasswordSet())

    def test_passwordInClear(self):
        adapter = self._makeAdapter()
        self.assertFalse(adapter.passwordInClear())

    def test_canWriteProperty(self):
        adapter = self._makeAdapter()
        self.assertFalse(adapter.canWriteProperty("title"))
