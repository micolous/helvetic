# helvetic #

*helvetic* is an application that replaces the web service for the FitBit Aria.

The software is a work-in-progress, and runs as a Django application.  It also includes a bare-bones implementation of the protocol for testing, which uses bottle.py (and stores no data).

It requires local DNS spoofing in order to intercept requests originally bound for `fitbit.com`.

## Currently implemented ##

* Recording data
* Sending preferences and user profiles to Aria

## Partially implemented ##

* Registering new device
* Viewing data (through Django Admin)
* Configuration manager (through Django Admin)
* Profile manager (through Django Admin)

## Planned ##

* WiFi connection setup & complete registration flow
* Replacing bits that depend on Django Admin
* User management
* Data access
* Graphs

## See also ##

* `protocol.md` - Contains information about the FitBit Aria protocol (version 3)
* `gfit.md` - Plans/notes on implementing [Google Fit](https://fit.google.com) support

