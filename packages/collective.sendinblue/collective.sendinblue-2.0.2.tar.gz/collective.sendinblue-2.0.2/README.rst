=====================
collective.sendinblue
=====================


This package provides Sendinblue_ integration for `Plone`_.

It allows you to link your Plone site to your Sendinblue account via a new configuration section.
Then, you can add a portlet to allow visitors to subscribe to one of your list (you can choose which one).
You can also add a portlet to simply redirect the user to your own Sendinblue subscription form (it will append user's email to your base url).

Version 2.x are tested with Plone 5.2.x & Plone 6.0.

Version 1.x are tested with Plone 4.3.x.
The versions build from the branch 1.x will stay compatible with Plone 4.3.x.
Please note that they do not provide the full functionality (no redirection portlet & use of deprecated Sendinblue v2 API).


Features
--------

- multiple accounts / lists support : you can link more than one Sendinblue account to your site
- archive link : you can provide an URL that points to archives (that you manage manually)
- optional reCaptcha on subscription portlet (not on redirection portlet) to avoid spammers


Translations
------------

This product has been translated into

- English

- French.

- Spanish.

You can contribute for any message missing or other new languages, join us at 
`Plone Collective Team <https://www.transifex.com/plone/plone-collective/>`_ 
into *Transifex.net* service with all world Plone translators community.


Installation
------------

Install ``collective.sendinblue`` by adding it to your buildout: ::

    [buildout]

    ...

    eggs =
        collective.sendinblue


and then running ``bin/buildout``


Tests status
============

This add-on is tested using Travis CI. The current status of the add-on is:

.. image:: https://img.shields.io/travis/collective/collective.sendinblue/master.svg
    :target: https://travis-ci.org/collective/collective.sendinblue

.. image:: http://img.shields.io/pypi/v/collective.sendinblue.svg
   :target: https://pypi.org/project/collective.sendinblue


Contribute
==========

Have an idea? Found a bug? Let us know by `opening a ticket`_.

- Issue Tracker: https://github.com/collective/collective.sendinblue/issues
- Source Code: https://github.com/collective/collective.sendinblue


To do
-----

- Add more tests
- If a Plone user is connected, use his email address to populate subscription portlet (default value)
- If a Plone user is connected, change the portlet form to a text if he's already subscribed


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.sendinblue/issues
- Source Code: https://github.com/collective/collective.sendinblue


License
-------

The project is licensed under the GPLv2.

.. _Sendinblue: https://sendinblue.com
.. _Plone: https://plone.org/
.. _`opening a ticket`: https://github.com/collective/collective.sendinblue/issues
