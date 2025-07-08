# 🧮 Formulas & Calculations Reference

## 💰 Commission Calculations

### Agent Commission Percentage
**Based on Transaction Type**:

| Transaction Type | Commission % | Description |
|------------------|--------------|-------------|
| NEW | 50% | New business policies |
| NBS | 50% | New business (alternative code) |
| STL | 50% | New business settlement |
| BoR | 50% | Broker of Record changes |
| END | 50% or 25% | Endorsements* |
| PCH | 50% or 25% | Policy changes* |
| RWL | 25% | Renewals |
| REWRITE | 25% | Policy rewrites |
| CAN | 0% | Cancellations |
| XCL | 0% | Cancellations (alternative) |

*For END and PCH: 50% if Policy Origination Date = Effective Date, otherwise 25%

### Commission Dollar Calculations

**Agent Estimated Comm $**:
```
Agency Estimated Comm/Revenue (CRM) × (Agent Comm % ÷ 100)
```

**Agency Estimated Comm/Revenue (CRM)**:
```
Commissionable Premium × (Policy Gross Comm % ÷ 100)
```
*Note: Now uses Commissionable Premium (Premium Sold minus taxes/fees) for accurate calculations

**Policy Balance Due**:
```
Agent Estimated Comm $ - Agent Paid Amount (STMT)
```

### 🆕 Broker Fee & Tax Calculations

**Commissionable Premium**:
```
Premium Sold - Policy Taxes & Fees = Commissionable Premium
```

**Broker Fee Agent Commission**:
```
Broker Fee × 0.50 = Broker Fee Agent Comm
```
*Note: Broker fee commission is always 50% regardless of transaction type

**Total Agent Commission**:
```
Agent Estimated Comm $ + Broker Fee Agent Comm = Total Agent Comm
```

## 📊 Premium Calculations

### Premium Sold (for Endorsements)
```
Premium Sold = New/Revised Premium - Existing Premium
```

**Example**:
- Existing Premium: $1,200
- New/Revised Premium: $1,350
- Premium Sold: $150

### Revenue Calculation
**Agency Revenue (10% default)**:
```
Agency Revenue = Premium Sold × 0.10
```

## 🎯 Report Aggregations

### Policy Revenue Ledger Reports
**Data is aggregated by Policy Number**:

**Descriptive Fields**: First value (should be same for all transactions)
- Customer, Policy Type, Carrier Name
- Effective Date, Policy Origination Date
- Client ID

**Monetary Fields**: Sum of all transactions
- Agent Estimated Comm $
- Agent Paid Amount (STMT)
- Agency Estimated Comm/Revenue (CRM)
- Premium Sold

**Calculated Fields**: Computed after aggregation
- Policy Balance Due = Sum(Agent Estimated Comm $) - Sum(Agent Paid Amount)

## 📈 Metrics Calculations

### Dashboard Metrics
**Total Transactions**: Count of all database rows

**Total Commissions**: Sum of all "Calculated Commission" values

**Client Metrics**:
- Total Paid Amount: Sum of "Agent Paid Amount (STMT)" for client
- Total Est. Commission: Sum of "Agent Estimated Comm $" for client

### Report Metrics
**Outstanding Policies**: Count where Policy Balance Due > 0

**Total Balance Due**: Sum of all positive Policy Balance Due amounts

**Mapping Health**: (Mapped Columns ÷ Total Columns) × 100

## 🔄 Calculation Triggers

### Automatic Recalculation
**Triggered when**:
- Adding new policy transaction
- Editing existing policy data
- Saving changes in Edit Policies page
- Running report generation

**Fields Recalculated**:
- Agent Estimated Comm $
- Agency Estimated Comm/Revenue (CRM)
- Policy Balance Due
- Report totals and metrics

### Manual Recalculation
**When needed**:
- After bulk data import
- After column mapping changes
- After database restoration

**How to trigger**:
1. Go to "Edit Policies in Database"
2. Click "Update Database with Edits"
3. System recalculates all formula fields