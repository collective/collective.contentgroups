Using the development buildout
------------------------------

Create a virtualenv in the package::

    $ python3.8 -mvenv .

Install requirements with pip::

    $ ./bin/pip install -r requirements.txt

Run buildout for Plone 6::

    $ ./bin/buildout

or Plone 5.2:

    $ ./bin/buildout -c test-5.2.x.cfg

Start Plone in foreground:

    $ ./bin/instance fg

Run the tests in various versions in parallel:

    $ tox
