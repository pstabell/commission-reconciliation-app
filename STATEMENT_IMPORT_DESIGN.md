# Statement Import Design
**Created**: July 5, 2025  
**Purpose**: Enable bulk import of commission statements from Excel files to streamline reconciliation

## 🎯 Core Concept

Transform the manual statement entry process into an automated import system that:
- **Reads Excel statements** from agencies/employers
- **Matches transactions** to existing policies
- **Creates -STMT- entries** automatically
- **Handles mismatches** gracefully
- **Maintains batch integrity** per statement

## 📊 Statement Import Workflow

### 1. Upload & Preview
- User uploads Excel/CSV statement file
- System detects columns and shows preview
- User maps statement columns to system fields
- Save mapping for future use (per agency)

### 2. Transaction Matching
- **Primary Match**: Policy Number + Customer Name + Effective Date
- **Secondary Match**: Customer Name + Effective Date + Commission Amount (within tolerance)
- **Fuzzy Matching**: Handle name variations (see Enhanced Matching section)
- **Match Confidence**: Show percentage confidence for each match
- **Policy Term Validation**: Ensure matching the correct policy term/renewal
- **Interactive Matching**: Allow manual selection when multiple potential matches exist

### 3. Review & Adjust
- Display all statement rows with match status:
  - ✅ **Matched** - Found corresponding transaction
  - ⚠️ **Partial Match** - Needs confirmation
  - ❌ **Unmatched** - No transaction found (option to create)
  - 🔄 **Duplicate** - Multiple possible matches
  - ➕ **Create & Match** - Add missing transaction then reconcile
- Allow manual matching for unclear items
- **Create missing transactions inline** without leaving import
- Show total matched vs unmatched amounts

### 4. Import Execution
- Create original transactions for any missing entries (if selected)
- Create -STMT- entries for all matched transactions
- Use single reconciliation_id for entire statement
- Set STMT DATE from file or user input
- Generate import summary report with:
  - Created transactions (new originals)
  - Reconciled transactions (-STMT- entries)
  - Skipped/unmatched items

## 💡 Create & Reconcile Workflow

### Missing Transaction Handling
When a statement contains commissions for transactions not in the database:

1. **Inline Creation Form**
   - Pre-fills data from statement (customer, policy, dates, amounts)
   - Calculates expected commission based on entered rates
   - Flags discrepancies between calculated and statement amounts
   - Option to use statement amount (common for special deals)

2. **Transaction Types Support**
   - **NEW**: New business - full effective date
   - **RWL/RENEWAL**: Renewal - matches prior term pattern
   - **END**: Endorsement - uses policy effective date
   - **CXL**: Cancellation - uses effective date with X-DATE

3. **Smart Defaults**
   - Transaction Type defaults based on amount patterns
   - Commission percentages based on similar policies
   - Effective dates validated against statement date

4. **Batch Creation**
   - Create multiple missing transactions at once
   - Review all before proceeding
   - Option to skip individual transactions
   - Export skipped items for later review

### Workflow Benefits
- No need to leave reconciliation process
- Maintains context from statement
- Reduces manual data entry
- Creates complete audit trail
- Ensures all statement items are addressed

## 🗂️ Expected Statement Formats

### Common Agency Statement Columns
```
Policy Number | Client Name | Premium | Agency Comm | Agent Paid | Payment Date | Policy Date
ABC123       | John Smith  | $1,000  | $200.00     | $100.00    | 06/30/2024  | 01/15/2024
DEF456       | Jane Doe    | $2,000  | $400.00     | $200.00    | 06/30/2024  | 03/01/2024
```
Note: "Agency Comm" is what the agency received (gross), "Agent Paid" is what you received (net)

### Flexible Column Mapping
- **Required Fields**:
  - Customer/Client Name
  - Policy Number
  - Effective Date (to match correct term)
  - **Agent Paid Amount (STMT)**: Your commission payment - PRIMARY RECONCILIATION FIELD
