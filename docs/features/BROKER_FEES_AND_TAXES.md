# Broker Fees and Taxes/Fees Implementation

**Created**: January 7, 2025  
**Updated**: January 7, 2025 - Implementation Complete  
**Purpose**: Document the implementation of broker fees and tax/fee separation for accurate commission calculations

## Overview

This document outlines the implementation plan for adding broker fee handling and separating non-commissionable taxes/fees from the premium to ensure accurate commission calculations.

## Business Requirements

### 1. Broker Fees
- Agency collects broker fees directly from clients
- Agency keeps 100% of the broker fee revenue
- Agent receives 50% commission on broker fees (regardless of transaction type)
- Broker fees are separate from policy premiums and commissions

### 2. Policy Taxes & Fees
- Taxes and fees are NOT commissionable
- Must be excluded from premium before calculating commissions
- Combined into single "Policy Taxes & Fees" field for simplicity
- Still track total premium for reporting purposes

### 3. Commission Calculation Changes
- Commissions calculated on "Commissionable Premium" (Premium - Taxes/Fees)
- Agent receives standard commission on commissionable premium PLUS 50% of broker fee
- All existing commission rate logic (NEW 50%, RWL 25%) remains unchanged

## Database Schema Changes

### New Columns Required

```sql
ALTER TABLE policies ADD COLUMN "Broker Fee" DECIMAL(10,2) DEFAULT 0;
ALTER TABLE policies ADD COLUMN "Policy Taxes & Fees" DECIMAL(10,2) DEFAULT 0;
ALTER TABLE policies ADD COLUMN "Commissionable Premium" DECIMAL(10,2);
ALTER TABLE policies ADD COLUMN "Broker Fee Agent Comm" DECIMAL(10,2);
ALTER TABLE policies ADD COLUMN "Total Agent Comm" DECIMAL(10,2);
```

### Column Purposes

| Column Name | Type | Purpose | Calculation |
|-------------|------|---------|-------------|
| Broker Fee | Currency | Fee charged by agency | User input |
| Policy Taxes & Fees | Currency | Combined taxes and fees | User input |
| Commissionable Premium | Currency | Premium minus taxes/fees | Formula: Premium Sold - Policy Taxes & Fees |
| Broker Fee Agent Comm | Currency | Agent's 50% of broker fee | Formula: Broker Fee × 0.50 |
| Total Agent Comm | Currency | Combined agent commission | Formula: Agent Estimated Comm $ + Broker Fee Agent Comm |

## Updated Commission Formulas

### Existing Formulas (Modified)

**Formula #1: Agency Estimated Comm/Revenue (CRM)**
```
OLD: Premium Sold × (Policy Gross Comm % ÷ 100)
NEW: Commissionable Premium × (Policy Gross Comm % ÷ 100)
```

**Formula #2: Agent Estimated Comm $**
```
NO CHANGE: Agency Estimated Comm/Revenue (CRM) × (Agent Comm Rate ÷ 100)
```

### New Formulas

**Formula #4: Commissionable Premium**
```
Premium Sold - Policy Taxes & Fees = Commissionable Premium
```

**Formula #5: Broker Fee Agent Commission**
```
Broker Fee × 0.50 = Broker Fee Agent Comm
```

**Formula #6: Total Agent Commission**
```
Agent Estimated Comm $ + Broker Fee Agent Comm = Total Agent Comm
```

## UI Changes - Add New Policy Transaction Form

### Field Organization

#### Premium & Fee Information (New Section)
```
Left Column:                    Right Column:
- Premium Sold ($)              - Policy Taxes & Fees ($)
- Broker Fee ($)                - Commissionable Premium ($) [calculated, gray]
```

#### Commission Details (Updated)
```
Left Column:                    Right Column:
- Policy Gross Comm %           - Agency Est. Comm/Revenue (CRM) [calculated]
- Agent Comm (NEW/RWL) [gray]   - Agent Estimated Comm $ [calculated]
- Broker Fee Agent Comm [gray]  - Total Agent Comm [calculated, gray]
```

### Field Behaviors

1. **Editable Fields** (white background):
   - Premium Sold
   - Policy Taxes & Fees
   - Broker Fee
   - Policy Gross Comm %

