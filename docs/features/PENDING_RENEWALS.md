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
