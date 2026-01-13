# Simplifi CSV Import Format Requirements

Use this prompt when working on projects that need to generate Simplifi-compatible CSV files for import.

---

## Prompt for AI Assistants

When generating CSV files for Quicken Simplifi import, follow these EXACT requirements (discovered through extensive testing - Simplifi's official documentation is incorrect/misleading):

### Required CSV Structure

**Headers (exact case):**
```
Date,Payee,Amount,Category,Tags,Notes,Check_No
```

### Critical Format Requirements

1. **Date Format**: `M/D/YYYY` (4-digit year)
   - ❌ WRONG: `1/13/26` (Simplifi docs say this, but it's WRONG)
   - ✅ CORRECT: `1/13/2026`
   - Format: Month (no leading zero) / Day (no leading zero) / 4-digit Year
   - Examples: `3/5/2025`, `12/25/2025`

2. **Category Format**: Child name only (NO parent prefix)
   - ❌ WRONG: `Auto & Transport:Gas & Fuel`
   - ✅ CORRECT: `Gas & Fuel`
   - If your data has parent:child format, strip everything before and including the colon
   - Categories MUST already exist in the user's Simplifi account with matching names

3. **Amount Format**: Numeric with negative sign for expenses
   - ❌ WRONG: `$1,234.56` or `($50.00)`
   - ✅ CORRECT: `1234.56` (income) or `-50.00` (expense)
   - No dollar signs, no commas, use negative sign for expenses

4. **CSV Quoting**: ALL fields must be quoted
   - Use Python's `csv.QUOTE_ALL` or equivalent in other languages
   - Example row: `"1/13/2026","Starbucks","-7.50","Restaurants","","",""`

5. **Check_No Column**: Always include, usually empty
   - Use empty string `""` for most transactions
   - Only populate if you have actual check numbers

6. **Tags and Notes**: Can be empty but must exist as columns
   - Multiple tags: use comma-separated format `"tag1, tag2, tag3"`
   - Empty: just use `""`

### Example Valid CSV

```csv
"Date","Payee","Amount","Category","Tags","Notes","Check_No"
"1/13/2026","Starbucks","-7.50","Coffee Shops","Vacation","","
"1/15/2026","Uber","-21.12","Rideshare","Business, Travel","Client meeting","
"1/20/2026","Paycheck","2500.00","Salary","","",""
"1/22/2026","Grocery Store","-150.45","Groceries","","Weekly shopping",""
```

### Common Pitfalls to Avoid

1. ❌ Using 2-digit years (M/D/YY) - will cause all categories to import as "Uncategorized"
2. ❌ Including parent category names (Parent:Child) - will cause categories to fail
3. ❌ Not quoting all fields - can cause parsing errors
4. ❌ Including dollar signs or commas in amounts - will cause import errors
5. ❌ Using categories that don't exist in Simplifi - will import as "Uncategorized"
6. ❌ Windows (CRLF) line endings - use Unix (LF) line endings

### Python Implementation Template

```python
import csv

# When writing CSV for Simplifi import:
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(
        f,
        fieldnames=['Date', 'Payee', 'Amount', 'Category', 'Tags', 'Notes', 'Check_No'],
        quoting=csv.QUOTE_ALL  # CRITICAL: Quote all fields
    )
    writer.writeheader()

    for transaction in transactions:
        writer.writerow({
            'Date': format_date(transaction['date']),  # M/D/YYYY format
            'Payee': transaction['payee'],
            'Amount': format_amount(transaction['amount']),  # No $, no commas, negative for expenses
            'Category': extract_child_category(transaction['category']),  # Strip parent if present
            'Tags': transaction.get('tags', ''),
            'Notes': transaction.get('notes', ''),
            'Check_No': transaction.get('check_number', '')
        })

def format_date(date_obj):
    """Convert to M/D/YYYY format"""
    return f"{date_obj.month}/{date_obj.day}/{date_obj.year}"

def format_amount(amount):
    """Remove currency symbols, ensure negative for expenses"""
    amount_str = str(amount).replace('$', '').replace(',', '').strip()
    return amount_str

def extract_child_category(category):
    """Strip parent from Parent:Child format"""
    if ':' in category:
        return category.split(':', 1)[1].strip()
    return category.strip()
```

### Testing Checklist

Before considering your CSV generator complete:

- [ ] Test with a small file (3-5 transactions) first
- [ ] Verify dates show as M/D/YYYY with 4-digit years
- [ ] Confirm categories are child-only names (no colons)
- [ ] Check that all fields are quoted in the output file
- [ ] Verify amounts have no $ or commas
- [ ] Test that existing categories import correctly (not as "Uncategorized")
- [ ] Confirm expense amounts are negative
- [ ] Check file uses Unix (LF) line endings, not Windows (CRLF)

### Reference

These requirements were discovered through extensive testing and debugging documented at:
https://github.com/ali5ter/simplifi-export-to-import

The script at that repository successfully converts Simplifi exports to import-ready format and serves as a reference implementation.
