# -*- coding: utf-8 -*-
from collective.contentgroups import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile import field as namedfile
from plone.supermodel import model
from Products.CMFPlone.utils import base_hasattr
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IGroup(model.Schema):
    """
    """

    users = namedfile.NamedBlobImage(
        title=_(u"users_field_title", default=u"Users"),
        description=_(u"users_field_description", default=u""),
        required=False,
    )


@implementer(IGroup)
@adapter(IDexterityContent)
class Group(object):
    def __init__(self, context):
        self.context = context

    @property
    def users(self):
        if base_hasattr(self.context, "users"):
            return self.context.users
        return None

    @users.setter
    def users(self, value):
        self.context.users = value
