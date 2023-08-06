=====
Usage
=====


Generating test files
---------------------

Execute ``pact-testgen`` as follows:

::

    pact-testgen /path/to/pactfile.json /output/dir


The output directory should be in your tests directory, where your
test runner will pick it up.

Alternately, ``pact-testgen`` can retrieve a Pact contract from a Pact Broker.

This will create two files in the output directory:

1. A file named ``provider_states.py``. This will contain empty setup functions for each
   combination of provider states defined in the given pact file.

   Developers must edit this file, filling in the function bodies with whatever code is
   necessary to create the necessary states required by each function.

2. A file named ``test_pact.py``. This file contains unit tests which call out to the functions
   defined in ``provider_states.py`` in their ``setUp`` methods. Each interaction defined in the pact
   file will get a corresponding test method.

   This file is 100% ready to go, and does not need to be edited.


Updating test files
-------------------

Currently, ``pact-testgen`` will not overwrite an existing ``provider_states.py`` file.

To update tests after an update to the pact file which does not
add new provider states, simply re-run ``pact-testgen``.

If provider states have changed, rename your ``provider_states.py`` before running
``pact-testgen``. Copy provider states from the renamed file to the new ``provider_states.py``
file, and fill in any new states as required.

In the future, ``pact-testgen`` will intelligently update the ``provider_states.py`` file,
which should make updates simpler, as well as simplify support for provider code bases
with multiple consumers.



Pact Broker
-----------

To retrieve a Pact contract from a Pact Broker instead of the local filesystem, provide the following parameters.
Any parameter can be given using CLI arguments, or set as an environment variable. Parameters passed to the CLI
will take precedence over environment variables.

.. list-table::
   :header-rows: 1
   :widths: 25 80 10 10 10

   * - Parameter
     - CLI
     - Env var
     - Required
     - Notes

   * - Base URL
     - ``-b``, ``--broker-base-url``
     - ``PACT_BROKER_BASE_URL``
     - Yes
     -

   * - Provider Name
     - ``-s``, ``--provider-name``
     - ``PACT_BROKER_PROVIDER_NAME``
     - Yes
     -


   * - Consumer Name
     - ``-c``, ``--consumer-name``
     - ``PACT_BROKER_CONSUMER_NAME``
     - Yes
     -


   * - Consumer version
     - ``-c``, ``--consumer-version``
     - ``PACT_BROKER_CONSUMER_VERSION``
     - No
     - Defaults to "latest"


Broker Authentication
+++++++++++++++++++++

Currently, only basic authentication is supported.

.. list-table::
   :header-rows: 1
   :widths: 25 80 10 10 10

   * - Parameter
     - CLI
     - Env var
     - Required
     - Notes

   * - Broker Username
     - ``-u``, ``--broker-username``
     - ``PACT_BROKER_USERNAME``
     - Yes
     -


   * - Broker Password
     - ``-p``, ``--broker-password``
     - ``PACT_BROKER_PASSWORD``
     - Yes
     -

Help
----

::

    ❯ pact-testgen --help
    usage: pact-testgen [-h] [-f PACT_FILE] [--base-class BASE_CLASS] [--line-length LINE_LENGTH] [--debug] [--version] [-q] [-m] [-b BROKER_BASE_URL] [-u BROKER_USERNAME] [-p BROKER_PASSWORD] [-c CONSUMER_NAME] [-s PROVIDER_NAME]
                        [-v CONSUMER_VERSION]
                        output_dir

    positional arguments:
    output_dir            Output for generated Python files.

    optional arguments:
    -h, --help            show this help message and exit
    -f PACT_FILE, --pact-file PACT_FILE
                            Path to a Pact file.
    --base-class BASE_CLASS
                            Python path to the TestCase which generated test cases will subclass.
    --line-length LINE_LENGTH
                            Target line length for generated files.
    --debug
    --version             show program's version number and exit
    -q, --quiet           Silence output
    -m, --merge-provider-state-file
                            Attempt to merge new provider state functions into existing provider state file. Only available on Python 3.9+.

    pact broker arguments:
    -b BROKER_BASE_URL, --broker-base-url BROKER_BASE_URL
                            Pact broker base url. Optionally configure by setting the PACT_BROKER_BASE_URL environment variable.
    -u BROKER_USERNAME, --broker-username BROKER_USERNAME
                            Pact broker username.
    -p BROKER_PASSWORD, --broker-password BROKER_PASSWORD
                            Pact broker password.
    -c CONSUMER_NAME, --consumer-name CONSUMER_NAME
                            Consumer name used to retrieve Pact contract from the pact broker.
    -s PROVIDER_NAME, --provider-name PROVIDER_NAME
                            Provider name used to retrieve Pact contract from the pact broker.
    -v CONSUMER_VERSION, --consumer-version CONSUMER_VERSION
                            Consumer version number. Used to retrieve the Pact contract from the Pact broker. Optional, defaults to 'latest'.
