"""
Data Processing Pipeline
DS 3500 - MP1

Usage:
    python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml
    python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
"""

# decides the order of the steps and passes results from one step to the next
#  the modules in src/ do the actual work such as loading, validating, cleaning, saving

import argparse
import logging
import sys
from pprint import pprint

import pandas as pd

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)

# When this file is run as a script, __name__ is "__main__", which is why
# log messages from this file are labeled __main__
logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Command-line data processing pipeline."
    )
    # required=True means argparse stops with a usage message if one is missing
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to the input file",
    )
    parser.add_argument(
        "--config", "-c",
        required=True,
        help="Path to the YAML configuration file",
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Path to the output file",
    )
    # store_true makes this a flag with no value: args.verbose is True if --verbose is given, and False otherwise
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging",
    )
    return parser.parse_args()


def main():
    """Main pipeline function."""

    # read the command line and set up logging.
    # --verbose switches the logging level from INFO to DEBUG.
    args = parse_arguments()
    setup_logging(args.verbose)

    logger.debug(
        f"Arguments parsed: input={args.input}, "
        f"config={args.config}, output={args.output}"
    )

    # check both files exist before loading anything, a bad path gives a clear error message and exit code 1 instead of a crash.
    # Exit code 0 means success and anything else means failure.

    # Validate both files before loading anything
    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)

    # The loaders raise ValueError for an unsupported format, which we catch here and turn into an exit.
    # Load the input data and the configuration
    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    # The pipeline works on tables, so the input must be a CSV
    if not isinstance(data, pd.DataFrame):
        logger.error(f"Input must be a CSV file to be processed: {args.input}")
        sys.exit(1)

    # Validate the data using the settings in the configuration
    validation = config.get("validation", {})
    required_columns = validation.get("required_columns", [])
    numeric_columns = validation.get("numeric_columns", [])

    rows_loaded = len(data)
    try:
        data = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)
    logger.info(f"Validation complete: {rows_loaded} → {len(data)} rows")

    # Keep a copy of the validated data so we can compare before and after
    df_before = data.copy()

    # clean. process_data() reads the "processing" section of the
    # config and runs only the steps that are turned on.
    try:
        df_after = process_data(data, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(df_before, df_after)
    logger.info(f"Processing complete: {len(df_before)} → {len(df_after)} rows")

    save_data(df_after, args.output)
    logger.info(f"Saved cleaned data to {args.output}")

    # print the report last and do not sort alphabetically
    print("Cleaning report:")
    pprint(report, sort_dicts=False)


# This runs main() only when the file is run directly
# (python pipeline.py), not when another file imports it
if __name__ == "__main__":
    main()