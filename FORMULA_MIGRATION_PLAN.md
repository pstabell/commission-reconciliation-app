# Formula Migration Plan - Zero Legacy Data Strategy
**Created**: July 5, 2025  
**Last Updated**: July 6, 2025  
**Purpose**: Ensure 100% formula-generated values in locked columns with no manual entries remaining

## ⚠️ MIGRATION STATUS - July 6, 2025

**IMPORTANT**: This migration plan is ON HOLD pending formula implementation in the application.

### Current Situation:
- ❌ Formula calculations are NOT implemented in the Edit Policies form
- ❌ Fields are still manual input, not auto-calculated
- ⚠️ Running this migration now would be premature

### Prerequisites Before Migration:
1. ✅ Phase 0: Reconciliation protection (COMPLETED)
2. ❌ Phase 1: Formula field implementation (NOT STARTED)
3. ❌ Testing of formula calculations (PENDING)
4. ❌ User acceptance of formula logic (PENDING)

## 🎯 Migration Objective

**Goal**: Replace EVERY value in the following columns with formula-calculated values:
1. `Agency Estimated Comm/Revenue (CRM)`
2. `Agent Estimated Comm $`

**Key Principle**: If the formula cannot calculate due to missing data, the result MUST be $0.00, making it visually obvious which transactions need attention.

## 📊 Pre-Migration Analysis

### Step 1: Data Audit Query
```sql
-- Identify all scenarios in current data
SELECT 
    COUNT(*) as total_records,
    -- Scenario breakdowns
    COUNT(CASE WHEN "Premium Sold" IS NULL OR "Premium Sold" = 0 THEN 1 END) as missing_premium,
    COUNT(CASE WHEN "Policy Gross Comm %" IS NULL OR "Policy Gross Comm %" = 0 THEN 1 END) as missing_comm_rate,
    COUNT(CASE WHEN "Transaction Type" IS NULL OR "Transaction Type" = '' THEN 1 END) as missing_trans_type,
    
    -- Current values that will change
    COUNT(CASE WHEN "Agency Estimated Comm/Revenue (CRM)" > 0 
               AND ("Premium Sold" IS NULL OR "Policy Gross Comm %" IS NULL) THEN 1 END) as agency_comm_will_become_zero,
    COUNT(CASE WHEN "Agent Estimated Comm $" > 0 
               AND ("Agency Estimated Comm/Revenue (CRM)" IS NULL OR "Agency Estimated Comm/Revenue (CRM)" = 0) THEN 1 END) as agent_comm_will_become_zero,
    
    -- Manual overrides detected
    COUNT(CASE WHEN "Premium Sold" > 0 AND "Policy Gross Comm %" > 0 
               AND ABS("Agency Estimated Comm/Revenue (CRM)" - ("Premium Sold" * "Policy Gross Comm %" / 100)) > 0.01 THEN 1 END) as manual_agency_overrides,
    
    -- Reconciliation entries (should remain $0)
    COUNT(CASE WHEN "Transaction ID" LIKE '%-STMT-%' THEN 1 END) as reconciliation_entries
FROM policies;
```

### Step 2: Backup Current Values
```sql
-- Create backup table with current values and calculated differences
CREATE TABLE formula_migration_backup AS
SELECT 
    _id,
    "Transaction ID",
    "Customer",
    "Policy Number",
    "Premium Sold",
    "Policy Gross Comm %",
    "Agency Estimated Comm/Revenue (CRM)" as current_agency_comm,
    "Agent Estimated Comm $" as current_agent_comm,
    "Transaction Type",
    
    -- What the formulas will calculate
    CASE 
        WHEN "Premium Sold" IS NULL OR "Policy Gross Comm %" IS NULL THEN 0
        ELSE "Premium Sold" * "Policy Gross Comm %" / 100
    END as formula_agency_comm,
    
    CASE 
        WHEN "Premium Sold" IS NULL OR "Policy Gross Comm %" IS NULL THEN 0
        WHEN "Transaction Type" IN ('NEW', 'NBS', 'STL', 'BoR') THEN ("Premium Sold" * "Policy Gross Comm %" / 100) * 0.50
        WHEN "Transaction Type" IN ('RWL', 'REWRITE') THEN ("Premium Sold" * "Policy Gross Comm %" / 100) * 0.25
        WHEN "Transaction Type" IN ('CAN', 'XCL') THEN 0
        WHEN "Transaction Type" IN ('END', 'PCH') THEN 
            CASE 
                WHEN "Policy Origination Date" = "Effective Date" THEN ("Premium Sold" * "Policy Gross Comm %" / 100) * 0.50
                ELSE ("Premium Sold" * "Policy Gross Comm %" / 100) * 0.25
            END
        ELSE 0  -- Unknown transaction type
    END as formula_agent_comm,
    
    -- Differences
    "Agency Estimated Comm/Revenue (CRM)" - 
        CASE 
            WHEN "Premium Sold" IS NULL OR "Policy Gross Comm %" IS NULL THEN 0
            ELSE "Premium Sold" * "Policy Gross Comm %" / 100
        END as agency_diff,
    
    CURRENT_TIMESTAMP as backup_date
FROM policies;
```

