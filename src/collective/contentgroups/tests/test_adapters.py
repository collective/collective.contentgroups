# -*- coding: utf-8 -*-
from collective.contentgroups.config import PLUGIN_ID
from collective.contentgroups.adapters import GroupAdapter
from Products.PlonePAS.plugins.ufactory import PloneUser

import unittest


class DummyGroup(object):

    def __init__(self, id, title=None, users=""):
        self.id = id
        self.title = title or id.capitalize()
        self.users = users

    def Title(self):
        return self.title


class BaseGroupAdapterTestCase(unittest.TestCase):
    """Base test case class with a few helper methods."""

    def _makeGroup(self, groupid="group1"):
        return DummyGroup(groupid)

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
        self.assertTupleEqual(adapter.getMemberIds(transitive=0), ())

    def test_getMemberIds_filled(self):
        group = self._makeGroup()
        group.users = "arthur\n\n\nbetty"
        adapter = self._makeAdapter(group)
        with self.assertRaises(NotImplementedError):
            # default argument transitive=1 is not supported for now
            adapter.getMemberIds()
        self.assertTupleEqual(adapter.getMemberIds(transitive=0), ("arthur", "betty"))

    def test_getRolesInContext(self):
        adapter = self._makeAdapter()
        context = object()
        self.assertTupleEqual(adapter.getRolesInContext(context), ())

    def test_allowed(self):
        adapter = self._makeAdapter()
        context = object()
        self.assertEqual(adapter.allowed(context), 0)
