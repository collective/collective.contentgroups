# -*- coding: utf-8 -*-
from collective.contentgroups.config import PLUGIN_ID
from collective.contentgroups.plugins import ContentGroupsPlugin
from zope.publisher.browser import TestRequest

import unittest


class BasePluginTestCase(unittest.TestCase):
    """Base test case class with a few helper methods."""

    def _make_plugin(self, request=None):
        plugin = ContentGroupsPlugin()
        plugin.id = PLUGIN_ID
        if request is None:
            request = TestRequest()
        plugin.REQUEST = request
        return plugin
