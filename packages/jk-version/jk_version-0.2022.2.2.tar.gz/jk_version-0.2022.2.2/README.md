jk_version
==========

Introduction
------------

This python module provides a version class. Instances of this class may be used in representing and version numbers and compare them.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/python-module-jk-version)
* [pypi.python.org](https://pypi.python.org/pypi/jk_version)

Why this module?
----------------

To manage data and software packages in a reasonable way versioning is important. For this you need to represent versions in computer memory.
This is what this module does: Provide version objects so that you can work with version information programmatically.
That's what this module has been written for.

Functionality
--------------------------

This module provides:

* `Version` - An object to represent version numbers in memory. (Parsing of version numbers is provided by this object as well.)
* Constraint classes that can be used to check versions:
	* `BaseVersionConstraint` - the abstract base class for all constraints
	* A set of concrete constraint classes: `VersionConstraint[GE|GT|LE|LT|NE|EQ|AND|OR]`

How to use this module
----------------------

### Import this module

Please include this module into your application using the following code:

```python
import jk_version
```

### Parse a version number

Version numbers can either be specified as lists of integers or as a string. Examples:

* `Version([ 1, 7, 51 ])`
* `Version(( 1, 7, 51 ))`
* `Version("1.7.51")`

### Version numbering schema

For compatibility reasons the version number parser is designed to accept the following schema:

*[ epoch ":" ] version_data [ "-" extra ]*

Where *epoch* is optional and - if present - must be an integer, and *version_data* is a regular version string consisting of decimal numbers separated by points.

Examples for valid version numbers:

* `0`
* `0.1`
* `0.1.2`
* `2020.12.24`
* `2:0.1.2`

An extra identifier is supported:

* `0.1.2-dev`
* `1.2.3-stable`
* `2.3.4-SNAPSHOT`
* `3.4.5-beta2`

### Comparing version numbers

Version numbers can be compared. Example:

```python
v1 = Version("0.1.2")
v2 = Version("0.2.0")
print(v2 > v1)
```

This will result in: `True`

**NOTE:** Please note that extra identifiers are stored in version objects but are ignored otherwise. If you require to compare two versions and this comparison must take this extra identifier into account you need to implement your own comparison function for this purpose. This is because of the fact that there is no general convention how this extra information can be processed.

Compatible Modules
-------------------

Version number parsers:
* [PHP `composer` version parser](https://github.com/jkpubsrc/python-module-jk-php-version-parser)

Contact Information
-------------------

This work is Open Source. This enables you to use this work for free.

Please have in mind this also enables you to contribute. We, the subspecies of software developers, can create great things. But the more collaborate, the more fantastic these things can become. Therefore Feel free to contact the author(s) listed below, either for giving feedback, providing comments, hints, indicate possible collaborations, ideas, improvements. Or maybe for "only" reporting some bugs:

* Jürgen Knauth: pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