- **Highly Recommended**:
  - **Agency Comm Received (STMT)**: Agency's gross commission - FOR AUDIT/VERIFICATION
- **Optional Fields**:
  - Policy Type
  - Transaction Type (NEW/RWL/END/CXL)
  - Premium Amount
  - X-DATE (Expiration/Cancellation Date)
  - Notes/Description

## 🔧 Technical Implementation

### Column Mapping Storage
```python
agency_mappings = {
    "Agency ABC": {
        "Policy Number": "Policy #",
        "Customer": "Client Name", 
        "Agency Comm Received (STMT)": "Commission Paid",
        "STMT DATE": "Payment Date"
    }
}
```

### Matching Algorithm
```python
def match_statement_row(row, existing_transactions):
    # 1. Exact match: Policy Number + Effective Date
    if row['Policy Number'] and row['Effective Date']:
        policy_matches = find_by_policy_and_date(
            row['Policy Number'], 
            row['Effective Date']
        )
        if len(policy_matches) == 1:
            return {"match": policy_matches[0], "confidence": 100}
    
    # 2. Enhanced Customer Name Matching
    customer_name = row['Customer']
    potential_matches = []
    
    # 2a. First word match (handles "Barboun" → "Barboun, Thomas")
    first_word = customer_name.split()[0] if customer_name else ""
    if first_word:
        first_word_matches = find_customers_starting_with(first_word)
        potential_matches.extend(first_word_matches)
    
    # 2b. Contains match (handles "RCM" → "RCM Construction of SWFL LLC")
    if len(customer_name) >= 3:
        contains_matches = find_customers_containing(customer_name)
        potential_matches.extend(contains_matches)
    
    # 2c. Business name normalization (remove LLC, Inc, Corp, etc.)
    normalized_name = normalize_business_name(customer_name)
    if normalized_name != customer_name:
        normalized_matches = find_by_normalized_name(normalized_name)
        potential_matches.extend(normalized_matches)
    
    # If single match found with good criteria, auto-match
    if len(potential_matches) == 1:
        return {"match": potential_matches[0], "confidence": 85}
    
    # If multiple matches, return for interactive selection
    elif len(potential_matches) > 1:
        return {
            "match": None, 
            "potential_matches": potential_matches,
            "confidence": 0,
            "needs_manual_selection": True
        }
    
    # 3. Original fuzzy matching as fallback
    if fuzzy_matches := find_by_fuzzy_name(row['Customer'], threshold=70):
        return {
            "match": None,
            "potential_matches": fuzzy_matches,
            "confidence": 0,
            "needs_manual_selection": True
        }
    
    return {"match": None, "confidence": 0}
```

### Business Name Normalization
```python
def normalize_business_name(name):
    # Remove common suffixes
    suffixes = ['LLC', 'L.L.C.', 'Inc', 'Inc.', 'Corp', 'Corporation', 
                'Ltd', 'Limited', 'PA', 'P.A.', 'PC', 'P.C.']
    
    normalized = name
    for suffix in suffixes:
        # Case-insensitive removal from end of string
        pattern = rf'\s*{re.escape(suffix)}\s*$'
        normalized = re.sub(pattern, '', normalized, flags=re.IGNORECASE)
    
    # Remove extra whitespace and punctuation
    normalized = ' '.join(normalized.split())
    return normalized.strip()
```

### Import Process
```python
def import_statement(file, mapping, statement_date):
    batch_id = f"IMPORT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    results = {"matched": 0, "unmatched": 0, "total_amount": 0}
    
    for row in statement_rows:
        match_result = match_statement_row(row, unreconciled_transactions)
        
        if match_result['confidence'] >= 80:  # Configurable threshold
            create_stmt_entry(
                original_transaction=match_result['match'],
                amount=row['Commission'],
                statement_date=statement_date,
                batch_id=batch_id
            )
            results['matched'] += 1
        else:
            results['unmatched'] += 1
    
    return results
```

## 🎯 User Interface Design

### Import Wizard Steps

