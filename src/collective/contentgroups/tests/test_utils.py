# -*- coding: utf-8 -*-
import unittest


class DummyGroup(object):
    def __init__(self, id, users=""):
        self.id = id
        self.users = users


class UtilsUnitTestCase(unittest.TestCase):
    """Test our utility functions."""

    def _makeGroup(self, groupid="group1", users=""):
        return DummyGroup(groupid, users=users)

    def test_list_users(self):
        from collective.contentgroups.utils import list_users

        self.assertListEqual(list_users(None), [])
        self.assertListEqual(list_users(self._makeGroup()), [])
        self.assertListEqual(list_users(self._makeGroup(users="joe")), ["joe"])
        self.assertListEqual(list_users(self._makeGroup(users="   joe \n   ")), ["joe"])
        self.assertListEqual(
            list_users(self._makeGroup(users="joe\njane")), ["jane", "joe"]
        )
        self.assertListEqual(
            list_users(self._makeGroup(users="\n  \r\n\tjoe\t\n\rjane\n")),
            ["jane", "joe"],
        )

    def test_find_all_groups_for_principal_id(self):
        from collective.contentgroups.utils import (
            find_all_groups_for_principal_id as fg,
        )

        # This simply works with a mapping (dict) and a principal id.
        self.assertListEqual(fg({}, ""), [])
        self.assertListEqual(fg({}, "joe"), [])
        self.assertListEqual(fg({"group": ["joe", "jane"]}, "joe"), ["group"])
        self.assertListEqual(fg({"group": ["joe", "jane"]}, "jane"), ["group"])
        self.assertListEqual(fg({"group": ["joe", "jane"]}, "john"), [])

        # Now try with sub groups.
        groups = {
            "subsub1": ["ss1"],
            "subsub2": ["ss2"],
            "sub": ["s", "subsub1", "subsub2"],
            "overall": ["sub"],
        }
        self.assertListEqual(fg(groups, "overall"), [])
        self.assertListEqual(fg(groups, "sub"), ["overall"])
        self.assertListEqual(fg(groups, "s"), ["overall", "sub"])
        self.assertListEqual(fg(groups, "subsub1"), ["overall", "sub"])
        self.assertListEqual(fg(groups, "subsub2"), ["overall", "sub"])
        self.assertListEqual(fg(groups, "ss1"), ["overall", "sub", "subsub1"])
        self.assertListEqual(fg(groups, "ss2"), ["overall", "sub", "subsub2"])

        # I guess you can add group1 to group2 and the other way around.
        # Our logic should not break then, or end up in an infinite loop.
        groups = {"a": "b", "b": "a"}
        self.assertListEqual(fg(groups, "joe"), [])
        self.assertListEqual(fg(groups, "a"), ["b"])
        self.assertListEqual(fg(groups, "b"), ["a"])
        # Check a circle of four.
        groups = {"a": "b", "b": "c", "c": "d", "d": "a"}
        self.assertListEqual(fg(groups, "joe"), [])
        self.assertListEqual(fg(groups, "a"), ["b", "c", "d"])
        self.assertListEqual(fg(groups, "b"), ["a", "c", "d"])
        self.assertListEqual(fg(groups, "c"), ["a", "b", "d"])
        self.assertListEqual(fg(groups, "d"), ["a", "b", "c"])
