# Data pipeline

The Python pipeline will extract observations from registered inputs, normalize the values and metadata, and validate the resulting CSV and JSON before loading them into DuckDB. Document-specific mappings and review evidence will be introduced with the first verified inputs.

Run the checks with `python pipeline/validate.py` and `python -m unittest discover -s pipeline`.
Regenerate the CSV from reviewed JSON with `python pipeline/validate.py --write-csv`.
The empty bootstrap files pass structural checks. Release coverage requires the reviewed corpus.