#### Step 1: Upload File
```
📤 Upload Statement File
[Drag and drop or click to browse]
Supported formats: .xlsx, .xls, .csv

Statement Date: [06/30/2024]
Agency: [Select Agency ▼]
```

#### Step 2: Column Mapping
```
Map Statement Columns to System Fields:

Statement Column          →  System Field
Commission Amount         →  [Agency Comm Received (STMT) ▼]
Client Name              →  [Customer ▼]
Policy #                 →  [Policy Number ▼]

Note: Statement Date is set from the date entered at top of form

[✓] Save mapping for future imports
```

**UI Fix Needed**: Remove duplicate text in field mapping - shows "Agency Comm Received (STMT) (Agency Comm Received (STMT))" - should just show field name once.

#### Step 3: Review Matches - Enhanced Interactive Matching
```
Statement Import Preview (25 rows)

Status  | Customer      | Policy  | Eff Date   | Type | Statement Amt | Matched Trans | Action
✅      | John Smith    | ABC123  | 01/15/2024 | NEW  | $100.00      | A1B2C3D      | Ready
🔍      | Barboun       | GHI456  | 02/01/2024 | RWL  | $150.00      | 2 possible   | [Select Match]
🔍      | RCM Construction | JKL789 | 03/01/2024 | NEW | $200.00     | 3 possible   | [Select Match]
❌      | New Client    | XYZ789  | 06/01/2024 | NEW  | $200.00      | -            | [Create & Match]
🔄      | Jane Doe      | DEF456  | 03/01/2024 | RWL  | $200.00      | Multiple     | [Select Match]

Matched: 18/25 transactions ($1,800.00)
Unmatched: 5 transactions ($500.00) - 3 can be created
Multiple Matches: 2 transactions ($400.00)

[✓] Create missing transactions before reconciling (3 transactions)

[Review Details] [Proceed with Import] [Cancel]
```

#### Interactive Match Selection (When Multiple Matches Found)
```
Statement Transaction: Barboun | GHI456 | $150.00

🔍 Potential Customer Matches:
○ Barboun, Thomas (2 transactions with balance)
○ Barboun Properties LLC (1 transaction with balance)
○ Barboun & Associates (0 transactions with balance)

[Select: Barboun, Thomas ▼]

Available Transactions for Selected Customer:
□ Policy: GHI456 | Eff: 02/01/2024 | Balance: $150.00 | Type: RWL ← Best Match
□ Policy: GHI123 | Eff: 01/15/2023 | Balance: $75.00 | Type: NEW
□ Policy: GHI789 | Eff: 08/01/2024 | Balance: $200.00 | Type: END

[Confirm Selection] [Search Different Customer] [Create New]
```

#### Manual Customer Search Interface
```
Can't find the right match? Search for customer:

🔍 [Search customers...                    ]

Search Results:
- RCM Construction of SWFL LLC (Found: "RCM Construction")
- RCM Property Management
- Richardson Construction Management

[Select Customer] [Show All Customers]
```

#### Create Missing Transaction (Inline)
```
Create New Transaction for Statement Match:

Customer: New Client                    Policy Number: XYZ789
Policy Type: [Select ▼]                Transaction Type: [NEW ▼]
Effective Date: 06/01/2024             X-Date: [____]
Premium Sold: $2,000.00                Gross Comm %: 10%
Agent Comm %: 50%                      Calculated Comm: $100.00
Statement Shows: $200.00               

⚠️ Commission mismatch: Calculated ($100) vs Statement ($200)
[✓] Use statement amount for this transaction

[Create & Continue] [Skip This] [Enter Manually]
```

#### Step 4: Import Confirmation
```
✅ Import Successful!

Imported: 20 transactions
Total Amount: $2,000.00
Batch ID: IMPORT-20240705-143022

Unmatched Items: 5
[Download Unmatched Report]

[View Reconciliation] [Import Another]
```

## 📋 Implementation Plan

