# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A single-purpose Python script that converts Quicken Simplifi exported CSV files into the import-ready format that Simplifi requires.

## Usage

Run the converter:
```bash
./simplifi-export-to-import.py input.csv [output.csv]
```

If output filename is omitted, creates `input-import.csv` automatically.

## Architecture

This is a **single-file Python script** (simplifi-export-to-import.py) with no external dependencies beyond Python 3 standard library.

The script performs:
1. Case-insensitive column mapping from Simplifi export format to import format
2. Date format preservation: maintains `M/D/YYYY` format (4-digit years, despite docs stating M/D/YY)
3. Category format transformation: strips parent from `Parent:Child` → `Child` (e.g., `Auto & Transport:Gas & Fuel` → `Gas & Fuel`)
4. Amount cleaning: removes `$` and `,` characters
5. Addition of required `Check_No` column (empty)
6. Proper CSV quoting: uses `csv.QUOTE_ALL` to ensure all fields are quoted
7. Removal of unused export columns (account, state, usage, action, security, etc.)

## CSV Format Mapping

**Export columns** (from Simplifi):
- postedOn, payee, amount, category, tags, notes, account, state, usage, action, security, etc.

**Import columns** (required by Simplifi):
- Date, Payee, Amount, Category, Tags, Notes, Check_No

The script is case-insensitive for input column names but enforces exact case for output columns.

## Critical Implementation Details

**Simplifi's official documentation is incorrect/misleading.** Key discoveries:

1. **Date format**: Official docs state `M/D/YY` (2-digit year) but actual imports require `M/D/YYYY` (4-digit year)
2. **Category format**: Exports contain `Parent:Child` format but imports only accept child names
3. **CSV quoting**: Must use `csv.QUOTE_ALL` - all fields must be quoted for reliable import
4. **Line endings**: Standard Unix `\n` line endings (though this seems less critical)

## Known Limitations

- Splits and transfers may not import correctly (Simplifi limitation)
- Recurring Transaction Series cannot be imported via CSV (Simplifi does not include them in exports)
- Categories must already exist in Simplifi to import successfully
- Import does not update existing transactions - only creates new ones
