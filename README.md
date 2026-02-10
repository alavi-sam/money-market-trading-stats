# Money Market Trading Statistics ETL

An ETL (Extract, Transform, Load) pipeline for processing Canadian bond and money market secondary trading statistics from Excel files into clean, structured CSV datasets.

## Overview

This project processes historical trading statistics from multiple Excel workbooks with varying formats (pre-2020 and 2020+) and consolidates them into normalized CSV files for easier analysis. The data includes various financial instruments across different market segments.

## Project Structure

```
money-market-trading-stats/
├── etl.py                 # Main ETL script with data cleaning functions
├── requirements.txt       # Python dependencies
├── raw_data/             # Source Excel files (*.xlsx)
├── processed_data/       # Output CSV files
└── test.ipynb           # Testing/exploration notebook
```

## Data Sources

The pipeline processes Excel files containing trading statistics with multiple worksheets covering:

- **MMKT**: Money Market instruments
- **BOND**: Bond trading data
- **GOVT**: Government bonds
- **FED_PROV**: Federal and Provincial bonds
- **STRIP_MUNI**: STRIP and Municipal bonds
- **CORP**: Corporate bonds
- **MBS_ABS**: Mortgage-Backed and Asset-Backed Securities
- **BOND_REPO**: Bond repurchase agreements
- **MMKT_REPO**: Money Market repo transactions

## Features

- **Multi-format handling**: Automatically detects and processes different Excel formats based on year (<2020 vs ≥2020)
- **Data normalization**: Converts wide-format data to long-format (melted) with consistent schema
- **Date parsing**: Extracts and standardizes dates from various month/year formats
- **Header processing**: Handles multi-level headers and cleans column names
- **Missing data handling**: Fills NaN values and filters out quarterly/total summary rows
- **Batch processing**: Processes all Excel files in the raw_data directory

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd money-market-trading-stats
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the ETL pipeline:

```bash
python etl.py
```

This will:
1. Read all Excel files from the `raw_data/` directory
2. Process each worksheet type across all files
3. Concatenate data from multiple years
4. Output cleaned CSV files to `processed_data/` directory

## Output Format

All output CSV files follow a consistent long-format structure:

| Column | Type | Description |
|--------|------|-------------|
| date | date | Trading date (first day of month) |
| month | string | Month number |
| year | string | Year |
| instruments | string | Instrument type/category |
| volume | float | Trading volume |

## Data Cleaning Functions

The project includes specialized cleaning functions for each worksheet type:

- `clean_mmkt_sheet()` - Money market instruments ([etl.py:31](etl.py#L31))
- `clean_govt_sheet()` - Government bonds ([etl.py:60](etl.py#L60))
- `clean_bond_sheet()` - General bonds ([etl.py:87](etl.py#L87))
- `clean_fed_prov_sheet()` - Federal/Provincial bonds ([etl.py:114](etl.py#L114))
- `clean_strip_muni_sheet()` - STRIP and Municipal bonds ([etl.py:143](etl.py#L143))
- `clean_corp_sheet()` - Corporate bonds ([etl.py:171](etl.py#L171))
- `clean_mbs_abs_sheet()` - MBS/ABS securities ([etl.py:199](etl.py#L199))
- `clean_bonds_repo_sheet()` - Bond repos ([etl.py:227](etl.py#L227))
- `clean_mmkt_repo_sheet()` - Money market repos ([etl.py:254](etl.py#L254))

Each function handles format variations between pre-2020 and 2020+ files.

## Dependencies

Core dependencies:
- **pandas**: Data manipulation and CSV I/O
- **openpyxl**: Excel file reading
- **numpy**: Numerical operations

See [requirements.txt](requirements.txt) for complete list.

## Requirements

- Python 3.7+
- All dependencies listed in requirements.txt
