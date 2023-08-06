"""Console script for pact_testgen."""
import argparse
import sys
from pathlib import Path
from pact_testgen import __version__
from pact_testgen.broker import BrokerBasicAuthConfig, BrokerConfig
from pact_testgen.pact_testgen import run
from pact_testgen.files import merge_is_available


def directory(path: str) -> Path:
    path = Path(path)
    if path.is_dir():
        return path
    raise argparse.ArgumentError()


def main():
    """Console script for pact_testgen."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "output_dir", help="Output for generated Python files.", type=directory
    )
    parser.add_argument("-f", "--pact-file", help="Path to a Pact file.")
    parser.add_argument(
        "--base-class",
        default="django.test.TestCase",
        help=("Python path to the TestCase which generated test cases will subclass."),
    )
    parser.add_argument(
        "--line-length",
        type=int,
        default=88,
        help="Target line length for generated files.",
    )
    parser.add_argument("--debug", action="store_true")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s v{version}".format(version=__version__),
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Silence output")
    parser.add_argument(
        "-m",
        "--merge-provider-state-file",
        action="store_true",
        help="Attempt to merge new provider state functions into existing "
        "provider state file. Only available on Python 3.9+.",
    )
    # Options related to pact broker are the same as those for the pact broker CLI
    # client, as much as possible
    # https://github.com/pact-foundation/pact_broker-client#usage---cli

    broker_group = parser.add_argument_group("pact broker arguments")

    broker_group.add_argument(
        "-b",
        "--broker-base-url",
        help="Pact broker base url. Optionally configure by setting the "
        "PACT_BROKER_BASE_URL environment variable.",
    )
    broker_group.add_argument("-u", "--broker-username", help="Pact broker username.")
    broker_group.add_argument("-p", "--broker-password", help="Pact broker password.")
    broker_group.add_argument(
        "-c",
        "--consumer-name",
        help="Consumer name used to retrieve Pact contract from the pact broker.",
    )
    broker_group.add_argument(
        "-s",
        "--provider-name",
        help="Provider name used to retrieve Pact contract from the pact broker.",
    )
    broker_group.add_argument(
        "-v",
        "--consumer-version",
        # Note we don't actually set default="latest" here, that happens
        # later when constructing the URL. Here, we rely on consumer_version=None
        # if it isn't specified.
        help="Consumer version number. Used to retrieve the Pact contract from the "
        "Pact broker. Optional, defaults to 'latest'.",
    )

    args = parser.parse_args()

    # Either both, or neither, i.e. logical XNOR
    if bool(args.consumer_name) ^ bool(args.provider_name):
        parser.error(
            "Must specify both --provider-name and --consumer-name, or neither."
        )

    if args.broker_base_url and not args.consumer_name:
        parser.error("Must specify consumer and provider names with pact broker URL.")

    if args.pact_file and args.consumer_name:
        parser.error("Specify either pact file or pact broker options, not both.")

    if not (args.pact_file or args.consumer_name):
        parser.error("Must provide a pact file with -f, or pact broker options.")

    if args.consumer_version and not args.consumer_name:
        parser.error("Must specify consumer name with consumer version.")

    if args.merge_provider_state_file and not merge_is_available():
        parser.error("Merge provider state file is only available in Python 3.9+.")

    if args.consumer_name:
        broker_config = BrokerConfig(
            base_url=args.broker_base_url,
            auth=BrokerBasicAuthConfig(
                username=args.broker_username,
                password=args.broker.password,
            ),
        )
    else:
        broker_config = None

    try:
        run(
            base_class=args.base_class,
            pact_file=args.pact_file,
            broker_config=broker_config,
            provider_name=args.provider_name,
            consumer_name=args.consumer_name,
            consumer_version=args.consumer_version,
            output_dir=args.output_dir,
            line_length=args.line_length,
            merge_ps_file=args.merge_provider_state_file,
        )
        return 0
    except Exception as e:
        if args.debug:
            raise
        print(f"An error occurred: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