### Phase 1: Basic Import
- [ ] File upload interface
- [ ] Excel/CSV parsing
- [ ] Simple column mapping
- [ ] Exact match only
- [ ] Basic import summary

### Phase 2: Smart Matching
- [ ] Fuzzy name matching
- [ ] Amount tolerance matching
- [ ] Confidence scoring
- [ ] Manual match override
- [ ] Saved column mappings

### Phase 3: Advanced Features
- [ ] Multi-statement batch import
- [ ] Duplicate detection
- [ ] Partial payment handling
- [ ] Import history tracking
- [ ] Undo import capability

## 🔴 Critical Discovery - July 2025

### Transaction Lookup Issue
During implementation testing, discovered that the import matching fails to find transactions that clearly exist:

**Test Case**: 
- Customer: "RCM Construction of SWFL LLC"
- Transaction: EFI6155 with $57.19 balance
- Result: Shows "No transactions with balance" despite transaction being visible in Unreconciled Transactions tab

**Root Cause Analysis**:
1. Import matching builds its own `existing_lookup` dictionary
2. This lookup may have:
   - Stale/cached data from before edits
   - Customer key formatting mismatches
   - Missing transactions due to filtering logic
3. Meanwhile, "Unreconciled Transactions" tab shows correct data

**Recommended Solution**:
Instead of building a separate lookup system, reuse the exact same query/logic that powers the "Unreconciled Transactions" tab:

```python
# Current approach (problematic)
existing_lookup = {}  # Build custom dictionary
# ... complex logic to populate lookup ...

# Better approach
unreconciled_transactions = get_unreconciled_transactions()  # Same as tab
# Filter and match directly against this proven data source
```

This ensures consistency between what users see in Unreconciled tab and what's available for matching.

## ⚠️ Important Considerations

1. **Data Validation**
   - Verify statement totals before import
   - Check for duplicate imports
   - Validate date formats and match policy terms
   - Handle negative amounts (reversals)
   - **Critical**: Prevent reconciling wrong policy term

2. **Policy Term Matching**
   - Always require effective date for matching
   - Allow configurable date tolerance (e.g., ±30 days)
   - Flag when multiple terms exist for same policy
   - Show policy term history during manual matching

3. **Error Handling**
   - Clear error messages for mismatches
   - Highlight date mismatches specifically
   - Option to save and resume import session
   - Export unmatched items for manual review

4. **Audit Trail**
   - Log all import activities
   - Track who imported what and when
   - Link to source file for reference
   - Record matching decisions and overrides

5. **Performance**
   - Handle large statements (1000+ rows)
   - Show progress during import
   - Allow background processing

## 🔍 Enhanced Name Matching Features

### Smart Name Recognition
1. **First Word Matching**
   - "Barboun" matches "Barboun, Thomas"
   - "Smith" matches "Smith, John and Mary"
   - Handles personal names with suffixes

2. **Business Name Intelligence**
   - "RCM" matches "RCM Construction of SWFL LLC"
   - Ignores legal suffixes (LLC, Inc, Corp, Ltd)
   - Handles DBA names and variations

3. **Partial Match Strategies**
   - Contains: "Construction" finds all construction companies
   - Starts with: "Bar" finds "Barboun", "Barton", etc.
   - Acronym detection: "ABC" matches "American Business Corp"

4. **Interactive Resolution**
   - Shows all potential matches with transaction counts
   - Displays available transactions with balances
   - Allows manual customer search
   - Option to create new if no match exists

### Match Confidence Levels
- **100%**: Policy Number + Customer + Effective Date match
- **90%**: Customer + Effective Date + Amount match (±5%)
- **85%**: Single customer match via smart name recognition
- **75%**: Fuzzy match requiring confirmation
- **Manual**: Multiple matches requiring user selection

## 🚀 Quick Win Implementation

For immediate value, start with:
1. Basic Excel upload
2. Simple column selection  
3. Exact policy number + date matching
4. **Inline creation for missing transactions**
5. Import matched + created transactions
6. Export any skipped items

