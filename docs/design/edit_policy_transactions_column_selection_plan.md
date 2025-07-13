# Master Plan: Add Column Selection & Templates to Edit Policy Transactions Page

## Overview
Implement a column selection and template management system for the Edit Policy Transactions page, similar to the one on Policy Revenue Ledger Reports page, affecting only the table display without impacting the edit form.

## Phase 1: Analysis & Preparation
1. **Study existing implementation**
   - Analyze the Column Selection & Templates feature in Policy Revenue Ledger Reports
   - Identify reusable components and patterns
   - Note any page-specific customizations needed

2. **Identify requirements**
   - List all columns available in Edit Policy Transactions table
   - Determine default visible columns
   - Plan template storage mechanism (session state)

## Phase 2: UI Components
1. **Add Column Selection Section**
   - Create expandable section above the table
   - Implement multi-column checkbox layout for column selection
   - Add "Select All" / "Deselect All" buttons

2. **Add Template Management**
   - Template name input field
   - Save Template button
   - Load Template dropdown
   - Delete Template functionality
   - Default templates (e.g., "Essential Info", "Financial View", "Full Details")

## Phase 3: Core Functionality
1. **Column Visibility Logic**
   - Track selected columns in session state
   - Filter dataframe columns based on selection
   - Preserve column order preferences

2. **Template Operations**
   - Save current column selection with custom name
   - Load saved templates to update column selection
   - Delete unwanted templates
   - Persist templates in session state

3. **Integration with Existing Table**
   - Apply column filtering to the data editor
   - Maintain all existing functionality (search, filters, edit buttons)
   - Ensure formula calculations still work

## Phase 4: Enhancement & Polish
1. **User Experience**
   - Remember last used column selection
   - Add helpful tooltips
   - Show column count indicator

2. **Default Templates**
   - "Quick View" - Essential columns only
   - "Commission Focus" - Financial and commission columns
   - "Policy Details" - Policy-related columns
   - "Full View" - All columns

## Implementation Notes
- Use session state to store column preferences and templates
- Ensure the edit form continues to access all data fields
- Maintain compatibility with existing search and filter features
- Keep the implementation modular for potential reuse on other pages
- Session state keys will be unique (e.g., `edit_policies_column_templates`) to avoid conflicts
- No impact on other pages - completely isolated to Edit Policy Transactions page

## Future Considerations
- Could be extended to other data table pages if successful
- Consider saving templates to database for persistence across sessions
- Add import/export functionality for sharing templates between users