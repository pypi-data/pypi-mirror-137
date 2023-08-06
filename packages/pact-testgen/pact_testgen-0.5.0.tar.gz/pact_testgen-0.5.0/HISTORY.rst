=======
History
=======

0.5.0 (2022-02-04)
------------------

* Adds Pact Broker support.


0.4.3 (2021-09-20)
------------------

* Fix file handling for merge provider state file option.


0.4.2 (2021-09-18)
------------------

* Improve handling of request data.


0.4.1 (2021-09-17)
------------------

* Fix test method name missing `test_`.


0.4.0 (2021-09-16)
------------------

* Adds option to merge changes to provider state file (Python 3.9 only).
* Include structured provider state parameters from Pact v3 in provider
  state function names.
* Support null provider state, i.e. pact.given(None).


0.3.0 (2021-09-03)
------------------

* Provider state setup functions now raise NotImplementedError by default.
* Format output files with target line length option.
* Improve output to console, add quiet option.


0.2.1 (2021-09-01)
------------------

* Fix test client not setting content type.


0.2.0 (2021-09-01)
------------------

* Improve output for failed test cases.


0.1.2 (2021-08-25)
------------------

* Fix bump2version config


0.1.1 (2021-08-24)
------------------

* Fix templates missing from distributed package.


0.1.0 (2021-08-23)
------------------

* First release on PyPI.
