# Policy Revenue Ledger Reports - Compact View Toggle and Numbered Hierarchy

## Date: August 3, 2025

### Overview
Added a compact/full column view toggle and improved group indicators with numbered hierarchy for better data visualization and understanding in the Policy Revenue Ledger Reports page.

### Features Added

#### 1. Compact/Full Column View Toggle
- **Toggle Button**: Radio button selector with eye icons
  - 👁️ Compact Data: Minimizes column widths to show more data at once
  - 👀 Full Headers: Shows complete column headers with appropriate widths
- **Smart Column Handling**:
  - Special columns (Reviewed, Group, Type) use pixel widths in compact mode
  - Regular columns adapt based on view mode
  - Preserves data readability while maximizing screen space

#### 2. Enhanced Group Indicators
- **Numbered Hierarchy System**:
  - Each policy term gets a sequential number (Term 1, Term 2, etc.)
  - Transactions within terms numbered as X.Y (e.g., 1.1, 1.2, 1.3 for Term 1)
  - Subtotal rows marked with equals sign (=) instead of abstract symbol
- **Improved Mental Model**:
  - Clear visual hierarchy showing which transactions belong to which term
  - Intuitive numbering that matches how users think about policy terms
  - Easy to identify transaction groupings at a glance

#### 3. Functional Subtotal Checkboxes
- **Bulk Operations**: Clicking a subtotal checkbox marks/unmarks ALL transactions in that term
- **Efficient Review Process**: No need to individually check each transaction in a term
- **Visual Feedback**: Subtotal checkbox reflects whether all transactions in the term are reviewed

#### 4. Term-Based Balance Filtering
- **Smart Filtering**: Balance filters now work at the term level using subtotal values
- **Options**:
  - Show policies with credit balance (positive subtotal)
  - Show policies with debit balance (negative subtotal)
  - Show policies with zero balance
- **Logical Grouping**: Respects policy term boundaries for more meaningful filtering

### Technical Implementation

#### Group Assignment Logic
- NEW/RWL transactions define term boundaries
- END transactions included if within term dates
- STMT/VOID transactions matched by STMT DATE
- All other transactions (STL, etc.) included if Effective Date falls within term range

#### Column Width Management
```python
# Compact mode - minimal pixel widths
checkbox_width = 50  # Just enough for checkbox
type_width = 40      # Just for emoji
group_width = 40     # Just for symbol

# Full mode - appropriate widths
checkbox_width = None    # Auto-size for "Reviewed" header
type_width = "small"     # Keep small for Type →
group_width = "small"    # Keep small for Group
```

### User Benefits
1. **Better Data Density**: See more columns without horizontal scrolling in compact mode
2. **Clear Organization**: Numbered hierarchy makes term groupings obvious
3. **Faster Review**: Bulk operations via subtotal checkboxes save time
4. **Flexible Viewing**: Toggle between detailed headers and compact data as needed

### Visual Examples

**Full Headers Mode (👀)**:
- Shows complete column names
- Better for understanding data fields
- Ideal when learning the system

**Compact Data Mode (👁️)**:
- Minimizes column widths
- Shows more data at once
- Perfect for experienced users who know the columns

**Group Indicators**:
- 1.1, 1.2, 1.3 = First term transactions
- 2.1, 2.2 = Second term transactions
- = = Subtotal row for the term

### Known Limitations
- Some columns may require manual stretching in compact mode for full visibility
- Browser zoom can be used in combination with compact mode for maximum data density

## Enhanced Export Functionality

### Excel Export with Subtotals and Formatting
The Excel export in Detailed Transactions view now preserves the exact table layout including:

#### Preserved Elements
1. **Subtotal Rows**: All term subtotals with equals sign (=) indicators
2. **Group Numbering**: Numbered hierarchy (1.1, 1.2, etc.) for transaction grouping
3. **Special Columns**: Reviewed checkboxes, Group indicators, Type emojis
4. **Visual Formatting**:
   - Dark gray background with white text for subtotal rows
   - Light blue background for STMT transactions
   - Light red background for VOID transactions
   - Bold headers with green background

#### Export Features
- **Column Order**: Exports columns in the exact order shown in the table
- **Data Integrity**: All calculated values (subtotals) are preserved
- **Professional Formatting**: Excel file includes proper column widths and cell formatting
- **Metadata Sheet**: First sheet contains all report parameters and filters

#### How It Works
When you click "Export as Excel" in Detailed Transactions view:
1. The system captures the current table state including all subtotals
2. Applies the same visual formatting used in the web interface
3. Creates a multi-sheet Excel file with parameters and formatted data
4. Preserves the exact view you see on screen

This makes it easy to share reports with others or archive them for future reference while maintaining all the visual cues and organization.