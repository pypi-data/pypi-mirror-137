=========
Migration
=========

Below is a list of caveats when migrating from Bootstrap3/django-bootstrap3 to Bootstrap4/django-bootstrap4.

This document only considers the differences between django-bootstrap4 and django-bootstrap-v5. For the migration
guide from Bootstrap 4 to 5, please look at the Bootstrap docs, especially the `Migration section <https://getbootstrap.com/docs/5.0/migration/>`_.

Icons
-----

Bootstrap 5 reversed the course on icons and they now publish their own extension pack. At the moment you will need to install it
manually via npm.  More details can be found on their web page: https://getbootstrap.com/docs/5.0/extend/icons/

JQuery
------

Bootstrap 5 does not need JQuery anymore. Therefore, django-bootstrap-v5 has removed all references to the library. It
won't be included in the output from {% bootstrap_javascript %}.  If your code relies on JQuery for other purposes,
you will need to include it manually.