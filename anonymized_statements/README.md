# Commission Statement Anonymizer

This folder contains tools for anonymizing commission statement Excel files for demo purposes.

## Quick Start

1. Place your commission statement Excel files in this folder
2. Run the anonymization script:
   ```bash
   python anonymize_statements_fixed.py
   ```
3. The script will create anonymized versions with "ANONYMIZED_" prefix

## What the Script Does

### 1. **Anonymizes Customer Names**
- Replaces real customer names with randomly generated fictitious names
- Consistent across all files (same customer gets same fictitious name)
- Mix of personal names and business names (LLC, Inc, Corp, etc.)

### 2. **Scrambles Policy Numbers**
- Removes all dashes, spaces, and dots from policy numbers
- Replaces digits with random digits (0-9)
- Replaces letters with random letters (A-Z)
- Consistent across files (same policy gets same scrambled number)

### 3. **Adjusts Dates**
- Bumps all effective dates forward by 2 months
- Removes time components (formats as YYYY-MM-DD)
- Helps avoid date conflicts with existing demo data

### 4. **Modifies Financial Amounts**
- Increases all commission/financial amounts by 10%
- Prevents duplicate reconciliation matches in demo environment
- Affects columns with keywords: amount, commission, premium, fee, total, gross, net, payment, paid
- Skips percentage columns

## Expected Column Names

The script looks for these columns (case-insensitive):
- **Customer Names**: 'Insured Name', 'Insured', 'Customer', 'Client', 'Name', 'Customer Name'
- **Policy Numbers**: 'Policy', 'Policy Number', 'Policy #', 'Policy No'
- **Dates**: 'Eff Date' (or any column with 'eff' and 'date')
- **Financial Data**: Any column containing financial keywords (see above)

## Modifying the Script

To adjust the anonymization behavior, edit `anonymize_statements_fixed.py`:

### Change Date Offset
```python
df[col] = df[col] + pd.DateOffset(months=2)  # Change the number
```

### Change Financial Increase
```python
df[col] = numeric_data * 1.10  # Change from 1.10 to desired multiplier
```

### Add More File Names
```python
files_to_process = [
    os.path.join(current_dir, "2025-06-30 Commission Statement.xlsx"),
    os.path.join(current_dir, "2025-07-31 Commission Statement.xlsx"),
    os.path.join(current_dir, "2025-08-31 Commission Statement.xlsx"),
    # Add more files here
]
```

## Example Output

```
Starting anonymization process for commission statements...
============================================================

📄 Processing '2025-06-30 Commission Statement.xlsx'...
   - Loaded 34 rows
   - Found name column: 'Insured Name'
   - Anonymized 24 unique names
   - Found policy column: 'Policy'
   - Scrambled 26 unique policy numbers
   - Found effective date column: 'Eff Date'
   - Bumped dates by 2 months and removed time
   - Increased 2 financial columns by 10%
   ✅ SUCCESS: Saved to 'ANONYMIZED_2025-06-30 Commission Statement.xlsx'
```

## Troubleshooting

### "File not found" Error
- Make sure Excel files are in the same folder as the script
- Check file names match exactly (including .xlsx extension)

### Missing Columns
- The script will show warnings for missing columns but continue processing
- Check the "Expected Column Names" section above
- Column names are matched case-insensitively

### Date Format Issues
- Script expects dates to be parseable by pandas
- If dates aren't updating, check the date column format in Excel

## Notes

- Original files are never modified
- Anonymized files can be re-anonymized (will generate new random data)
- The script maintains consistency within a single run (same customer = same fictitious name)
- Policy numbers have ALL special characters removed for clean data