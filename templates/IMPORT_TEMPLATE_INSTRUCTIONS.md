# Policy Import Template Instructions

## Overview
The Policy Import Template helps you prepare your data for bulk import into the Agent Commission Tracker.

## Required Columns (Must Have)
1. **Client ID** - Unique identifier for the client (e.g., CL12345)
2. **Transaction ID** - Unique transaction ID (e.g., NEW001, END002)
3. **Policy Type** - Type of policy (e.g., AUTO, HOME, LIFE, COMM)

## All Available Columns

### Basic Information
- **Customer** - Customer/Insured name
- **Policy Number** - Policy number from carrier
- **Transaction Type** - NEW, RWL, END, CAN, BoR, PCH, etc.
- **Effective Date** - Effective date of the transaction (MM/DD/YYYY)

### Financial Information
- **Premium Sold** - Premium amount (positive for NEW/RWL, negative for CAN)
- **Policy Gross Comm %** - Gross commission percentage from carrier
- **Agency Estimated Comm/Revenue (CRM)** - Agency commission amount
- **Agent Comm %** - Agent commission percentage (e.g., 50 for new, 25 for renewal)
- **Total Agent Comm** - Total agent commission amount

### Carrier Information
- **Carrier Name** - Name of insurance carrier
- **MGA** - Managing General Agent name (or "Direct" if no MGA)

### Important Dates
- **Policy Origination Date** - Original policy start date (MM/DD/YYYY)
- **X-DATE** - Policy expiration date (MM/DD/YYYY)
- **STMT Date** - Statement/reconciliation date (MM/DD/YYYY)

### Payment & Additional Info
- **AS_EARNED_PMT_PLAN** - FULL, 12-PAY, 6-PAY, 4-PAY, 2-PAY, etc.
- **Agency Comm Received (STMT)** - Commission received from carrier (for reconciliation)
- **Agent Paid Amount (STMT)** - Amount paid to agent (for reconciliation)
- **Prior Policy Number** - Previous policy number (for renewals/rewrites)
- **NOTES** - Any notes or comments
- **Broker Fee** - Broker fees charged
- **Policy Taxes & Fees** - Policy taxes and fees
- **Policy Term** - Policy term number (1 for first term, 2 for second term/renewal, etc.)
- **Policy Checklist Complete** - Yes/No indicating if all required documents are complete

## Transaction Type Examples
- **NEW** - New business
- **RWL** - Renewal
- **END** - Endorsement (policy change)
- **CAN** - Cancellation
- **BoR** - Broker of Record change
- **PCH** - Policy change
- **REWRITE** - Policy rewrite
- **STL** - ?

## Tips for Successful Import
1. **Dates** - Use MM/DD/YYYY format (e.g., 01/15/2024)
2. **Numbers** - Don't use currency symbols ($) or commas
3. **Percentages** - Enter as numbers (15 not 15%)
4. **Transaction IDs** - Must be unique across your entire database
5. **Empty cells** - Leave blank for optional fields
6. **Negative amounts** - Use negative numbers for cancellations

## Column Name Variations
The import tool recognizes common variations:
- `Client ID` = `Client_ID`, `ClientID`, `client_id`
- `Transaction ID` = `Transaction_ID`, `TransactionID`
- `Agent Comm %` = `Agent Comm`, `Agent_Comm_%`
- Spaces, underscores, and case don't matter!

## Example Data Included
The template includes 5 example transactions:
1. NEW - New auto policy
2. NEW - New home policy
3. END - Endorsement adding coverage
4. RWL - Renewal with new policy number
5. CAN - Cancellation with negative amounts

## After Import
- Use "Delete Last Import" if you need to undo
- Check Edit Policy Transactions to verify data
- Run reports to ensure calculations are correct