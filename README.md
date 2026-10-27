# API JSON Data Processor

A Python portfolio project that retrieves data from a public API, validates and processes JSON records, calculates summary statistics, and writes a structured JSON report.

## What this project demonstrates

- Python
- REST API consumption
- JSON parsing and serialization
- HTTP request handling
- Error handling
- Dataclasses
- Data normalization
- Aggregate statistics
- File input/output
- Automated testing
- Clear, auditable processing logic

## Public API

This project uses the free JSONPlaceholder test API:

`https://jsonplaceholder.typicode.com/posts`

No API key or account is required.

## Run the project

```bash
python api_json_processor.py
```

The script:

1. Sends an HTTP request to the public API.
2. Parses the JSON response.
3. Validates and normalizes the returned records.
4. Calculates basic dataset statistics.
5. Writes a structured report to `api_report.json`.

## Run the tests

```bash
python -m unittest test_api_json_processor.py
```

The tests use local sample data, so they do not require an internet connection.

## Example console output

```text
Fetching JSON data from public API...
API JSON DATA PROCESSOR
========================================
Processed posts: 100
Unique users: 10
Average body word count: ...
Report saved to: api_report.json
```

## Project design

The project separates network access, data normalization, statistics, and report generation into independent functions. This makes the code easier to test, understand, and maintain.

Invalid records are skipped rather than causing the entire processing workflow to fail, while network and JSON-format errors produce clear error messages.

## Why I built this

I created this project to demonstrate practical Python experience working with REST APIs, JSON data, validation, error handling, reporting, and automated tests.

## Author

Stephen Burks
