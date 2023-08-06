Change Log
==========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <http://keepachangelog.com/>`__
and this project adheres to `Semantic
Versioning <http://semver.org/>`__.

0.5.2
-----

Fixed
~~~~~

* Fixed issue with from_date (thanks to Sampath)

0.5.1
-----

Changed
~~~~~~~

-  Allow Django 4.0

0.5.0
-----

Added
~~~~~

-  Class method which gets the last week of a year

Fixed
~~~~~

-  Fix year detection at year turns

0.4.7
-----

Changed
~~~~~~~

-  Use default language from settings if language is not recognizable

0.4.6
-----

Changed
~~~~~~~

-  Don't add encondings in i18n functions

0.4.5
-----

Changed
~~~~~~~

-  Convert enums to lists for Django choices

0.4.4
-----

Changed
~~~~~~~

-  Leave empty locale unchanged when normalising

0.4.1
-----

Changed
~~~~~~~

-  Use system default encoding when normalising locale

0.4.0
-----

Added
~~~~~

-  Normalise locales

0.3.1
-----

Fixed
~~~~~

-  Fix a type cast for GET parameters

0.3.0
-----

Added
~~~~~

-  Allow passing first day of week to i18n_js
-  Allow passing locale to all functions

Fixed
~~~~~

-  Fix bug in month_names that still had the dummy first element

0.2.1
-----

Changed
~~~~~~~

-  Let JS function return a full script

0.2.0
-----

Added
~~~~~

-  Functions for month names and abbreviationss
-  JSON view for i18n

0.1.1
-----

Added
~~~~~

-  Provide functions for tuples and enumerations in i18n module
