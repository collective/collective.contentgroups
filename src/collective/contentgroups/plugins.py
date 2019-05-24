# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from collective.contentgroups.interfaces import IGroupMarker
from plone import api
from Products.PlonePAS.interfaces import group as group_plugins
from Products.PlonePAS.plugins.group import PloneGroup
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

    # Start of IGroupEnumerationPlugin

    def enumerateGroups(
        # C816 missing trailing comma in Python 3.6+, but black removes it
        self,
        id=None,
        exact_match=False,
        sort_by=None,
        max_results=None,
        **kw  # noqa C816
    ):

        """ -> (group_info_1, ... group_info_N)

        o Return mappings for groups matching the given criteria.

        o 'id' in combination with 'exact_match' true, will
          return at most one mapping per supplied ID ('id'
          may be a sequence).

        o If 'exact_match' is False, then 'id' may be treated by
          the plugin as "contains" searches (more complicated searches
          may be supported by some plugins using other keyword arguments).

        o If 'sort_by' is passed, the results will be sorted accordingly.
          known valid values are 'id' (some plugins may support others).

        o If 'max_results' is specified, it must be a positive integer,
          limiting the number of returned mappings.  If unspecified, the
          plugin should return mappings for all groups satisfying the
          criteria.

        o Minimal keys in the returned mappings:

          'id' -- (required) the group ID

          'pluginid' -- (required) the plugin ID (as returned by getId())

          'properties_url' -- (optional) the URL to a page for updating the
                              group's properties.

          'members_url' -- (optional) the URL to a page for updating the
                           principals who belong to the group.

        o Plugin *must* ignore unknown criteria.

        o Plugin may raise ValueError for invalid critera.

        o Insufficiently-specified criteria may have catastrophic
          scaling issues for some implementations.
        """
        if id or exact_match or sort_by or max_results or kw:
            logger.warning("Ignoring all arguments to enumerateGroups.")
        groups = api.content.find(object_provides=IGroupMarker)
        results = []
        for group in groups:
            results.append({"id": group.getId, "pluginid": self.getId()})
        return results

    # Start of IGroupsPlugin

    def getGroupsForPrincipal(self, principal, request=None):
        """ principal -> (group_1, ... group_N)

        o Return a sequence of group names to which the principal
          (either a user or another group) belongs.

        o May assign groups based on values in the REQUEST object, if present
        """
        # TODO It may be nice for performace to store this somewhere, probably a BTree in a utility,
        # much like the redirection tool.
        logger.warning("getGroupsForPrincipal for {0} ignored".format(principal))
        groups = api.content.find(object_provides=IGroupMarker)
        principal_id = principal.id
        found = []
        for group in groups:
            obj = group.getObject()
            if principal_id in obj.users:
                found.append(obj.id)
        return found

    # Start of IGroupIntrospection

    def getGroupById(self, group_id, default=None):
        """
        Returns the portal_groupdata-ish object for a group
        corresponding to this id.

        Taken over from Products.PlonePAS.plugins.group.
        """
        if group_id not in self.getGroupIds():
            return default
        plugins = self._getPAS()._getOb("plugins")
        return self._findGroup(plugins, group_id)

    def getGroups(self):
        """Returns an iteration of the available groups

        Taken over from Products.PlonePAS.plugins.group.
        """
        return [self.getGroupById(group_id) for group_id in self.getGroupIds()]

    def getGroupIds(self):
        """Returns a list of the available groups.
        """
        return [group["id"] for group in self.enumerateGroups()]

    def getGroupMembers(self, group_id):
        """
        return the members of the given group
        """
        groups = self.enumerateGroups(id=group_id)
        if not groups:
            return []
        group = groups[0]
        return group.getObject().users

    # group wrapping mechanics for IGroupIntrospection

    @security.private
    def _createGroup(self, plugins, group_id, name):
        """Create group object.

        Taken over from Products.PlonePAS.plugins.group.

        TODO: instead of PloneGroup, this should probably use
        content items: the found item with our behavior.
        """
        return PloneGroup(group_id, name).__of__(self)

    @security.private
    def _findGroup(self, plugins, group_id, title=None, request=None):
        """group_id -> decorated_group

        This method based on PluggableAuthService._findGroup
        Taken over from Products.PlonePAS.plugins.group.
        """
        group = self._createGroup(plugins, group_id, title)

        # propfinders = plugins.listPlugins(IPropertiesPlugin)
        # for propfinder_id, propfinder in propfinders:
        #     data = propfinder.getPropertiesForUser(group, request)
        #     if data:
        #         group.addPropertysheet(propfinder_id, data)

        # groups = self._getPAS()._getGroupsForPrincipal(group, request, plugins=plugins)
        # group._addGroups(groups)

        # rolemakers = plugins.listPlugins(IRolesPlugin)

        # for rolemaker_id, rolemaker in rolemakers:
        #     roles = rolemaker.getRolesForPrincipal(group, request)
        #     if roles:
        #         group._addRoles(roles)

        group._addRoles(["Authenticated"])

        return group.__of__(self)


InitializeClass(ContentGroupsPlugin)
classImplements(
    ContentGroupsPlugin,
    plugins.IGroupEnumerationPlugin,
    plugins.IGroupsPlugin,
    group_plugins.IGroupIntrospection,
)


def add_contentgroups_plugin():
    # Form for manually adding our plugin.
    # But we do this in setuphandlers.py always.
    pass
