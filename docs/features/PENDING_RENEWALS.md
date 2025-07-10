# Pending Policy Renewals Feature

**Last Updated**: July 10, 2025

## Current Implementation

The Pending Policy Renewals feature is now live with the following capabilities:

### Key Features:
1. **Automatic Renewal Detection**: Identifies policies expiring within 60 days
2. **Policy Term Support**: Uses actual policy terms (3, 6, 9, 12 months) for accurate renewal calculations
3. **Transaction Type Filtering**: Only considers NEW and RWL policies for renewal
4. **Batch Operations**: Select multiple policies for renewal at once

### How It Works:
1. **Data Source**: Reads from the `policies` table
2. **Filtering Logic**:
   - Transaction Type must be "NEW" or "RWL"
   - Expiration date (X-DATE) within next 60 days
   - Groups by Policy Number to find latest transaction
3. **Renewal Calculation**:
   - New Effective Date = Previous policy's Expiration Date
   - New Expiration Date = New Effective Date + Policy Term months
   - If no Policy Term specified, defaults to 6 months

### Recent Enhancements (July 10, 2025):
- Added Policy Term field to database and UI
- Updated renewal calculation to use actual policy terms instead of hardcoded 6 months
- 98 existing policies automatically assigned terms based on date calculations

---

## Original Design Document

# Pending Policy Renewals – Master Design V2

## Phase 1: Foundational Setup (Safe Scaffolding)
- **Step 1.1: Create `renewal_history` Table:** 
  - Create a new table in the database to store a log of all renewal actions.
  - This is a non-destructive operation and provides the necessary structure for logging renewals later.
- **Step 1.2: Add Sidebar Navigation:** 
  - Add "Pending Policy Renewals" to the sidebar navigation list in `commission_app.py`.
- **Step 1.3: Create Placeholder Page:** 
  - Create an empty placeholder function for the "Pending Policy Renewals" page.
  - This ensures the app remains fully functional and that we have a dedicated section to build upon.

## Phase 2: Core Data Logic (In-Memory, No UI)
- **Step 2.1: Develop Renewal Identification Logic:** 
  - Create a new, isolated function to identify policies due for renewal.
  - This function will perform the core data manipulation in memory without affecting the UI:
    - Read all policies into a DataFrame.
    - Filter for "NEW" and "RWL" transaction types.
    - Group by policy number and find the latest transaction.
    - Calculate the new policy term dates based on the original term length.
- **Step 2.2: Implement Data Duplication:** 
  - Create a function that takes the identified policies and generates a new DataFrame of pending renewals, ready for display.

## Phase 3: User Interface (Display & Interaction)
- **Step 3.1: Display Pending Renewals:** 
  - Integrate the logic from Phase 2 to display the generated list of pending renewals in a `st.data_editor` on the new page.
- **Step 3.2: Add Selection and Action Buttons:** 
  - Add checkboxes to each row for batch selection.
  - Implement the "Renew Selected" and "Delete Selected" buttons.
  - Initially, these buttons will only display the selected rows to confirm the logic is working correctly.

## Phase 4: Backend Functionality (Connecting Actions to Database)
- **Step 4.1: Implement "Renew" Action:** 
  - Connect the "Renew Selected" button to a function that:
    - Adds the selected pending renewals as new transactions to the main `policies` table.
    - Logs the details of each renewal into the `renewal_history` table.
- **Step 4.2: Implement "Delete" Action:** 
  - Connect the "Delete Selected" button to a function that removes the selected rows from the *in-memory* list of pending renewals, ensuring the main database is untouched.

## Phase 5: Finalization and Refinement
- **Step 5.1: Comprehensive Testing:** 
  - Thoroughly test all aspects of the new page, including edge cases like policies with no expiration date, batch actions, and data validation.
- **Step 5.2: Code Cleanup and Documentation:** 
  - Review the new code for clarity, add comments where necessary, and ensure it adheres to the project's existing style and conventions.
