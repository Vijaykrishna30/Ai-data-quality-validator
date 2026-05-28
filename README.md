# AI Data Quality Validator

A Streamlit-based data quality validator for CSV files.

## Overview

This app helps teams inspect and improve tabular data quality by automatically detecting:

- Missing values
- Duplicate rows
- Invalid email addresses
- Invalid phone numbers
- Suspicious salary values
- Overall data health score

It also allows users to download a cleaned CSV after removing duplicates, missing rows, and invalid email records.

## Features

- Upload any CSV file in the browser
- View a summary of data quality issues
- Visualize issue counts with a bar chart
- Download a cleaned CSV file
- Simple scoring for quick risk assessment

## Requirements

- Python 3.10+
- Streamlit
- pandas
- plotly
- openpyxl

## Installation

```bash
pip install -r requirements.txt
```

## Run the app

```bash
streamlit run app.py
```

Then open the URL shown in your terminal.

## CSV expectations

The sample validator is designed for CSV files with columns such as:

- `email`
- `phone`
- `salary`

If these columns are present, the app will perform email and phone validation and flag high salaries.

## Sample data

A sample dataset is included in `sample_data/customers.csv` for quick testing.

## Notes

- Invalid emails are detected using a simple regex pattern.
- Invalid phone numbers are flagged when they are not exactly 10 digits long.
- Suspicious salaries are currently defined as values greater than `500000`.

## License

This project is released under the MIT License.
