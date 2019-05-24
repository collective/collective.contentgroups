# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from Products.PluggableAuthService.interfaces import plugins
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements

import logging


logger = logging.getLogger("collective.contentgroups")


class ContentGroupsPlugin(BasePlugin):
    """PAS Plugin which handles groups as content.
    """

    meta_type = "ContentGroups Plugin"
    security = ClassSecurityInfo()


InitializeClass(ContentGroupsPlugin)
classImplements(ContentGroupsPlugin, plugins.IRolesPlugin)


def add_contentgroups_plugin():
    # Form for manually adding our plugin.
    # But we do this in setuphandlers.py always.
    pass
