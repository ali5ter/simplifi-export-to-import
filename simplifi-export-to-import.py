#!/usr/bin/env python3
"""
simplifi-export-to-import.py
Converts a Simplifi exported CSV to import-ready format

Usage: ./simplifi-export-to-import.py input.csv [output.csv]
"""

import csv
import sys
from datetime import datetime
from pathlib import Path


def convert_date(date_str):
    """Convert date to M/D/YYYY format

    Despite documentation saying M/D/YY, the official Simplifi template
    uses M/D/YYYY (4-digit year), so we preserve that format.
    """
    if not date_str:
        return ""

    # Try parsing various date formats and output as M/D/YYYY
    for fmt in ["%m/%d/%Y", "%-m/%-d/%Y", "%Y-%m-%d"]:
        try:
            dt = datetime.strptime(date_str, fmt)
            return f"{dt.month}/{dt.day}/{dt.year}"
        except ValueError:
            continue

    # If all parsing fails, return as-is
    return date_str


def format_amount(amount_str):
    """Remove $, commas from amount"""
    if not amount_str:
        return ""
    return amount_str.replace('$', '').replace(',', '').strip()


def format_category(category_str):
    """Extract child category from parent:child format

    Simplifi exports categories as 'Parent:Child' but requires
    only the child name for import (e.g., 'Gas & Fuel' not 'Auto & Transport:Gas & Fuel')
    """
    if not category_str:
        return ""
    # If there's a colon, take everything after it
    if ':' in category_str:
        return category_str.split(':', 1)[1].strip()
    return category_str.strip()


def main():
    # Check arguments
    if len(sys.argv) < 2:
        print("Usage: simplifi-export-to-import.py input.csv [output.csv]", file=sys.stderr)
        print("Converts Simplifi export CSV to import-ready format", file=sys.stderr)
        sys.exit(1)

    input_file = Path(sys.argv[1])

    # Generate output filename if not provided
    if len(sys.argv) >= 3:
        output_file = Path(sys.argv[2])
    else:
        output_file = input_file.with_stem(f"{input_file.stem}-import")

    # Verify input file exists
    if not input_file.exists():
        print(f"Error: Input file '{input_file}' not found", file=sys.stderr)
        sys.exit(1)

    # Column mapping
    column_map = {
        'postedon': 'Date',
        'payee': 'Payee',
        'amount': 'Amount',
        'category': 'Category',
        'tags': 'Tags',
        'notes': 'Notes'
    }

    try:
        with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
             open(output_file, 'w', newline='', encoding='utf-8') as outfile:

            reader = csv.DictReader(infile)

            # Normalize header names (case-insensitive)
            fieldnames_lower = {k.lower(): k for k in reader.fieldnames}

            # Check required columns exist
            required = ['postedon', 'payee', 'amount']
            missing = [col for col in required if col not in fieldnames_lower]
            if missing:
                print(f"Error: Missing required columns: {', '.join(missing)}", file=sys.stderr)
                sys.exit(1)

            # Write output with proper quoting for all fields
            writer = csv.DictWriter(outfile, fieldnames=['Date', 'Payee', 'Amount', 'Category', 'Tags', 'Notes', 'Check_No'], quoting=csv.QUOTE_ALL)
            writer.writeheader()

            for row in reader:
                # Create case-insensitive row dict
                row_lower = {k.lower(): v for k, v in row.items()}

                output_row = {
                    'Date': convert_date(row_lower.get('postedon', '')),
                    'Payee': row_lower.get('payee', ''),
                    'Amount': format_amount(row_lower.get('amount', '')),
                    'Category': format_category(row_lower.get('category', '')),
                    'Tags': row_lower.get('tags', ''),
                    'Notes': row_lower.get('notes', ''),
                    'Check_No': ''
                }

                writer.writerow(output_row)

        print(f"✓ Converted {input_file} to {output_file}")
        print("Import this file into Simplifi using the CSV import option")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
