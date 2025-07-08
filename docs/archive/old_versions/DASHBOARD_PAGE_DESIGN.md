# Dashboard Page Design
**Page**: Commission Dashboard  
**Route**: Main/Home page  
**Purpose**: Overview of commission metrics and quick insights

## 🎯 Current Issues

### Transaction vs Policy Confusion
- **Current**: Shows "Total Policies: 195"
- **Reality**: This is transaction count, not unique policies
- **Problem**: Misleading - one policy can have many transactions (NEW, RWL, END, etc.)

## 📊 Design Specifications

### Metrics to Display
1. **Transaction Metrics**
   - Total Transactions: X
   - This Month: X
   - This Quarter: X
   - This Year: X

2. **Policy Metrics** (new)
   - Unique Policies: X (COUNT DISTINCT policy numbers)
   - Active Policies: X (latest transaction not CAN/XCL)
   - New This Month: X (NEW transactions)
   - Renewals This Month: X (RWL transactions)

3. **Financial Metrics**
   - Premium Sold Total
   - Agency Commission Total
   - Agent Commission Total
   - Outstanding Balances

### Visual Layout
```
┌─────────────────────────────────────────────┐
│          Commission Dashboard               │
├─────────────────┬───────────────────────────┤
│ TRANSACTIONS    │ POLICIES                  │
│ Total: 195      │ Unique: 87               │
│ This Month: 23  │ Active: 72               │
│ -STMT-: 2       │ Cancelled: 15            │
├─────────────────┴───────────────────────────┤
│              FINANCIAL SUMMARY              │
│ Premium Sold: $XXX,XXX                      │
│ Agency Comm: $XX,XXX                        │
│ Agent Comm: $X,XXX                          │
└─────────────────────────────────────────────┘
```

### Transaction Type Breakdown
Show distribution pie chart:
- NEW: X%
- RWL: X%
- END: X%
- CAN: X%
- -STMT-: X%

## 🔧 Implementation Notes

### SQL for Unique Policies
```sql
SELECT COUNT(DISTINCT "Policy Number") as unique_policies
FROM policies
WHERE "Policy Number" IS NOT NULL;
```

### SQL for Active Policies
```sql
WITH latest_transactions AS (
  SELECT "Policy Number", 
         "Transaction Type",
         ROW_NUMBER() OVER (PARTITION BY "Policy Number" 
                           ORDER BY "Effective Date" DESC) as rn
  FROM policies
)
SELECT COUNT(DISTINCT "Policy Number") as active_policies
FROM latest_transactions
WHERE rn = 1 
  AND "Transaction Type" NOT IN ('CAN', 'XCL');
```

## 📝 Terminology Standards

### Use These Terms:
- "Transaction Count" - for database records
- "Policy Count" - for unique policy numbers
- "Policy Transactions" - when showing both

### Avoid:
- "Total Policies" when meaning transactions
- Ambiguous use of "policies"

## 🎨 Future Enhancements

1. **Interactive Filters**
   - Filter by agent
   - Filter by carrier
   - Filter by date range

2. **Drill-Down Capability**
   - Click metrics to see details
   - Link to filtered views

3. **Trend Charts**
   - Monthly transaction trends
   - Policy growth over time
   - Commission trends

---

*This page serves as the entry point and should provide clear, accurate metrics at a glance.*