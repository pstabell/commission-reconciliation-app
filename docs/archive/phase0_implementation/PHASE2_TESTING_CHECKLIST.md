# Phase 2 Testing Checklist - Formula Display in Data Grid
**Date**: July 6, 2025  
**Purpose**: Guided inspection of new formula columns in "All Policies" view

## 📋 Pre-Test Setup

### 1. Navigate to All Policies
- [ ] Open the Sales Commission App
- [ ] Click on "All Policies in Database" in the sidebar
- [ ] Verify you see the total record count at the top

## 🔍 Visual Inspection

### 2. Check for New Info Banner
- [ ] Look for blue info box below "Showing records X to Y"
- [ ] Should say: "📊 **Formula Columns**: 'Agency Comm (Formula)' and 'Agent Comm (Formula)' are auto-calculated..."
- [ ] Confirms formula columns are active

### 3. Locate New Formula Columns
Look for these 4 new columns in the data grid:

#### After "Agency Estimated Comm/Revenue (CRM)" column:
- [ ] **Agency Comm (Formula)** - Should show calculated values
- [ ] **Agency Comm Variance** - Should show differences

#### After "Agent Estimated Comm $" column:
- [ ] **Agent Comm (Formula)** - Should show calculated values  
- [ ] **Agent Comm Variance** - Should show differences

### 4. Column Order Verification
The columns should appear in this sequence:
1. ... Premium Sold ...
2. ... Policy Gross Comm % ...
3. ... Agency Estimated Comm/Revenue (CRM)
4. ➡️ Agency Comm (Formula) [NEW]
5. ➡️ Agency Comm Variance [NEW]
6. ... Agent Estimated Comm $
7. ➡️ Agent Comm (Formula) [NEW]
8. ➡️ Agent Comm Variance [NEW]

## 🧮 Calculation Verification

### 5. Pick a Sample Transaction
Find a transaction with these characteristics:
- [ ] Has a Premium Sold value (not $0.00)
- [ ] Has a Policy Gross Comm % (not 0%)
- [ ] Has a Transaction Type (NEW, RWL, etc.)

**Record the values:**
- Customer Name: _________________
- Premium Sold: $_________________
- Policy Gross Comm %: ___________% 
- Transaction Type: ______________

### 6. Verify Agency Commission Formula
- [ ] Check: Agency Comm (Formula) = Premium Sold × Policy Gross Comm % ÷ 100
- [ ] Example: $10,000 × 10% = $1,000
- [ ] Does the formula column show the correct calculation?

### 7. Verify Agent Commission Formula
Based on Transaction Type:
- [ ] NEW, NBS, STL, BoR → Agent gets 50% of Agency Comm
- [ ] RWL, REWRITE → Agent gets 25% of Agency Comm
- [ ] CAN, XCL → Agent gets 0%
- [ ] Does the Agent Comm (Formula) match the expected rate?

### 8. Check Variance Columns
- [ ] **Agency Comm Variance** = Manual Entry - Formula
  - Positive = Manual entry is higher than formula
  - Negative = Manual entry is lower than formula
  - Zero = Perfect match
- [ ] **Agent Comm Variance** = Manual Entry - Formula
  - Look for any large variances that might indicate errors

## 🔎 Special Cases to Find

### 9. Look for These Scenarios
Try to find examples of each:

#### Zero Variance (Perfect Match):
- [ ] Find a transaction where variance columns show $0.00
- [ ] This means manual entry matches the formula exactly

#### Positive Variance:
- [ ] Find a transaction where variance is positive
- [ ] Manual entry is higher than formula suggests

#### Negative Variance:
- [ ] Find a transaction where variance is negative
- [ ] Manual entry is lower than formula suggests

#### Missing Data:
- [ ] Find a transaction with missing Premium or Comm %
- [ ] Formula should show $0.00

#### Reconciliation Transactions:
- [ ] Search for a -STMT- transaction
- [ ] Should these have formula calculations? (Note findings)

## 📊 Export Testing

### 10. Test CSV Export
- [ ] Click "📥 Current Page CSV"
- [ ] Open the downloaded file
- [ ] Verify all 4 formula columns are included
- [ ] Check that values match what you saw on screen

### 11. Test Excel Export
- [ ] Click "📥 Current Page Excel"
- [ ] Open the downloaded file
- [ ] Verify formula columns are included
- [ ] Check formatting (should have 2 decimal places)

### 12. Test Full Data Export
- [ ] Click "📥 All Data CSV" or "📥 All Data Excel"
- [ ] Verify formula columns are included for ALL records
- [ ] Note: This may take longer to generate

## 🎯 Pagination Testing

### 13. Check Multiple Pages
- [ ] Change "Items per page" to 25
- [ ] Navigate to page 2
- [ ] Verify formula columns still appear
- [ ] Verify calculations are correct on different pages

## 📝 Findings & Feedback

### 14. Record Your Observations

**What works well:**
- 
- 
- 

**What could be improved:**
- 
- 
- 

**Any calculation errors found:**
- Transaction ID: _________ Issue: _________________
- Transaction ID: _________ Issue: _________________

**Visual/UX suggestions:**
- Would color coding help?
- Should variance columns be highlighted when non-zero?
- Other ideas:

**Performance:**
- [ ] Does the page load quickly?
- [ ] Any lag when changing pages?
- [ ] Export generation speed acceptable?

## 🚀 Next Steps

Based on your testing, what should we prioritize next?
1. [ ] Visual styling (colors, backgrounds)
2. [ ] Icons and indicators
3. [ ] Conditional formatting for variances
4. [ ] Add formulas to other views (Policy Revenue Ledger)
5. [ ] Other: _______________________

---

**Testing Complete**: ⬜ Yes ⬜ No  
**Date/Time**: _________________  
**Overall Assessment**: ⬜ Working as Expected ⬜ Needs Fixes ⬜ Needs Enhancements

*Please share your completed checklist and any screenshots of issues found.*