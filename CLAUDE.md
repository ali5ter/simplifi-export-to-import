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
2. Date conversion: `YYYY-MM-DD` → `M/D/YY`
3. Amount cleaning: removes `$` and `,` characters
4. Addition of required `Check_No` column (empty)
5. Removal of unused export columns (account, state, usage, action, security, etc.)

## CSV Format Mapping

**Export columns** (from Simplifi):
- postedOn, payee, amount, category, tags, notes, account, state, usage, action, security, etc.

**Import columns** (required by Simplifi):
- Date, Payee, Amount, Category, Tags, Notes, Check_No

The script is case-insensitive for input column names but enforces exact case for output columns.

## Known Limitations

- Splits and transfers may not import correctly (Simplifi limitation)
- Recurring Transaction Series cannot be imported via CSV (Simplifi does not include them in exports)
