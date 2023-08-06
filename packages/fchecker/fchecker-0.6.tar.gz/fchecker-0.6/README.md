fchecker
========

fchecker is designed to provide cleaner useable check exceptions. The "f" in fchecker represents formatted.

The purpose of fchecker is not to replace some of the built-in Python general checks but to act as a companion to enhance messages and increase issue resolution.

All check exceptions will return with no trackback from the checker. All tracing will get displayed from the caller line. Inspecting the original traceback will show all traces, but general usage and return output will not show any traces of the backend calls.

Returned exceptions are formatted using [fexception](https://pypi.org/project/fexception/). Import the required fexception exception classes for exception handling.

Description
===========

Python's general checks return True or False when a check result gets returned. fchecker removes the True or False return and throws a cleanly written exception when a check does not pass. fchecker checks many different Python checks and adds the ability to wrap a clean formatted structure around the returned exception.

Available Checks
================

Below are the listed check options. Some options are methods, and some are functions. Proper formatting is used to distinguish between the two. Please read the docstring for more details on usage requirements. 

| Import Name           | Method or Function | Checking      | Overview                                                                             |
| --------------------- |:------------------:|:-------------:|------------------------------------------------------------------------------------- |
| KeyCheck              | Method             | Dictionary    | An advanced dictionary key checker that offers two different check options.<br>&emsp;1. Checks if some required keys exist in the dictionary.<br>&emsp;2. Checks if all required keys exist in the dictionary.|
| type_check            | Function           | Type          | A simple type validation check.<br>Offers optional caller_override to change traceback.|
| file_check            | Function           | File          | Checks if the file exists.                                                           |

Installation
============

From PyPI
-------------------
You can find fchecker on PyPI. https://pypi.org/project/fchecker/ 

Usage
=====
Once installed, add fchecker as a module and select the checker option from the import.

Note: You can use * to import all check options.