This enhanced approach would:
- Handle 90% of use cases  
- Eliminate the back-and-forth of manual entry
- Create a complete reconciliation in one session
- Maintain full audit trail of what was created vs matched

## 🔄 Major Updates - July 5, 2025

### Critical Discovery: Dual-Purpose Reconciliation

During implementation testing, user clarified a fundamental misunderstanding about the reconciliation system:

**The Problem**: 
- Initial implementation focused on reconciling agency's gross commission (what the agency received)
- But the PRIMARY purpose is reconciling the agent's commission payments (what YOU received)
- User said: "I do need a simple tracking of the 'Agency Comm Received (STMT)'... but... the app's main reconciling feature... is tracking what the agent gets"

**The Solution**:
The reconciliation system now has a dual purpose:
1. **Primary**: Reconcile agent's commission payments (Agent Paid Amount STMT)
2. **Secondary**: Track agency's gross commission for audit verification

This enables:
- Proper reconciliation of YOUR payments (not the agency's)
- Audit capability to verify correct commission splits
- Detection of underpayments (e.g., agency got $100 but only paid you $45 instead of $50)

### Implementation Changes Made

#### 1. Field Priority Restructuring
**Before**: Agency Comm Received was the primary required field
**After**: 
- Agent Paid Amount (STMT) = Primary required field for reconciliation
- Agency Comm Received (STMT) = Required field for audit trail

**Reasoning**: The reconciliation should match what appears on YOUR bank statement, not what the agency received.

#### 2. Totals Row Handling
**Discovery**: Commission statements often include a "Totals" row that shouldn't be matched
**Solution**: 
- Skip rows where customer name contains "total", "totals", "subtotal", etc.
- Use the totals row value as a verification check only
- Display statement total vs. reconciliation total for checks and balances

**User Quote**: "The only reason I would want the total 'Pay Amount' from the commission statement on the reconciliation page is so I can verify all transactions have been reconciled correctly."

#### 3. Column Mapping Persistence
**Problem**: Users had to re-map columns every time they imported from the same agency
**Solution**: Added save/load functionality for column mappings
- Save mappings with custom names (e.g., "ABC Insurance Statement")
- Load saved mappings with column validation
- Delete unwanted mappings

**Implementation**: Stored in session state with creation timestamps

### Technical Implementation Details

#### Enhanced Name Matching (Previously Implemented)
The system uses multiple strategies to handle real-world name variations:
- **First Word Match**: "Barboun" → "Barboun, Thomas"
- **Business Name Normalization**: "RCM Construction" → "RCM Construction of SWFL LLC"
- **Interactive Selection**: When multiple matches exist

#### Transaction Lookup Fix (Previously Implemented)
Resolved critical issue where import couldn't find transactions even with exact matches:
- **Root Cause**: Import built its own lookup dictionary with potential stale data
- **Solution**: Reuse the exact same balance calculation logic as "Unreconciled Transactions" tab

### Current Required Fields (Updated July 5, 2025)
1. **Customer/Client Name** - For matching
2. **Policy Number** - For exact matching
3. **Effective Date** - To match correct policy term
4. **Agent Paid Amount (STMT)** - YOUR commission payment (PRIMARY)
5. **Agency Comm Received (STMT)** - Agency's gross commission (AUDIT)

### Lessons Learned

1. **Always Clarify the User's Perspective**
   - We initially built from the agency's perspective
   - User needed it from the agent's perspective
   - The dual-purpose design satisfies both needs

2. **Real-World Data is Messy**
   - Totals rows need special handling
   - Name matching needs to be fuzzy but controlled
   - Users need to save time with repeated imports

3. **Verification is Critical**
   - Statement totals provide essential checks and balances
   - Both agent and agency amounts enable audit trails
   - Visual feedback helps users spot discrepancies quickly

---

*This design enables efficient bulk reconciliation while maintaining data integrity and providing flexibility for various statement formats. The dual-purpose approach ensures both accurate payment tracking and audit capability.*