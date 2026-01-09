# Simplifi Export to Import Converter

Converts a Quicken Simplifi exported CSV file into the format required for importing back into Simplifi.

## Problem

Simplifi's export format is incompatible with its import format. This script handles the conversion automatically.

## Requirements

- Python 3 (standard library only, no pip packages needed)

## Usage

```bash
./simplifi-export-to-import.py input.csv [output.csv]
```

If you don't specify an output filename, it will create one by adding `-import` to your input filename.

### Example

```bash
# Export from Simplifi saved as 'my-account-export.csv'
./simplifi-export-to-import.py my-account-export.csv

# Creates: my-account-export-import.csv
```

Then import `my-account-export-import.csv` into Simplifi using the CSV import option.

## What It Does

1. **Deletes unnecessary columns** from the export (account, state, usage, action, security, etc.)
2. **Renames columns** to match import requirements:
   - `postedOn` → `Date`
   - `payee` → `Payee`
   - `amount` → `Amount`
   - `category` → `Category`
   - `tags` → `Tags`
   - `notes` → `Notes`
3. **Converts date format** from `YYYY-MM-DD` to `M/D/YY` (e.g., `2024-01-15` → `1/15/24`)
4. **Cleans amount field** by removing `$` and `,` characters
5. **Adds required Check_No column** (empty)

## Tested With

- Simplifi exports from 2024
- Transactions with commas in payee/category/notes fields
- Negative amounts (expenses)
- Positive amounts (income)

## Limitations

- Splits and transfers may not import correctly (this is a Simplifi limitation)
- Recurring Transaction Series are not included in exports and cannot be imported via CSV
