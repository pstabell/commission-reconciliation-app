# Reconciliation History Tab Reorganization Plan

## Current Structure (Top to Bottom)
1. Date filter form (lines 8657-8689)
2. Summary metrics (lines 8704-8726)
3. View mode radio buttons (lines 8731-8736)
4. Data editor table (lines 8853-8861 for batch view, 9023-9066 for transaction view)
5. Edit form appears AFTER selection (lines 9071-9227)

## Problem
- When users select a transaction to edit, they must scroll down past the data table to see the edit form
- This creates a poor user experience, especially with many transactions

## Proposed New Structure
1. Date filter form (keep at top)
2. Summary metrics (keep position)
3. View mode radio buttons (keep position)
4. **Edit form section** (move here, show when transaction selected)
5. Data editor table (move below edit form)

## Implementation Strategy

### Step 1: Restructure the "All Transactions" view
- Move the edit form logic (lines 9071-9227) to appear BEFORE the data editor
- Keep the data editor at the bottom

### Step 2: Maintain State Management
- Preserve the checkbox selection state when form is displayed
- Ensure the selected transaction remains highlighted in the table

### Step 3: Visual Improvements
- Add a clear visual separator between the edit form and data table
- Consider collapsible sections or tabs within the reconciliation history

### Step 4: User Experience Enhancements
- Add "Cancel Edit" button to clear selection and hide form
- Auto-scroll to edit form when transaction is selected
- Show/hide edit form with smooth transitions

## Benefits
1. Users see the edit form immediately upon selection
2. No scrolling required to access edit functionality
3. Better workflow: select → edit → save without navigation
4. Data table remains visible for reference while editing

## Code Changes Required
1. Move the edit form block before the data editor
2. Add conditional rendering for the edit form
3. Ensure proper state management for selections
4. Test that all functionality remains intact