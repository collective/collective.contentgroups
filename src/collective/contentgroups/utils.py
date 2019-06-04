# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import base_hasattr


def list_users(obj):
    if not base_hasattr(obj, "users"):
        return []
    users = obj.users
    if not users:
        return []
    return sorted(filter(None, [line.strip() for line in users.splitlines()]))


def _find_all_groups_for_principal_id(mapping, principal_id, found=None):
    """Find all group ids for the principal id.

    This includes recursive groups.
    This is only meant for content groups.
    The mapping is from content group id to a list of users.

    Note: this changes 'found' in place.
    This is to avoid infinite loops when groups contain each other in a circle.
    """
    if found is None:
        found = set()
    extra = set()
    for group_id, users in mapping.items():
        if principal_id in users and group_id not in found:
            extra.add(group_id)
            found.add(group_id)
    for group_id in extra:
        _find_all_groups_for_principal_id(mapping, group_id, found)
    return found


def find_all_groups_for_principal_id(mapping, principal_id):
    """Find all group ids for the principal id.

    This includes recursive groups.
    This is only meant for content groups.
    The mapping is from content group id to a list of users.
    """
    found = _find_all_groups_for_principal_id(mapping, principal_id)
    if principal_id in found:
        # When group a is in group b and b is in group a,
        # we should not report a as being in a.
        found.remove(principal_id)
    return sorted(found)
