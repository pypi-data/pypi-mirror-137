Changelog
=========


2.0.2 (2022-02-03)
------------------

- Migrate to Sendinblue API v3 (#4)
  Warning: old api keys will be cleared (because v2 keys are not compatible)
  [laulaz]


2.0.1 (2022-01-28)
------------------

- Make captcha use optional in subscription portlet (for a11y)
  [laulaz]

- Get rid of includeDependencies for Plone 6 compatibility
  [laulaz]

- Add Transifex.net service integration to manage the translation process
  [macagua]

- Added Spanish translation
  [macagua]

- Updated gettext files support
  [macagua]

- Add placeholder to email fields
  This allows you to hide field label if you want to
  [laulaz]


2.0 (2020-01-29)
----------------

- Add new redirection portlet (to use custom subscription form)
  [boulch, laulaz]

- Migrate to Plone 5 & drop Plone 4 support
  [boulch, laulaz]


1.0.4 (2020-01-29)
------------------

- Minor fixes & improvements
  [boulch, laulaz]

- Update buildout & packages to last Plone 4 version
  [laulaz]


1.0.3 (2018-08-23)
------------------

- Handle multiple lists for Sendinblue accounts
  [laulaz]


1.0.2 (2018-02-09)
------------------

- Add recaptcha field on subscription portlet
  [laulaz]


1.0.1 (2017-01-10)
------------------

- Fix typo in French
  [laulaz]

- Unpin Sendinblue (tested with 2.0.5.1)
  [laulaz]


1.0 (2016-11-25)
----------------

- Initial release.
  [laulaz]
