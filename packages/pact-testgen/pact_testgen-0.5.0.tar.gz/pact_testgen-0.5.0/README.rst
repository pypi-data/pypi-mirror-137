===================
Pact Test Generator
===================


.. image:: https://img.shields.io/pypi/v/pact-testgen.svg
        :target: https://pypi.python.org/pypi/pact-testgen

.. image:: https://img.shields.io/travis/pymetrics/pact-testgen.svg
        :target: https://travis-ci.com/pymetrics/pact-testgen

.. image:: https://readthedocs.org/projects/pact-testgen/badge/?version=latest
        :target: https://pact-testgen.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Generate Python test cases from Pact files, for easier provider verification.


* Free software: MIT license
* Documentation: https://pact-testgen.readthedocs.io.


Features
--------

* Test Pact contracts against your Python providers via unit tests. Get test isolation *for free*.
* ``pact-testgen`` creates test cases from your Pact files, with placeholders for defining provider states.


Getting Started
---------------

Install with pip
****************

::

    python -m pip install pact-testgen

Generate test files
*******************

Generate a ``provider_states.py`` and ``test_pact.py`` files in your tests directory:

::

    pact-testgen /path/to/pactfile.json /tests/dir

For more details, see the Usage section of the documentation.

Fill in the generated provider states file
******************************************

In your tests directory (passed as the second argument to ``pact-testgen``), you'll see a file named ``provider_states.py``. It will contain set up
functions matching the provider states defined in your pact file.

Before continuing, complete these functions so that they create the required states.

Run your tests
**************

Run your test suite as normal, being sure to check the the test runner has picked up
your new `test_pact.py` file.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

Logo `Admiranda Urbis Venetæ`_ from the British Library's King’s Topographical Collection.

Verification of test responses in generated test code is powered by pactman_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Admiranda Urbis Venetæ`: https://www.flickr.com/photos/britishlibrary/51196200069/
.. _`pactman`: https://github.com/reecetech/pactman
