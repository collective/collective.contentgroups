# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from collective.contentgroups.interfaces import IGroupMarker
from plone import api
from Products.PlonePAS.interfaces import group as group_plugins
from Products.PluggableAuthService.interfaces import plugins as pas_plugins
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
          TODO: not supported yet

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
        if sort_by:
            logger.warning("Ignoring sort_by=%r argument to enumerateGroups.", sort_by)
        if kw:
            logger.warning("Ignoring keyword arguments %r to enumerateGroups.", kw)
        query = {"object_provides": IGroupMarker}
        if id:
            query["id"] = id
        groups = api.content.find(**query)
        results = []
        if max_results is not None:
            groups = groups[:max_results]
        for group in groups:
            results.append(
                {"id": group.getId, "pluginid": self.getId(), "title": group.Title}
            )
        return results

    def _get_single_group_brain(self, group_id):
        """Helper method to get the brain of a single group by id."""
        query = {"object_provides": IGroupMarker, "id": group_id}
        groups = api.content.find(**query)
        if not groups:
            return
        return groups[0]

    # Start of IGroupsPlugin

    def getGroupsForPrincipal(self, principal, request=None):
        """ principal -> (group_1, ... group_N)

        o Return a sequence of group names to which the principal
          (either a user or another group) belongs.

        o May assign groups based on values in the REQUEST object, if present
        """
        # TODO It may be nice for performance to store this somewhere, probably a BTree in a utility,
        # much like the redirection tool.
        groups = api.content.find(object_provides=IGroupMarker)
        principal_id = principal.getId()
        found = []
        for group in groups:
            obj = group.getObject()
            if not obj.users:
                continue
            if principal_id in obj.users.splitlines():
                found.append(obj.id)
        if found:
            logger.info(
                "getGroupsForPrincipal for {0} returned: {1}".format(principal, found)
            )
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
        brain = self._get_single_group_brain(group_id)
        if brain is None:
            return default
        group = group_plugins.IGroupData(brain.getObject(), None)
        if group is None:
            return default

        # Some of the next calls need a request, but it may be None.
        request = None

        # Determine the roles.
        pas = self._getPAS()
        plugins = pas._getOb("plugins")
        rolemakers = plugins.listPlugins(pas_plugins.IRolesPlugin)
        for rolemaker_id, rolemaker in rolemakers:
            roles = rolemaker.getRolesForPrincipal(group, request)
            if roles:
                group._addRoles(roles)
        group._addRoles(["Authenticated"])

        # TODO: should we fill _groups as well?  PloneGroup does not do this.
        groups = pas._getGroupsForPrincipal(group, request, plugins=plugins)
        if groups:
            group._addGroups(groups)

        # Apparently it may help if this is acquisition wrapped.
        # But our current GroupAdapter has no __of__ method, so maybe not.
        # return group.__of__(self)
        return group

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
        group = self._get_single_group_brain(group_id)
        if not group:
            return []
        users = group.getObject().users
        if not users:
            return []
        # This is (at least currently) a Text field.
        return users.splitlines()


InitializeClass(ContentGroupsPlugin)
classImplements(
    ContentGroupsPlugin,
    pas_plugins.IGroupEnumerationPlugin,
    pas_plugins.IGroupsPlugin,
    group_plugins.IGroupIntrospection,
)


def add_contentgroups_plugin():
    # Form for manually adding our plugin.
    # But we do this in setuphandlers.py always.
    pass
