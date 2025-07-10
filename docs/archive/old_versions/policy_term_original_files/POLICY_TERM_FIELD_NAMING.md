# Policy Term Field Naming Convention

## Summary
- **UI Label**: "Policy Term Months"
- **Database Column**: "Policy Term" 
- **Data Type**: INTEGER (stores number only)
- **Values**: 3, 6, 9, or 12

## Why This Naming?
1. **UI Label** ("Policy Term Months") - Clear to users that they should enter months
2. **Database Column** ("Policy Term") - Shorter for database efficiency
3. **Column Mapping** - Handles the translation between UI and database

## Column Mapping Entry
In `column_mapping_config.py`:
```python
"Policy Term Months": "Policy Term",
```

This means:
- When users see the field, it's labeled "Policy Term Months"
- When saved to database, it goes to column "Policy Term"
- The value is just a number (6, 12, etc.)

## Usage Examples

### In Forms (UI):
```python
st.selectbox("Policy Term Months", [None, 3, 6, 9, 12])
```

### In Database Queries:
```sql
SELECT * FROM policies WHERE "Policy Term" = 12;
```

### In Code (using mapping):
```python
policy_term = row.get(get_mapped_column("Policy Term Months"))
```

## Benefits
- Users clearly understand to enter months
- Database column name is concise
- No confusion about units (always months)
- Consistent with app's column mapping system