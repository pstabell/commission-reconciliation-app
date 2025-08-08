# Reconciliation System - Comprehensive Documentation
**Created**: July 4, 2025  
**Last Updated**: August 5, 2025  
**Purpose**: Complete reference for the commission reconciliation system implementation

## Table of Contents
1. [Overview](#overview)
2. [Core Concepts](#core-concepts)
3. [Transaction Types & Structure](#transaction-types--structure)
4. [Balance-Based Reconciliation](#balance-based-reconciliation)
5. [Implementation Phases](#implementation-phases)
6. [Statement Import System](#statement-import-system)
7. [Matching Logic & Fixes](#matching-logic--fixes)
8. [Technical Implementation](#technical-implementation)
9. [Testing & Validation](#testing--validation)
10. [Future Enhancements](#future-enhancements)

## Overview

The reconciliation system transforms commission tracking into a true double-entry accounting ledger that:
- **Tracks commission earnings** (credits) and **payments received** (debits)
- **Maintains outstanding balances** until fully reconciled
- **Provides dual-purpose tracking** for both agent payments and agency receipts
- **Enables bulk import** from commission statements
- **Ensures data integrity** through immutable reconciliation records

### Key Achievement
The system successfully implements professional accounting principles while remaining user-friendly for non-accountants. It solves the critical business need of tracking what agents are owed versus what they've been paid.

## Core Concepts

### Double-Entry Accounting Model
- **Credits (Original Transactions)**: Commission earned when policy is sold/renewed
- **Debits (Reconciliation Transactions)**: Commission payments received from agency
- **Balance**: Outstanding amount owed (Credit - Debit)
- **Visibility**: Transactions remain visible until balance = $0

### Dual-Purpose Reconciliation

**Primary Purpose - Agent Payment Reconciliation**
- Tracks what YOU (the agent) actually received
- Matches payments to your bank deposits
- Drives the reconciliation matching and totals

**Secondary Purpose - Commission Audit Trail**
- Records what the agency received from carriers
- Enables verification of correct commission splits
- Helps detect calculation errors or underpayments

**Example**: Agency receives $100, pays agent $45 instead of $50 → System flags $5 discrepancy

## Transaction Types & Structure

### 1. Original Transactions (Credits)
- **Transaction ID**: `A1B2C3D` (7 characters: mixed letters & numbers)
- **Purpose**: Record commission earned
- **Transaction Types**: 
  - **NEW**: New business commission
  - **RWL**: Renewal commission
  - **END**: Endorsement commission
  - **CAN**: Cancellation (negative commission/chargeback)
  - **PMT**: Payment-driven commission (as-earned)
- **Behavior**: Visible while balance > $0, can be partially reconciled multiple times

### 2. Reconciliation Transactions (Debits)
- **Transaction ID**: `X7Y8Z9Q-STMT-20250704`
  - Base: 7-character unique ID
  - Suffix: `-STMT-` indicates reconciliation
  - Date: Statement date (YYYYMMDD)
- **Key Fields**:
  - Agent Paid Amount (STMT): Primary reconciliation field
  - Agency Comm Received (STMT): Audit verification field
- **Behavior**: Permanently locked, grouped by batch
- **Transaction Type Mapping**: Applied during import (see [TRANSACTION_TYPE_MAPPING.md](TRANSACTION_TYPE_MAPPING.md))

### 3. Import-Created Transactions (NEW in v3.6.3)
- **Transaction ID**: `D5D19K7-IMPORT`
- **Purpose**: Placeholder for payments without matching policy transactions
- **Created**: Automatically during reconciliation when payment has no match
- **Behavior**: 
  - Partially editable (premium/commission fields only)
  - Payment fields protected (read-only)
  - Cannot be deleted to preserve payment history
  - Shows comprehensive explanation box when editing
  - Description contains "Created from statement import"
- **Use Case**: Complete premium and commission data to calculate expected vs actual

### 4. Adjustment Transactions
- **Transaction ID**: `M3N4P5R-ADJ-20250715`
- **Purpose**: Correct errors without modifying originals
- **Behavior**: Creates audit trail, locked once created

### 5. Void Transactions
- **Transaction ID**: `K9L8M7N-VOID-20250720`
- **Purpose**: Reverse entire reconciliation batch
- **Behavior**: Creates negative entries, maintains integrity

## Balance-Based Reconciliation

### Workflow Overview

1. **Transaction Selection**
   - Drill-down: Customer → Policy Type → Policy Number → Effective Date
   - Shows only transactions with outstanding balances
   - Displays full transaction details including current balance

2. **Batch Building**
   - Add selected transactions to reconciliation batch
   - Running total updates in real-time
   - Visual indicator when batch total = statement total

3. **Batch Reconciliation**
   - Entire batch reconciled as one unit
   - All transactions receive same reconciliation_id
   - Creates multiple -STMT- entries maintaining grouping

4. **Error Correction**
   - Void entire batches with -VOID- transactions
   - Create adjustments with -ADJ- transactions
   - Full audit trail maintained

### Example Workflow
```
Statement shows: $500 total commission paid

1. Select Transaction A: $120 balance → Add to batch
2. Select Transaction B: $180 balance → Add to batch  
3. Select Transaction C: $200 balance → Add to batch
4. Batch total: $500 ✓ Matches statement
5. Reconcile batch → Creates 3 -STMT- entries
```

## Implementation Phases

### ✅ Phase 1-5: Core System (COMPLETED)
All fundamental reconciliation features have been implemented:
- Transaction ID structure with suffixes
- Database schema with reconciliation columns
- Balance-based transaction visibility
- Drill-down selection interface
- Batch reconciliation with integrity checks
- Void and adjustment functionality
- Payment history tracking

### Phase 6: Visual Design & Polish (Pending)
- [ ] Field locking for reconciled transactions
- [ ] Visual batch grouping with color coding
- [ ] Consistent gray styling for locked fields
- [ ] Batch status indicators

## Statement Import System

### Overview
The statement import feature enables bulk reconciliation from Excel/CSV files, dramatically reducing manual data entry while maintaining accuracy.

### Import Workflow

#### 1. Upload & Preview
- Upload Excel/CSV statement files
- Auto-detect columns with preview
- Map statement columns to system fields
- Save mappings for reuse

#### 2. Transaction Matching
**Primary Match**: Policy Number + Effective Date (100% confidence)
- Handles different date formats automatically
- Normalizes to YYYY-MM-DD for consistency

**Secondary Match**: Customer Name with smart matching
- **Name Reversal**: "Last, First" ↔ "First Last" (98%)
- **Business Normalization**: Removes LLC, Inc, etc. (95%)
- **First Word Match**: "Barboun" → "Barboun, Thomas" (90%)
- **Contains Match**: "RCM" → "RCM Construction" (85%)

**Interactive Selection**: When multiple matches exist
- Shows all potential customers
- Displays available transactions with balances
- Allows manual selection or search

#### 3. Review & Adjust
Match Status Indicators:
- ✅ **Matched**: Found corresponding transaction
- 🔍 **Multiple Matches**: Needs manual selection
- ❌ **Unmatched**: No transaction found
- ➕ **Create & Match**: Add missing transaction inline

#### 4. Import Execution
- Creates original transactions for missing entries
- Generates -STMT- entries for matched transactions
- Uses single batch ID for entire statement
- Produces detailed import summary

### Create & Reconcile Feature
When statement contains commissions for missing transactions:
1. **Inline Creation Form** pre-fills data from statement
2. **Smart Defaults** based on transaction patterns
3. **Validation** checks calculated vs statement amounts
4. **Batch Creation** for multiple missing transactions

### Column Mapping
**Required Fields**:
- Customer/Client Name
- Policy Number
- Effective Date
- Agent Paid Amount (STMT) - Primary
- Agency Comm Received (STMT) - Audit

**Optional Fields**:
- Policy Type
- Transaction Type
- Premium Amount
- Notes/Description

## Matching Logic & Fixes

### Critical Issues Resolved

#### 1. Date Format Mismatch (Fixed July 6, 2025)
**Problem**: Dates in different formats prevented matching
- Database: "05/22/2024" (MM/DD/YYYY)
- Statement: "2024-05-22 00:00:00" (ISO format)

**Solution**: Normalize all dates to YYYY-MM-DD before matching
```python
eff_date_normalized = pd.to_datetime(trans['Effective Date']).strftime('%Y-%m-%d')
policy_key = f"{trans['Policy Number']}_{eff_date_normalized}"
```

#### 2. Name Format Variations (Fixed July 6, 2025)
**Problem**: Different name formats couldn't match
- Database: "Thomas Barboun"
- Statement: "Barboun, Thomas"

**Solution**: Smart name matching with multiple strategies
```python
# Detect and reverse "Last, First" format
if "," in search_name:
    parts = search_name.split(",", 1)
    search_name_reversed = f"{parts[1].strip()} {parts[0].strip()}"
```

#### 3. Transaction Lookup Bug (Fixed July 5, 2025)
**Problem**: Import couldn't find existing transactions
- Root cause: Separate lookup dictionary with stale data

**Solution**: Reuse proven logic from Unreconciled Transactions tab

#### 4. Search Column Names (Fixed)
**Problem**: Search used underscores instead of spaces
- Looking for: `Transaction_ID`
- Actual column: `Transaction ID`

**Solution**: Updated search to use correct column names

### Current Matching Algorithm (Updated v3.9.4)

1. **Policy + Date Match** (100%): Exact policy number and effective date match
2. **Customer + Policy Match** (95%): Customer name match with correct policy number
3. **Customer + Amount Match** (90%): Customer name match with amount within 5% tolerance
4. **Customer Only Match**: Requires manual selection (no automatic matching)

#### Customer Name Matching Tiers:
- **Exact** (100%): Perfect string match
- **Name Reversal** (98%): "Last, First" → "First Last"
- **Business Normalized** (95%): Ignores LLC, Inc, etc.
- **First Word Match** (90%): Partial name matching
- **All Words Match** (88%): All words present in any order
- **Contains Match** (85%): Substring matching
- **Most Words Match** (82%): Most words match between names

#### Confidence Labels:
- **exact**: 99%+ confidence
- **high**: 95-98% confidence
- **good**: 90-94% confidence
- **moderate**: 85-89% confidence
- **low**: <85% confidence

### Enhanced Unmatched Transaction Display (Added v3.5.14)

When reviewing unmatched transactions, users now see comprehensive statement details:

#### Statement Details Section
- **Policy**: Policy number from statement
- **Effective Date**: Policy effective date  
- **Amount**: Agent commission amount
- **LOB/Chg**: Line of Business or Change indicator
- **Transaction**: Transaction type (NEW, RWL, END, etc.)
- **Rate**: Commission rate with smart percentage formatting

#### Technical Details
- Automatic detection of column variations (LOB/Chg, LOB, Tran, Transaction)
- Smart rate formatting (0.15 → 15%, 15 → 15%)
- Only displays fields with actual values
- Rate field added to optional column mappings

### Enhanced Reconciliation UI (Added v3.5.15)

Major improvements to reconciliation clarity and safety:

#### Force Match Warnings
- Clear red warning text when customer names don't match
- Transaction ID displayed: "Force match to A1B2C3D4"
- Smart logic: No warnings for high-confidence name reversals (≥95%)
- Warnings only appear for genuine mismatches

#### Create Transaction Labels
- Improved labels showing customer names
- Format: "Create new transaction for: [Customer Name]"
- Clear indication of what action will be taken

#### UI Safety Improvements
- Checkbox order flipped for safety
- "Create new" (safer) option on left
- "Force match" (riskier) option on right
- Pre-filled confirmation messages

#### Agency Comm Made Optional
- Moved from required to optional fields
- Positioned in right column
- Allows reconciliation without agency commission data
- Focuses on agent payment reconciliation

#### Extended Confirmation Display
- Success message delay increased from 2 to 4 seconds
- Ensures users can read confirmation details
- Better visibility of reconciliation results

### Manual Matching Feature (Added v3.5.9)

When automatic matching fails, users can now manually match transactions:

#### UI Elements
- **Customer Dropdown**: Pre-populated with potential matches and confidence scores
- **"Match transaction" Checkbox**: Allows manual customer selection
- **"Create as new transaction" Checkbox**: For genuine new transactions
- **Helpful Caption**: "*(Use for new policies or endorsements not yet in system)*"

#### Use Cases
1. **Name Format Mismatches**: "D'Alessandro, Nicole" → "Nicole D'Alessandro"
2. **Missing Transactions**: Endorsements not yet entered in system
3. **Negative Transactions**: Cancellations or refunds

#### Technical Implementation
- Manual matches store customer selection in session state
- System attempts to find matching transaction by customer/policy/date
- Falls back to customer-only match if no exact transaction found
- Handles missing fields gracefully with .get() methods

### Client ID Matching (Added v3.5.15)

A critical enhancement ensuring all new transactions created during reconciliation are properly linked to Client IDs:

#### The Problem
New transactions created during reconciliation import had no Client ID, breaking:
- Client-based reporting and filtering
- Dashboard client search functionality
- Overall data integrity and relationships

#### The Solution
Enhanced reconciliation UI with automatic client matching and selection:

1. **Automatic Client Lookup**
   - When creating new transactions, system searches for existing clients
   - Uses same smart matching logic as transaction matching
   - Shows exact matches and similar client names

2. **Radio Button Selection Interface**
   ```
   🔍 Client Match Options:
   ○ Existing client found: [Matched Client Name] (ID: CL-XXXXXXXX)
   ○ Similar clients found:
     - Similar Client 1 (ID: CL-YYYYYYYY)
     - Similar Client 2 (ID: CL-ZZZZZZZZ)
   ○ Create new client for: [Statement Customer Name]
   ```

3. **Client Record Creation**
   - If no match exists, creates new client record
   - Auto-generates Client ID in format: CL-XXXXXXXX
   - Links all transactions to appropriate Client ID

#### Technical Implementation
```python
# Check for existing clients
exact_match = supabase.table('clients').select('*').eq('client_name', customer).execute()

# Find similar clients
similar_matches = find_potential_customer_matches(customer, is_client_search=True)

# Create new client if needed
if create_new_client:
    new_client_id = generate_client_id()  # CL-XXXXXXXX format
    new_client = {
        'client_id': new_client_id,
        'client_name': customer_name,
        'created_at': datetime.now()
    }
    supabase.table('clients').insert(new_client).execute()
```

#### Impact
- All new transactions now have proper Client IDs
- Maintains referential integrity in database
- Enables accurate client-based reporting
- Prevents orphaned transactions

## Technical Implementation

### Transaction ID Generation
```python
def generate_reconciliation_transaction_id(transaction_type="STMT", date=None):
    """Generate unique IDs with proper suffixes"""
    chars = string.ascii_uppercase + string.digits
    base_id = ''.join(random.choice(chars) for _ in range(7))
    
    if transaction_type == "STMT":
        return f"{base_id}-STMT-{date.strftime('%Y%m%d')}"
    elif transaction_type == "VOID":
        return f"{base_id}-VOID-{date.strftime('%Y%m%d')}"
    elif transaction_type == "ADJ":
        return f"{base_id}-ADJ-{date.strftime('%Y%m%d')}"
```

### Batch Reconciliation Logic
```python
# Only enable reconcile when batch matches statement exactly
if batch_total == statement_total and statement_total > 0:
    for transaction in batch:
        create_reconciliation_entry(transaction, batch_id)
```

### Business Name Normalization
```python
def normalize_business_name(name):
    suffixes = ['LLC', 'L.L.C.', 'Inc', 'Inc.', 'Corp', 'Corporation']
    normalized = name
    for suffix in suffixes:
        pattern = rf'\s*{re.escape(suffix)}\s*$'
        normalized = re.sub(pattern, '', normalized, flags=re.IGNORECASE)
    return normalized.strip()
```

### Database Schema
Key reconciliation columns:
- `reconciliation_status`: Current status
- `reconciliation_id`: Batch grouping ID
- `reconciled_at`: Timestamp
- `is_reconciliation_entry`: Boolean flag
- `STMT DATE`: Statement date for reconciliations

## Void and Adjustment Functionality

### Void Reconciliation Process
When voiding a reconciliation batch:
1. Creates negative -VOID- entries for each -STMT- transaction
2. Updates original transactions back to 'unreconciled' status
3. Maintains complete audit trail with void reason

### Double-Void Prevention (Added v3.9.5)
The system now prevents attempting to void an already-voided batch:
- **Validation Check**: Before showing void form, checks if `VOID-{batch_id}` already exists
- **Error Message**: "This batch has already been voided. You cannot void a batch twice."
- **Suggested Action**: "If you need to make corrections, please create an adjustment entry instead."
- **UI Behavior**: Void form is completely hidden when batch is already voided
- **Prevents**: Duplicate VOID entries and balance calculation errors

### Void Reason Field Styling (Added v3.9.5)
The void reason text area now has enhanced visibility:
- **Background**: Yellow (#fff3b0) matching app-wide input field styling
- **Border**: 2px solid darker yellow (#e6a800)
- **Label**: Bold font-weight (600) for emphasis
- **Purpose**: Makes the required field immediately visible to users

### Important: Agent vs Agency Amounts (Fixed v3.5.12)
The system tracks two commission amounts:
- **Agent Paid Amount (STMT)**: What YOU receive (primary reconciliation field)
- **Agency Comm Received (STMT)**: What the agency receives (audit/verification)

All reconciliation and void operations use Agent Paid Amount to ensure consistency.

### Void Entry Structure
```python
void_entry = {
    'Transaction ID': 'ABC123-VOID-20250711',
    'Agent Paid Amount (STMT)': -491.55,  # Negative to reverse
    'reconciliation_status': 'void',
    'reconciliation_id': 'VOID-{original_batch_id}',
    'NOTES': 'VOID: {reason}'
}
```

### Balance Calculation with Voids
The `calculate_transaction_balances` function includes both -STMT- and -VOID- entries:
```python
# Include both STMT and VOID entries
recon_entries = all_data[
    (all_data['Policy Number'] == policy_num) &
    (all_data['Effective Date'] == effective_date) &
    (all_data['Transaction ID'].str.contains('-STMT-|-VOID-', na=False))
]
```
This ensures voided transactions properly show as unreconciled again.

### Protection Mechanisms
```python
def is_reconciliation_transaction(transaction_id):
    """Identifies locked reconciliation transactions"""
    return any(suffix in str(transaction_id) 
              for suffix in ['-STMT-', '-VOID-', '-ADJ-'])
```

## Testing & Validation

### Current System Status
- Total database records: 178
- -STMT- transactions: 2
- -VOID- transactions: 0
- -ADJ- transactions: 0

### Test Transactions
1. **RD84L6D-STMT-20240630**: Thomas Barboun reconciliation
2. **F266CCX-STMT-20240630**: RCM Construction reconciliation

### Validation Checklist
- [x] Date format normalization working
- [x] Name reversal matching functional
- [x] Business name normalization active
- [x] Search functionality finding all transaction types
- [x] Edit protection preventing modification
- [x] Balance calculations accurate
- [x] Batch totals matching requirements

### Testing Recommendations
1. **Date Formats**: Test MM/DD/YYYY, M/D/YY, YYYY-MM-DD
2. **Name Variations**: "Smith, John", "O'Brien, Mary", business names
3. **Partial Payments**: $120 owed, $110 paid → $10 balance
4. **Batch Operations**: Void and adjustment creation

## Future Enhancements

### Immediate Priorities
1. **Field Locking Implementation**
   - Visual indicators for locked fields
   - Consistent gray styling (#F5F5F5 background)
   - Prevent accidental modifications

2. **Enhanced Import Features**
   - Fuzzy matching confidence scores
   - Bulk operations interface
   - Progress indicators for large files

3. **Reporting Capabilities**
   - Reconciliation summary reports
   - Audit trail exports
   - Balance aging analysis

### Long-term Enhancements
1. **Automation**
   - Auto-match suggestions
   - Recurring statement patterns
   - Email notifications

2. **Integration**
   - Direct bank feed connections
   - Agency system APIs
   - Accounting software export

3. **Advanced Matching**
   - Nickname handling ("Bob" → "Robert")
   - Soundex for phonetic matches
   - Machine learning for patterns

## Key Design Decisions

### Balance-Based Visibility
- Transactions visible until fully reconciled
- Supports partial payments naturally
- Leverages existing ledger calculations

### Batch Integrity
- Exact statement matching required
- All-or-nothing reconciliation
- Clean audit trail maintained

### User Experience
- Familiar drill-down navigation
- Real-time validation feedback
- Clear visual status indicators

### Data Integrity
- Immutable reconciliation records
- Comprehensive audit trail
- No modification of originals

## Critical Lessons Learned

### 1. User Perspective is Paramount
Initially built for agency perspective, but users needed agent perspective. The dual-purpose design now serves both needs effectively.

### 2. Real-World Data is Complex
- Names appear in multiple formats
- Dates vary by system
- Statements include summary rows
- Business names have many variations

### 3. Consistency is Key
Reusing proven logic (like balance calculations) across features prevents "works here but not there" issues.

### 4. Iterative Development Works
Each user feedback session led to immediate improvements, resulting in a system that truly meets user needs.

## Conclusion

The reconciliation system successfully transforms commission tracking into a professional accounting system while remaining accessible to non-accountants. Through careful design, iterative development, and attention to real-world requirements, it provides:

- **Accuracy**: True double-entry accounting with balance tracking
- **Efficiency**: Bulk import with smart matching
- **Integrity**: Immutable audit trail with batch controls
- **Flexibility**: Handles partial payments and corrections
- **Usability**: Intuitive interface with helpful automation

The system stands as a testament to the power of listening to users, understanding their actual needs, and building solutions that work with real-world data complexity.

---

## Recent Enhancements (v3.5.7 - v3.9.33)

### Transaction Type Mapping System (v3.9.33 - August 5, 2025)
Complete implementation of transaction type standardization:

#### Admin Panel Interface
- **New Tab**: Transaction Type Mapping in Admin Panel
- **Visual Management**: Add/remove mappings with dropdowns
- **Default Mapping**: STL → PMT (as-earned commission payments)
- **Configuration Storage**: `config_files/transaction_type_mappings.json`

#### Import Validation & Application
- **Pre-Import Validation**: Blocks imports with unmapped transaction types
- **Clear Error Messages**: Lists all unmapped types with next steps
- **Automatic Mapping**: Applied during transaction creation
- **Visual Feedback**: Shows "Mapped from 'STL' → 'PMT'" in UI

#### Transaction Type Philosophy
- **Policy Action Types** (NEW, RWL, END, CAN): Commission on policy events
- **Payment Types** (PMT): Commission on customer payments (as-earned)
- **Critical Distinction**: Separates policy-driven vs payment-driven commissions
- **See**: [TRANSACTION_TYPE_MAPPING.md](TRANSACTION_TYPE_MAPPING.md) for complete details

### Enhanced Reconciliation Data Copying (v3.9.1 - July 30, 2025)
Major improvements to reconciliation import and void operations:

#### Complete Field Copying During Reconciliation
- **Auto-copies all non-financial fields** from matched transactions
- Preserves factual data: Policy Type, Carrier Name, Dates, Client ID, etc.
- Excludes financial estimates (Premium Sold, commission calculations)
- Keeps only actual statement amounts (Agent/Agency payments)
- Eliminates manual data entry for reconciled transactions

#### Improved VOID Transaction IDs
- **Uses same base ID** as original transaction
- Example: `63Q4XX6-STMT-20240731` → `63Q4XX6-VOID-20240731`
- Makes transaction pairs immediately identifiable
- Improves batch delete matching verification

### Edit Reconciled Transactions (v3.9.0 - July 30, 2025)
New feature allowing corrections to reconciled transactions without voiding:
- **Checkbox Selection**: Select transactions to edit in Reconciliation History
- **Two-Column Form**: Non-editable reference fields (left) and editable fields (right)
- **Nine Editable Fields**: Transaction Type, Customer, Policy Number, Policy Type, Carrier Name, Effective Date, Agent Comm %, Policy Origination Date, X-DATE
- **Visual Design**: Yellow borders on editable fields using form context
- **Data Integrity**: Financial amounts remain locked to preserve reconciliation
- **See**: [EDIT_RECONCILED_TRANSACTIONS.md](./EDIT_RECONCILED_TRANSACTIONS.md) for full details

### Debug Mode for Unmatched Transactions (v3.5.13)
Enhanced troubleshooting capabilities for reconciliation matching:
- **Expandable Debug Section**: Shows ALL transactions for a customer
- **Balance Calculations**: Displays credit, debit, and balance for each transaction
- **Match Explanations**: Explains why transactions aren't available (e.g., zero balance)
- **Name Mismatch Detection**: Helps identify customer name variations

### Improved Customer Name Matching (v3.5.13)
Enhanced matching algorithms:
- **All Words Matching** (88% confidence): Matches any word order
- **Most Words Matching** (82% confidence): Handles partial matches
- **Examples**: "Adam Gomes" ↔ "Gomes, Adam" ↔ "Adam J. Gomes"
- **Business Name Handling**: Better recognition of company variations

### Statement Details Enhancement (v3.5.14)
Comprehensive information for unmatched transactions:
- **LOB/Chg Display**: Line of Business or Change type from statement
- **Transaction Type**: Shows NEW, RWL, END, etc. from statement
- **Commission Rate**: Smart percentage formatting (0.15 → 15%)
- **Automatic Detection**: Recognizes column variations (LOB, Tran, Rate)

### Transactions Requiring Attention Filter (v3.5.15)
New workflow for data completion:
- **Filter Button**: "Show Transactions Requiring Attention" on Edit Policies page
- **Smart Detection**: Finds transactions with payments but missing premium/commission
- **Quick Fix Workflow**: Uses existing edit interface for rapid data entry
- **Ledger Accuracy**: Ensures complete data for accurate reporting

### Agency Commission Made Optional (v3.5.15)
Simplified reconciliation requirements:
- **Moved to Optional**: Agency Comm no longer required for reconciliation
- **UI Positioning**: Placed in right column with other optional fields
- **Focus on Agent**: Emphasizes agent payment reconciliation
- **Flexibility**: Allows reconciliation without full agency data

### Financial Fields Exclusion (v3.9.34 - August 7, 2025)
Enhanced reconciliation import to prevent unwanted financial data:
- **Excluded by Default**: Financial calculation fields no longer imported unless explicitly mapped
- **Fields Affected**:
  - Premium Sold
  - Policy Taxes & Fees
  - Commissionable Premium
  - Policy Gross Comm %
  - Broker Fee
  - Broker Fee Agent Comm
- **Clean Imports**: These fields won't appear (not even as zeros) unless you specifically map them
- **Focus on Payments**: Reconciliation is about matching payments, not recalculating commissions

### UI Improvements (v3.9.34 - August 7, 2025)
Major improvements to reconciliation import interface:
- **Layout Fix**: Statement Details moved to top, customer matching below (as requested)
- **"Use" Button Positioning**: Buttons moved to far left, immediately next to customer names
- **Duplicate Prevention**: Added deduplication for unmatched transactions list
- **Key Naming Fix**: Fixed duplicate widget key errors in "Show all at once" mode
- **Clearer Association**: Use buttons now clearly associated with their respective customers

### Import Integrity Issues Identified (v3.9.34 - August 7, 2025)
- **Issue**: Orphaned batch records appearing in history even when import aborted
- **Root Cause**: Client records being created outside of atomic transaction batch
- **Expected Behavior**: System should validate everything before creating ANY records
- **Current State**: Three batch records showing as ACTIVE despite only one successful import
- **Note**: Full atomic transaction support exists but may have timing issues

---

*This comprehensive documentation consolidates all reconciliation system knowledge through August 7, 2025. For implementation of field locking features, refer to FORMULA_DESIGN.md which shares the visual design specifications.*