## 🔄 Migration Process

### Phase 1: Reconciliation Entries (Special Handling)
```sql
-- Step 1.1: Ensure all -STMT-, -VOID-, -ADJ- entries have $0 in both columns
UPDATE policies
SET 
    "Agency Estimated Comm/Revenue (CRM)" = 0,
    "Agent Estimated Comm $" = 0
WHERE 
    "Transaction ID" LIKE '%-STMT-%' 
    OR "Transaction ID" LIKE '%-VOID-%'
    OR "Transaction ID" LIKE '%-ADJ-%';
```

### Phase 2: Agency Commission Migration
```sql
-- Step 2.1: Update all records with formula calculation
UPDATE policies
SET "Agency Estimated Comm/Revenue (CRM)" = 
    CASE 
        -- Reconciliation entries always $0
        WHEN "Transaction ID" LIKE '%-STMT-%' THEN 0
        WHEN "Transaction ID" LIKE '%-VOID-%' THEN 0
        WHEN "Transaction ID" LIKE '%-ADJ-%' THEN 0
        
        -- Missing data = $0 (makes it obvious what needs fixing)
        WHEN "Premium Sold" IS NULL THEN 0
        WHEN "Policy Gross Comm %" IS NULL THEN 0
        WHEN "Premium Sold" = 0 THEN 0
        WHEN "Policy Gross Comm %" = 0 THEN 0
        
        -- Valid calculation
        ELSE ROUND("Premium Sold" * "Policy Gross Comm %" / 100, 2)
    END
WHERE 1=1;  -- Update ALL records
```

### Phase 3: Agent Commission Migration
```sql
-- Step 3.1: Update all records with formula calculation
UPDATE policies
SET "Agent Estimated Comm $" = 
    CASE 
        -- Reconciliation entries always $0
        WHEN "Transaction ID" LIKE '%-STMT-%' THEN 0
        WHEN "Transaction ID" LIKE '%-VOID-%' THEN 0
        WHEN "Transaction ID" LIKE '%-ADJ-%' THEN 0
        
        -- Missing data = $0
        WHEN "Premium Sold" IS NULL THEN 0
        WHEN "Policy Gross Comm %" IS NULL THEN 0
        WHEN "Transaction Type" IS NULL THEN 0
        WHEN "Transaction Type" = '' THEN 0
        
        -- Transaction type rates
        WHEN "Transaction Type" IN ('NEW', 'NBS', 'STL', 'BoR') 
            THEN ROUND(("Premium Sold" * "Policy Gross Comm %" / 100) * 0.50, 2)
            
        WHEN "Transaction Type" IN ('RWL', 'REWRITE') 
            THEN ROUND(("Premium Sold" * "Policy Gross Comm %" / 100) * 0.25, 2)
            
        WHEN "Transaction Type" IN ('CAN', 'XCL') 
            THEN 0
            
        WHEN "Transaction Type" IN ('END', 'PCH') THEN
            CASE 
                WHEN "Policy Origination Date" = "Effective Date" 
                    THEN ROUND(("Premium Sold" * "Policy Gross Comm %" / 100) * 0.50, 2)
                ELSE ROUND(("Premium Sold" * "Policy Gross Comm %" / 100) * 0.25, 2)
            END
            
        -- Unknown transaction type = $0 (needs attention)
        ELSE 0
    END
WHERE 1=1;  -- Update ALL records
```

## 📋 Post-Migration Verification

### Step 1: Identify Records Needing Attention
```sql
-- Find all records where formulas resulted in $0 due to missing data
SELECT 
    "Transaction ID",
    "Customer",
    "Policy Number",
    "Premium Sold",
    "Policy Gross Comm %",
    "Transaction Type",
    "Agency Estimated Comm/Revenue (CRM)",
    "Agent Estimated Comm $",
    CASE
        WHEN "Premium Sold" IS NULL OR "Premium Sold" = 0 THEN 'Missing Premium'
        WHEN "Policy Gross Comm %" IS NULL OR "Policy Gross Comm %" = 0 THEN 'Missing Gross Comm %'
        WHEN "Transaction Type" IS NULL OR "Transaction Type" = '' THEN 'Missing Transaction Type'
        ELSE 'Unknown Issue'
    END as issue_reason
FROM policies
WHERE 
    -- Not a reconciliation entry
    "Transaction ID" NOT LIKE '%-STMT-%'
    AND "Transaction ID" NOT LIKE '%-VOID-%'
    AND "Transaction ID" NOT LIKE '%-ADJ-%'
    -- But has $0 in formula fields
    AND ("Agency Estimated Comm/Revenue (CRM)" = 0 OR "Agent Estimated Comm $" = 0)
ORDER BY "Customer", "Policy Number";
```

