# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import base_hasattr


def list_users(obj):
    if not base_hasattr(obj, "users"):
        return []
    users = obj.users
    if not users:
        return []
    return sorted(filter(None, [line.strip() for line in users.splitlines()]))
