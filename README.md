# MP1 Data Pipeline
'''
This is a command-line pipeline that takes in a CSV file and validates it and cleans it before producing an output and saving the result. What controls the entire pipeline is the config/config.yaml file. This file allows for the same code to be able to clean different CSV files by simply updating the configuration. The data movement starts first with the the input file and the configuration loaded, then the data provided will be validated, then cleaned through a couple steps, and then the final data is saved to the output path. The organization of the pipeline starts in the pipeline.py file which manages what steps are to be taken. The modules in the src folder are where the work to validate and clean the data is done. data_loaders.py loads in the CSV, YAML and JSON files. data_validator.py scans for the required colomns in the data and removes any bad data points. data_processor.py focuses on removing any missing values, duplicates or outliers from the data as well as providing a summary of what changed in the data after this step. data_output.py is where the final data is stored. utils.py gives us the logging setup and the file input validation. Finally test data is under the fixtures folder and the results from that fall under the output. 

EXAMPLE CODE

INPUT

python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
OUTPUT

22:40:22 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, config=config/config.yaml, output=output/clean.csv
22:40:22 INFO     src.utils — Input file validated: fixtures/sample_data.csv
22:40:22 INFO     src.utils — Input file validated: config/config.yaml
22:40:23 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
22:40:25 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
22:40:25 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
22:40:25 DEBUG    src.data_validator — Validation: 100 → 98 rows (valid 98, removed 2)
22:40:25 INFO     __main__ — Validation complete: 100 → 98 rows
22:40:25 DEBUG    src.data_processor — remove_duplicates: 98 → 96 rows (removed 2)
22:40:25 DEBUG    src.data_processor — handle_missing: 96 → 94 rows (removed 2)
22:40:25 DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, lower=43.625, upper=106.625, removed=2
22:40:25 INFO     __main__ — Processing complete: 98 → 92 rows
22:40:26 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
22:40:26 INFO     __main__ — Saved cleaned data to output/clean.csv
Cleaning report:
{'rows_before': 98,
 'rows_after': 92,
 'rows_removed': 6,
 'columns_before': 5,
 'columns_after': 5,
 'columns_removed': 0}

 '''
