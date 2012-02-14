The fork situation
==================

The newest best maintained fork is at https://github.com/RobCombs/django-locking.

About this fork
===============

This fork adds numerous improvements to the admin integration of django-locking.
These improvements entails:

- It actually works.
- Media is included correctly.
- Adds new settings for specifying the timing of the locks.
- Warns the user that his lock is about to expire and offers to save the page
  for him.
- Informs the user that his lock is expired.
- Includes a test project.

New settings
============

The following two new settings are added::

	LOCKING = {
	    'time_until_warning': 15 * 60, # Seconds.
	    'time_until_expiration': 20 * 60, # Seconds.
	}

Trying it out
=============

The following command will clone this fork and run the test project::

    curl https://raw.github.com/runekaagaard/django-locking/master/test_proj/tryme.sh > tryme.sh && sh tryme.sh

Compatibility
=============

Works well with https://github.com/runekaagaard/django-admin-save-me-genie. If
you want to use django-extensions ModificationDateTimeField, see https://github.com/stdbrouw/django-locking/issues/6.