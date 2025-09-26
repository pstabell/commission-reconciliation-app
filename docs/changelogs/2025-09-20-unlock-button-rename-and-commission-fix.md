# Unlock Button Rename and Agent Commission Due Fix
**Date**: September 20, 2025
**Version**: 4.3.x

## Changes Made

### 1. Unlock Button Rename
- **Changed**: "🔓 Unlock STMT" → "🔓 Unlock Reconciled Transactions"
- **Location**: Edit Policy Transactions page, line 8254
- **Reason**: Clearer description of what the button does (unlocks STMT/VOID/ADJ transactions)

### 2. Agent Commission Due Calculation Fix
- **Issue**: Dashboard showed $2,045.75 instead of expected $9,842.93
- **Root Cause**: Demo account had NULL values in "Agent Estimated Comm $" column
- **Fix Applied**:
  1. Created diagnostic scripts to identify missing values
  2. Updated "Agent Estimated Comm $" using formula: Premium × Commission % × Agent Rate
  3. Updated "Broker Fee Agent Comm" as 50% of Broker Fee
  4. Recalculated "Total Agent Comm" = Agent Estimated Comm $ + Broker Fee Agent Comm
- **Result**: Agent Commission Due now shows $9,824.29 (correct value)

## SQL Scripts Created
1. `check_total_agent_comm_issue.sql` - Initial diagnostic
2. `simple_commission_debug.sql` - Simplified debugging
3. `check_balance_calculation.sql` - Balance column verification
4. `fix_agent_estimated_comm.sql` - First fix attempt
5. `fix_all_commission_calculations.sql` - Complete fix that resolved the issue

## Technical Details
The dashboard relies on "Total Agent Comm" column being properly populated. The demo data had:
- NULL values in "Agent Estimated Comm $" 
- Zero values in "Total Agent Comm"
- This caused the balance calculation to return incorrect low values

## Lessons Learned
1. Always check if required columns have data before assuming calculation issues
2. The dashboard uses the same calculation as Policy Revenue Ledger - data must be complete
3. Document fixes immediately as they're easier to find than searching through old commits