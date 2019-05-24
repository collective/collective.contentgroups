.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi. It is a comment.

========================
collective.contentgroups
========================

This is a PAS (``PluggableAuthenticationService``) plugin for Plone.
It supports content items as groups.


Features
--------

- A behavior that makes a portal type a group.
- A PAS plugin that integrates these groups.
- An installer that installs the plugin into ``acl_users``.
- An uninstaller to remove the plugin.


Installation
------------

Install collective.contentgroups by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.contentgroups


and then running ``bin/buildout``.

Install the product in the Add-ons control panel in Plone.


Support
-------

If you are having issues, please let us know.
Contact Maurits van Rees at Zest Software, m.van.rees@zestsoftware.nl.
Or open an issue in the tracker.


License
-------

The project is licensed under the GPLv2.
