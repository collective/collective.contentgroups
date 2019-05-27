# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from AccessControl.users import BasicUser


class GroupAdapter(BasicUser):
    """This adapts items with our group behavior to IGroupData from PlonePAS.

    The IGroupData interface says this "is an abstract interface for accessing
    properties on a group object."

    We may not want to fill in everything: we *could* support setting properties
    in the Users and Groups control panel, but this should just be done in the
    edit form of the Group itself.
    """

    # TODO check security.
    security = ClassSecurityInfo()

    def __init__(self, group):
        self.group = group
        self._id = group.id
        self._groups = {}
        self._roles = {}
        users = self.group.users
        if users:
            self._userids = tuple(filter(None, users.splitlines()))
        else:
            self._userids = []

    # from Products.PlonePAS.plugins.group.PloneGroup:

    def getId(self):
        """Return the string id of this group.

        This is from IBasicUser.
        """
        return self._id

    @security.private
    def getMemberIds(self, transitive=1):
        """Return member ids of this group, including or not
        transitive groups.
        """
        raise NotImplementedError

    @security.public
    def getRolesInContext(self, object):
        """Since groups can't actually log in, do nothing.
        """
        return []

    @security.public
    def allowed(self, object, object_roles=None):
        """Since groups can't actually log in, do nothing.
        """
        return 0

    # from Products.PlonePAS.plugins.ufactory.PloneUser:

    @security.public
    def isGroup(self):
        """Return 1/True if this user is a group abstraction."""
        return True

    @security.public
    def getName(self):
        """Get user's or group's name.
        This is the id. PAS doesn't do prefixes and such like GRUF.
        """
        return self.getId()

    @security.public
    def getUserId(self):
        """Get user's or group's name.
        This is the id. PAS doesn't do prefixes and such like GRUF.
        """
        return self.getId()

    # Next we need some methods from
    # Products.PluggableAuthService.PropertiedUser.PropertiedUser
    # which implements
    # Products.PluggableAuthService.interfaces.authservice.IPropertiedUser
    # But that is only for users that have property sheets associated,
    # implementing addPropertysheet, listPropertysheets, getPropertysheet.
    # We only need authservice.IBasicUser, which IPropertiedUser subclasses.

    def getUserName(self):
        """Return the name used by the user to log into the system.

        Groups do not login, but Plone needs this anyway.
        """
        return self.getId()

    def getRoles(self):
        """Return the roles assigned to a user "globally".

        The roles should have been added in plugins.py in getGroupById
        by calling group._addRoles.
        """
        return self._roles

    def getDomains(self):
        """Return the list of domain restrictions for a user."""
        raise NotImplementedError

    def getGroups(self):
        """Return the groups the user is in.

        This does not seem to be in any interface.
        But PropertiedUser has it, and RecursiveGroupsPlugin calls it.
        """
        return list(self._groups.keys())

    # PropertiedUser defines methods to allow user folder plugins to annotate the user.

    def _addGroups(self, groups=()):
        """Extend our set of groups.

        o Don't complain about duplicates.
        """
        for group in groups:
            self._groups[group] = 1

    def _addRoles(self, roles=()):
        """Extend our set of roles.

        o Don't complain about duplicates.
        """
        for role in roles:
            self._roles[role] = 1

    # IGroupData

    def setProperties(self, properties=None, **kw):
        """Allows setting of group properties en masse.
        Properties can be given either as a dict or a keyword parameters
        list"""
        raise NotImplementedError

    def getProperty(self, id):
        """Return the value of the property specified by 'id'."""
        if id == "title":
            return self.group.Title()
        raise KeyError

    def getProperties(self):
        """Return the properties of this group.

        Properties are as usual in Zope.
        """
        return {"title": self.group.Title()}

    def getGroupId(self):
        """Return the string id of this group, WITHOUT group prefix."""
        return self.getId()

    def getMemberId(self):
        """This exists only for a basic user/group API compatibility."""
        return self.getId()

    def getGroupName(self):
        """Return the name of the group.

        Plone seems to expect an id, not a title.
        """
        return self.getId()

    def getGroupMembers(self):
        """Return a list of the portal_memberdata-ish members of the group."""
        # TODO: the memberdata-ish part is the problem.
        # But we may copy some code from PlonePAS.
        raise NotImplementedError

    def getAllGroupMembers(self):
        """Return a list of the portal_memberdata-ish members of the group
        including transitive ones (ie. users or groups of a group in that
        group)."""
        raise NotImplementedError

    def getGroupMemberIds(self):
        """Return a list of the user ids of the group."""
        return self._userids

    def getAllGroupMemberIds(self):
        """ Return a list of the user ids of the group.
        including transitive ones (ie. users or groups of a group in that
        group)."""
        raise NotImplementedError

    def addMember(self, id):
        """ Add the existing member with the given id to the group"""
        raise NotImplementedError

    def removeMember(self, id):
        """ Remove the member with the provided id from the group """
        raise NotImplementedError

    def getGroup(self):
        """ Returns the actual group implementation.

        Varies by group implementation (GRUF/Nux/et al).
        """
        return self.group


InitializeClass(GroupAdapter)
