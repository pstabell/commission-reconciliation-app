# IMPORT Transaction Analysis Report

Generated: 2025-07-30

## Summary

Based on the commission app codebase analysis, here's what we know about -IMPORT transactions:

### What are -IMPORT Transactions?

-IMPORT transactions are special transaction records that appear to be created during data import or migration processes. These transactions have "-IMPORT" as a suffix in their Transaction ID field.

### Key Fields to Analyze

The two commission fields that may have double entries are:
1. **Agent Estimated Comm $** - The estimated commission amount for the agent
2. **Agent Paid Amount (STMT)** - The actual paid amount from statements

### Potential Issues with Double Entries

When both fields have non-zero values in -IMPORT transactions, it could indicate:
- Duplicate commission recording during import
- Both estimated and actual values being imported incorrectly
- Data migration issues where values were mapped to both fields

### How to Manually Analyze

1. **Access the Application**
   - Open the Sales Commission App
   - Navigate to the Policy Ledger page

2. **Filter for -IMPORT Transactions**
   - Use the search box to filter: `-IMPORT`
   - This will show all transactions with -IMPORT in the Transaction ID

3. **Identify Double Entries**
   - Look for rows where BOTH "Agent Estimated Comm $" AND "Agent Paid Amount (STMT)" have values
   - These are potential double entries

4. **Export for Analysis**
   - Use the "Export to Excel" feature
   - In Excel, you can:
     - Filter for non-zero values in both columns
     - Sum the totals to see the financial impact
     - Group by customer or date to find patterns

### What to Look For

1. **Pattern Analysis**
   - Are double entries concentrated on specific dates?
   - Do they affect specific customers more than others?
   - Are the amounts identical or different?

2. **Financial Impact**
   - Total amount in Agent Estimated Comm $ for double entries
   - Total amount in Agent Paid Amount (STMT) for double entries
   - Potential overpayment if both were processed

3. **Data Quality Issues**
   - Inconsistent import patterns
   - Missing or incorrect transaction IDs
   - Reconciliation status of these transactions

### Recommended Actions

1. **Immediate Analysis**
   - Export all -IMPORT transactions
   - Identify all double entries
   - Calculate total financial impact

2. **Data Cleanup**
   - Determine which field should contain the value
   - Clear the incorrect field
   - Update reconciliation status

3. **Process Improvement**
   - Review import procedures
   - Add validation to prevent double entries
   - Consider removing -IMPORT suffix after validation

### SQL Query for Database Analysis

If you have direct database access, use this query:

```sql
SELECT 
    "Transaction ID",
    "Customer",
    "Agent Estimated Comm $",
    "Agent Paid Amount (STMT)",
    "Stmt Paid Date",
    "X Date",
    CASE 
        WHEN "Agent Estimated Comm $" > 0 AND "Agent Paid Amount (STMT)" > 0 
        THEN 'DOUBLE ENTRY' 
        ELSE 'SINGLE ENTRY' 
    END as entry_type
FROM policies
WHERE "Transaction ID" LIKE '%-IMPORT'
ORDER BY entry_type DESC, "Customer", "Stmt Paid Date";
```

### Notes from Code Analysis

- The app uses Supabase as the database backend
- The main table is called 'policies'
- There are protections against deleting certain -IMPORT transactions
- The app has special handling for -STMT- and -VOID- transactions, but -IMPORT transactions don't appear to have special visual indicators

## Next Steps

1. Run the manual analysis using the app's search and export features
2. Document all double entries found
3. Determine the correct values for each transaction
4. Plan a data cleanup strategy
5. Implement validation to prevent future occurrences