2. **Calculated Fields** (gray background #F5F5F5):
   - Commissionable Premium
   - Agency Estimated Comm/Revenue (CRM)
   - Agent Comm (NEW 50% RWL 25%)
   - Agent Estimated Comm $
   - Broker Fee Agent Comm
   - Total Agent Comm

## Implementation Status

### ✅ Phase 1: Configuration Updates (COMPLETE)
- Added new columns to column_mapping_config.py
- Updated calculated fields list
- Added formula definitions for new fields

### ✅ Phase 2: Formula Engine Updates (COMPLETE)
- Updated apply_formula_display() to calculate Commissionable Premium
- Modified Agency commission to use Commissionable Premium
- Added Broker Fee Agent Comm calculation (always 50%)
- Added Total Agent Comm calculation

### ✅ Phase 3: UI Implementation (COMPLETE)
- Added Premium & Fee Information section to Add New Policy form
- Reorganized Commission Details with new fields
- Updated Edit Policy form with same structure
- All fields calculate automatically in forms

### ✅ Phase 4: Display Updates (COMPLETE)  
- Updated All Policy Transactions to show new columns
- Added new fields to numeric columns configuration
- Formula mode properly displays calculated values

### ⏳ Phase 5: Database Migration (PENDING)
**Important**: The new columns need to be added to your Supabase database:

```sql
-- Run these commands in Supabase SQL Editor
ALTER TABLE policies ADD COLUMN "Broker Fee" DECIMAL(10,2) DEFAULT 0;
ALTER TABLE policies ADD COLUMN "Policy Taxes & Fees" DECIMAL(10,2) DEFAULT 0;
ALTER TABLE policies ADD COLUMN "Commissionable Premium" DECIMAL(10,2);
ALTER TABLE policies ADD COLUMN "Broker Fee Agent Comm" DECIMAL(10,2);
ALTER TABLE policies ADD COLUMN "Total Agent Comm" DECIMAL(10,2);

-- Update existing records with default values
UPDATE policies SET 
  "Broker Fee" = 0,
  "Policy Taxes & Fees" = 0,
  "Commissionable Premium" = "Premium Sold",
  "Broker Fee Agent Comm" = 0,
  "Total Agent Comm" = "Agent Estimated Comm $"
WHERE "Broker Fee" IS NULL;
```

## Example Calculations

### Scenario 1: New Business with Broker Fee
- Premium Sold: $10,000
- Policy Taxes & Fees: $500
- Broker Fee: $250
- Policy Gross Comm %: 20%
- Transaction Type: NEW

**Calculations:**
- Commissionable Premium: $10,000 - $500 = $9,500
- Agency Estimated Comm: $9,500 × 0.20 = $1,900
- Agent Estimated Comm: $1,900 × 0.50 = $950 (NEW = 50%)
- Broker Fee Agent Comm: $250 × 0.50 = $125
- Total Agent Comm: $950 + $125 = $1,075

### Scenario 2: Renewal without Broker Fee
- Premium Sold: $5,000
- Policy Taxes & Fees: $200
- Broker Fee: $0
- Policy Gross Comm %: 15%
- Transaction Type: RWL

**Calculations:**
- Commissionable Premium: $5,000 - $200 = $4,800
- Agency Estimated Comm: $4,800 × 0.15 = $720
- Agent Estimated Comm: $720 × 0.25 = $180 (RWL = 25%)
- Broker Fee Agent Comm: $0 × 0.50 = $0
- Total Agent Comm: $180 + $0 = $180

## Reporting Considerations

### New Report Metrics
1. Total Broker Fees Collected
2. Total Taxes & Fees
3. Total Commissionable Premium vs Total Premium
4. Broker Fee Commissions Paid

### Dashboard Updates
- Add "Broker Fees" metric
- Show "Commissionable Premium" total
- Display "Taxes & Fees" separately

## Migration Strategy

### For Existing Data
1. Set Broker Fee = 0 for all existing records
2. Set Policy Taxes & Fees = 0 for all existing records
3. Set Commissionable Premium = Premium Sold (assume no taxes initially)
4. Recalculate all commission fields using new formulas

### Data Validation
- Ensure Premium Sold ≥ Policy Taxes & Fees
- Broker Fee and Taxes/Fees cannot be negative
- Total Agent Comm must equal sum of components

## Security Considerations

### Reconciliation Protection
- Broker Fee fields locked for -STMT- transactions
- Tax/Fee fields locked for reconciliation entries
- Maintain existing Phase 0 security model

### Audit Trail
- Track changes to broker fees separately
- Log tax/fee modifications
- Maintain commission calculation history

## Future Enhancements

1. **Broker Fee Tiers**: Different broker fee rates by policy type
2. **Tax Categories**: Break down taxes vs fees for detailed reporting
3. **Automated Tax Rates**: Calculate taxes based on state/product
4. **Broker Fee Agreements**: Track different broker fee arrangements by client

---

*This implementation ensures accurate commission calculations while maintaining flexibility for broker fees and non-commissionable amounts.*