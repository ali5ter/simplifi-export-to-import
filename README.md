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
3. **Preserves date format** as `M/D/YYYY` (4-digit year required despite documentation stating M/D/YY)
4. **Strips parent category names** - converts `Auto & Transport:Gas & Fuel` → `Gas & Fuel` (Simplifi requires child-only names)
5. **Cleans amount field** by removing `$` and `,` characters
6. **Adds required Check_No column** (empty)
7. **Properly quotes all CSV fields** to ensure correct parsing

## Important Notes

**Simplifi's documentation is misleading!** Through extensive testing, we discovered:

- **Date format**: Documentation says `M/D/YY` but imports actually require `M/D/YYYY` (4-digit years)
- **Category format**: Exports use `Parent:Child` format but imports require only child names (e.g., `Gas & Fuel` not `Auto & Transport:Gas & Fuel`)
- **Categories must exist**: Categories will only import if they already exist in your Simplifi account with matching names
- **Import is not an update mechanism**: Importing to an existing account won't update transactions, it will create duplicates or be ignored

## Tested With

- Simplifi exports from 2025-2026
- 500+ transaction imports
- Transactions with commas in payee/category/notes fields
- Negative amounts (expenses)
- Positive amounts (income)
- Hierarchical categories (Parent:Child format)

## Limitations

- Splits and transfers may not import correctly (this is a Simplifi limitation)
- Recurring Transaction Series are not included in exports and cannot be imported via CSV
- Categories must already exist in Simplifi to import successfully