### Step 2: Verification Report
```sql
-- Summary of migration results
SELECT 
    'Total Records' as metric,
    COUNT(*) as count
FROM policies
UNION ALL
SELECT 
    'Records with $0 Agency Comm (excluding reconciliations)',
    COUNT(*)
FROM policies
WHERE "Agency Estimated Comm/Revenue (CRM)" = 0
    AND "Transaction ID" NOT LIKE '%-STMT-%'
UNION ALL
SELECT 
    'Records with $0 Agent Comm (excluding reconciliations)',
    COUNT(*)
FROM policies
WHERE "Agent Estimated Comm $" = 0
    AND "Transaction ID" NOT LIKE '%-STMT-%'
UNION ALL
SELECT 
    'Records with Missing Premium',
    COUNT(*)
FROM policies
WHERE ("Premium Sold" IS NULL OR "Premium Sold" = 0)
    AND "Transaction ID" NOT LIKE '%-STMT-%'
UNION ALL
SELECT 
    'Records with Missing Gross Comm %',
    COUNT(*)
FROM policies
WHERE ("Policy Gross Comm %" IS NULL OR "Policy Gross Comm %" = 0)
    AND "Transaction ID" NOT LIKE '%-STMT-%'
UNION ALL
SELECT 
    'Records with Missing Transaction Type',
    COUNT(*)
FROM policies
WHERE ("Transaction Type" IS NULL OR "Transaction Type" = '')
    AND "Transaction ID" NOT LIKE '%-STMT-%';
```

### Step 3: Difference Analysis
```sql
-- Compare before and after values
SELECT 
    b."Transaction ID",
    b."Customer",
    b."Policy Number",
    b.current_agency_comm as "Old Agency Comm",
    p."Agency Estimated Comm/Revenue (CRM)" as "New Agency Comm",
    b.current_agent_comm as "Old Agent Comm",
    p."Agent Estimated Comm $" as "New Agent Comm",
    ABS(b.current_agency_comm - p."Agency Estimated Comm/Revenue (CRM)") as "Agency Diff",
    ABS(b.current_agent_comm - p."Agent Estimated Comm $") as "Agent Diff"
FROM formula_migration_backup b
JOIN policies p ON b._id = p._id
WHERE 
    ABS(b.current_agency_comm - p."Agency Estimated Comm/Revenue (CRM)") > 0.01
    OR ABS(b.current_agent_comm - p."Agent Estimated Comm $") > 0.01
ORDER BY "Agency Diff" DESC, "Agent Diff" DESC;
```

## 🚨 Rollback Plan

If migration needs to be reversed:

```sql
-- Restore original values from backup
UPDATE policies p
SET 
    "Agency Estimated Comm/Revenue (CRM)" = b.current_agency_comm,
    "Agent Estimated Comm $" = b.current_agent_comm
FROM formula_migration_backup b
WHERE p._id = b._id;
```

## 📊 Expected Outcomes

### Clean Data Indicators
After migration, you should see:

1. **All reconciliation entries**: $0.00 in both columns
2. **Missing premium records**: $0.00 (easy to spot and fix)
3. **Missing comm % records**: $0.00 (easy to spot and fix)
4. **Missing transaction type**: $0.00 in agent comm
5. **Valid records**: Calculated values matching formulas exactly

### Visual Result in Application
```
Customer: ABC Company
Premium Sold: [empty]           ← Need to fill this
Policy Gross Comm %: 10%
Agency Comm (CRM): $0.00 🔒     ← Formula shows $0 due to missing premium
Agent Comm $: $0.00 🔒          ← Formula shows $0 due to missing premium
```

## ✅ Success Metrics

1. **100% Formula Coverage**: Every value in locked columns is formula-generated
2. **Zero Legacy Values**: No manually entered values remain
3. **Clear Problem Identification**: All $0.00 values indicate missing data
4. **Accurate Calculations**: All non-zero values match formula exactly
5. **Audit Trail**: Complete backup of pre-migration values

## 📝 Migration Checklist

- [ ] Run pre-migration analysis query
- [ ] Create backup table
- [ ] Export backup to CSV for extra safety
- [ ] Run Phase 1: Reconciliation entries update
- [ ] Run Phase 2: Agency commission migration
- [ ] Run Phase 3: Agent commission migration
- [ ] Generate verification report
- [ ] Review records needing attention
- [ ] Document any manual fixes needed
- [ ] Confirm all values are formula-generated
- [ ] Archive backup table after 90 days

---

*This migration plan ensures complete data integrity with no legacy values remaining. Every cell will either show a formula-calculated value or $0.00 when data is missing, making it immediately obvious which transactions need attention.*