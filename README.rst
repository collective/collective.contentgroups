.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi. It is a comment.

collective.contentgroups
========================

This is a PAS (``PluggableAuthenticationService``) plugin for Plone.
It supports content items as groups.

.. image:: https://travis-ci.org/collective/collective.contentgroups.svg?branch=master
    :target: https://travis-ci.org/collective/collective.contentgroups


Features
--------

- A behavior ``collective.contentgroups.group`` that turns a dexterity portal type into a group, with a simple ``users`` text field.
- A PAS plugin ``contentgroups`` that integrates these groups.
- An adapter ``GroupAdapter`` that gives content items with our behavior the needed functionality that the standard ``PloneGroup`` and ``GroupData`` objects provide.
- An installer that installs the plugin into ``acl_users``.
- An uninstaller to remove the plugin.

Note: this package has no Group portal type.
You will have to enable the behavior yourself on a new or existing dexterity portal type.


Installation
------------

Install collective.contentgroups by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.contentgroups


and then running ``bin/buildout`` and starting Plone.

Now you can install the product in the Add-ons control panel in Plone.
Then go to the Dexterity contenttypes control panel.
Either create a new type or edit an existing type and enable the Group behavior.


Usage
-----

Creating groups
~~~~~~~~~~~~~~~

Any groups that you add in the Users and Groups control panel, are standard Plone groups.

In the Content UI, you can create a Group, just like you would create a Page or Folder.
Use the Add New action menu and select the content type for which you have enabled the behavior.

Deleting groups is also done in the content UI: simply delete the Group like you would delete a Page.

Note that if the Group is private, a Site Adminstrator will see it in the Groups control panel.
But other users may not see the group.
Editors that have no permission to see the group, will not be able to select it in the Sharing tab.
A member of the group may not effectively get the group membership, because the group is not found (in the ``portal_catalog`` search).

In other words: setting a Group in the private state is an effective way to disable it.


Adding users
~~~~~~~~~~~~

Adding users to a group *must* be done on the edit form of the content group.
It *cannot* be done in the Users and Groups control panel.
In the Users text field, type the ids of users that you want in this group, one per line.

Note: you need the *id* of the user, not the login name.
Usually they are the same, but they may differ, for example when you use email as login.

It is also fine to add a group id in the users field, either from another content group or a standard Plone Group.
Such "recursive" group memberships work seemlessly when you use the Plone recursive groups plugin, which is enabled in default Plone.
For this to work, the ``contentgroups`` PAS plugin needs to be above the ``recursive_groups`` plugin in the ``IGroupsPlugin``.
The installer takes care of this.

To remove a user from the group, simply remove its id from the Users field.

In the Users and Groups control panel you will be able to see which users are in a content group and to which content groups a user belongs.
But you won't be able to change it.


Adding roles
~~~~~~~~~~~~

You cannot add roles to groups, not in the edit form and not in the control panel.
What you *can* do, is:

- Add the content group to a standard Plone group and give this standard group a role.
  For example, you can add the content group to the Reviewers group.
- Search and select the content group on the Sharing tab and give it a local role.


Compatibility
-------------

This works on Plone 5.2 with Python 2.7 and 3.6.
It probably works with earlier Plone versions or later Python versions too, but this has not been tested.


Support
-------

If you are having issues, please let us know.
Contact `Maurits van Rees at Zest Software <m.van.rees@zestsoftware.nl>`_.
Or open an issue in the `tracker <https://github.com/collective/collective.contentgroups/issues>`_.


License
-------

The project is licensed under the GPLv2.
