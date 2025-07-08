# UI Design Standards - Consolidated
**Last Updated**: July 8, 2025  
**Purpose**: Comprehensive UI/UX design standards for the Sales Commission App

## Table of Contents
1. [Terminology Standards](#terminology-standards)
2. [Visual Design System](#visual-design-system)
3. [Page-Specific Designs](#page-specific-designs)
4. [Component Standards](#component-standards)
5. [Responsive Design](#responsive-design)
6. [Accessibility](#accessibility)

---

## Terminology Standards

### Transaction vs Policy
**Critical distinction that affects all UI labeling:**

| Term | Definition | When to Use | Example |
|------|------------|-------------|---------|
| **Transaction** | Individual database record | Counting rows | "195 transactions" |
| **Policy** | Unique policy number | Counting distinct policies | "87 unique policies" |
| **Policy Transaction** | Transaction for a policy | When clarity needed | "View policy transactions" |

### Correct Usage Examples:
- ✅ "Total Transactions: 195"
- ❌ "Total Policies: 195" (when showing transaction count)
- ✅ "Filter by Transaction Type"
- ✅ "87 Unique Policies (195 transactions)"

---

## Visual Design System

### Color Palette

#### Transaction Type Colors
- **NEW**: #28a745 (Green) - New business
- **RWL**: #007bff (Blue) - Renewals
- **END**: #ffc107 (Orange) - Endorsements
- **CAN/XCL**: #dc3545 (Red) - Cancellations
- **-STMT-/-VOID-/-ADJ-**: #6c757d (Gray) - Reconciliation

#### Status Colors
- **Success**: #28a745 (Green)
- **Warning**: #ffc107 (Orange)
- **Error**: #dc3545 (Red)
- **Info**: #17a2b8 (Teal)
- **Locked**: #6c757d (Gray)

### Status Indicators

| Icon | Meaning | Use Case | Color |
|------|---------|----------|-------|
| ✓ | Success/Match | Formula matches manual | Green |
| ✏️ | Manual Override | User edited value | Orange |
| ⚠️ | Warning | Missing data | Orange |
| 🔒 | Locked | Protected record | Gray |
| ❌ | Error | Invalid data | Red |
| 📊 | Formula Mode | Calculated value | Blue |
| 📝 | Manual Mode | User-entered value | Gray |

### Typography
- **Headers**: System default + bold
- **Labels**: System default
- **Values**: Monospace for numbers
- **Hints**: Smaller, gray (#6c757d)

---

## Page-Specific Designs

### 1. Commission Dashboard

#### Current Issues:
- Shows "Total Policies" but displays transaction count
- Lacks distinction between transactions and unique policies

#### Improved Design:
```
┌─────────────────────────────────────────────┐
│         📊 Commission Dashboard             │
├─────────────────┬───────────────────────────┤
│ TRANSACTIONS    │ POLICIES                  │
│ Total: 195      │ Unique: 87               │
│ This Month: 23  │ Active: 72               │
│ -STMT-: 2       │ Cancelled: 15            │
├─────────────────┴───────────────────────────┤
│           💰 FINANCIAL SUMMARY              │
│ Premium Sold: $543,210                      │
│ Agency Comm: $54,321                        │
│ Agent Comm: $27,160                         │
└─────────────────────────────────────────────┘
```

### 2. All Policies (Should be "All Transactions")

#### Improvements:
- Rename to "All Policy Transactions"
- Add summary bar showing unique policy count
- Formula toggle prominent at top

#### Layout:
```
All Policy Transactions                    [📊 Show Formulas ▼]
Showing 195 transactions (87 unique policies)
[Pagination] [Search] [Filters] [Export]
```

### 3. Edit Policies (Should be "Edit Transactions")

#### Current Features (Keep):
- Reconciliation protection
- Formula calculations
- Field organization

#### Improvements:
- Clearer labeling of what's being edited
- Show transaction type prominently
- Lock icon for protected fields

---

## Component Standards

### Number Formatting (Added July 8, 2025)

#### Display Requirements
**All numeric values must show exactly 2 decimal places for accounting consistency**

1. **Currency Fields**
   - Format: `$X,XXX.XX`
   - Examples: `$1,500.00`, `$308.70`, `$29.40`
   - Implementation: `format="$%.2f"`

2. **Percentage Fields**
   - Format: `XX.XX%` or `XX.XX`
   - Examples: `10.00%`, `50.00%`, `25.50%`
   - Implementation: `format="%.2f"`

3. **Data Tables**
   - All numeric columns must use column_config
   - Dollar columns: `st.column_config.NumberColumn(format="$%.2f")`
   - Percent columns: `st.column_config.NumberColumn(format="%.2f")`

### Forms
1. **Field Grouping**
   - Client Information
   - Policy Information
   - Commission Details
   - Internal Fields (grayed out)

2. **Field States**
   - Editable: White background
   - Calculated: Light gray (#f8f9fa)
   - Locked: Dark gray (#e9ecef)
   - Error: Light red (#fee)

### Tables
1. **Column Headers**
   - Sortable columns show arrows
   - Frozen first column for scrolling
   - Resizable columns

2. **Row States**
   - Default: White
   - Hover: Light blue (#f0f8ff)
   - Selected: Blue border
   - Locked: Gray background

### Buttons
1. **Primary Actions**
   - Background: #007bff
   - Text: White
   - Examples: Save, Submit, Calculate

2. **Secondary Actions**
   - Background: White
   - Border: #6c757d
   - Examples: Cancel, Reset

3. **Danger Actions**
   - Background: #dc3545
   - Text: White
   - Examples: Delete, Remove

### Notifications
1. **Success**: Green banner with ✓
2. **Warning**: Orange banner with ⚠️
3. **Error**: Red banner with ❌
4. **Info**: Blue banner with ℹ️

---

## Responsive Design

### Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Mobile Adaptations
1. **Navigation**: Hamburger menu
2. **Tables**: Horizontal scroll with frozen columns
3. **Forms**: Single column layout
4. **Buttons**: Full width

### Priority Content by Screen Size
- **Mobile**: Key metrics, actions
- **Tablet**: Add secondary info
- **Desktop**: Full feature set

---

## Accessibility

### Color Contrast
- Text on background: 4.5:1 minimum
- Large text: 3:1 minimum
- Don't rely on color alone

### Keyboard Navigation
- All interactive elements reachable
- Clear focus indicators
- Logical tab order

### Screen Readers
- Descriptive labels
- ARIA attributes where needed
- Table headers properly associated

### Visual Indicators
- Never rely solely on color
- Use icons + color
- Provide text alternatives

---

## Implementation Guidelines

### Consistency Rules
1. **Always use the same term** for the same concept
2. **Follow color conventions** religiously
3. **Maintain spacing standards**: 8px grid
4. **Use consistent icons** from the defined set

### Progressive Enhancement
1. **Core functionality** works without JavaScript
2. **Enhanced features** layer on top
3. **Graceful degradation** for older browsers

### Performance
1. **Lazy load** large datasets
2. **Debounce** search inputs
3. **Virtual scrolling** for long lists
4. **Optimize images** and icons

---

## Dashboard Implementation Strategy

### Objective
Transform the dashboard from showing misleading "Total Policies" (which is actually transaction count) to showing accurate metrics that distinguish between transactions and unique policies.

### Implementation Steps

#### Step 1: Create Metric Calculation Functions
Add these functions to commission_app.py:

```python
def calculate_dashboard_metrics(df):
    """Calculate dashboard metrics distinguishing transactions vs policies."""
    metrics = {
        # Transaction metrics
        'total_transactions': len(df),
        'transactions_this_month': len(df[df['Effective Date'].dt.month == datetime.now().month]),
        'stmt_transactions': len(df[df['Transaction Type'].str.startswith('-')]),
        
        # Policy metrics (unique policy numbers)
        'unique_policies': df['Policy Number'].nunique(),
        'active_policies': 0,  # Calculated below
        'cancelled_policies': 0,  # Calculated below
        
        # Financial metrics
        'total_premium': df['Premium Sold'].sum(),
        'total_agency_comm': df['Agency Commission'].sum(),
        'total_agent_comm': df['Agent Commission'].sum()
    }
    
    # Calculate active vs cancelled policies
    if not df.empty:
        # Get latest transaction for each policy
        latest_trans = df.sort_values('Effective Date').groupby('Policy Number').last()
        metrics['active_policies'] = len(latest_trans[~latest_trans['Transaction Type'].isin(['CAN', 'XCL'])])
        metrics['cancelled_policies'] = len(latest_trans[latest_trans['Transaction Type'].isin(['CAN', 'XCL'])])
    
    return metrics
```

#### Step 2: Update Dashboard Display
Replace the current metrics display with:

```python
# In the commission_dashboard() function
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 TRANSACTIONS")
    st.metric("Total Transactions", metrics['total_transactions'])
    st.metric("This Month", metrics['transactions_this_month'])
    st.metric("Reconciliation (-STMT-)", metrics['stmt_transactions'])

with col2:
    st.subheader("📋 POLICIES")
    st.metric("Unique Policies", metrics['unique_policies'])
    st.metric("Active", metrics['active_policies'])
    st.metric("Cancelled", metrics['cancelled_policies'])

st.subheader("💰 FINANCIAL SUMMARY")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Premium Sold", f"${metrics['total_premium']:,.2f}")
with col2:
    st.metric("Agency Commission", f"${metrics['total_agency_comm']:,.2f}")
with col3:
    st.metric("Agent Commission", f"${metrics['total_agent_comm']:,.2f}")
```

#### Step 3: Add Transaction Type Distribution
Add a pie chart showing transaction type breakdown:

```python
# Transaction type distribution
trans_types = df['Transaction Type'].value_counts()
fig = px.pie(values=trans_types.values, names=trans_types.index, 
             title="Transaction Type Distribution",
             color_discrete_map={
                 'NEW': '#28a745',
                 'RWL': '#007bff', 
                 'END': '#ffc107',
                 'CAN': '#dc3545',
                 'XCL': '#dc3545'
             })
st.plotly_chart(fig)
```

### Testing Strategy

1. **Verify Counts**:
   - Count unique policy numbers manually
   - Compare with dashboard display
   - Check transaction counts match database

2. **Edge Cases**:
   - Policies with multiple transactions
   - Policies with only -STMT- transactions
   - Empty policy numbers (should be excluded)

3. **Performance**:
   - Test with full dataset
   - Monitor load times
   - Consider caching for large datasets

### Rollout Plan

1. **Phase 1**: Implement metrics calculation (immediate)
2. **Phase 2**: Update dashboard display (immediate)
3. **Phase 3**: Update all other pages to use consistent terminology (next sprint)

### Success Criteria

- Dashboard shows both transaction and policy counts
- No confusion between transactions and policies
- Clear visual distinction between the two metrics
- All counts are accurate and verifiable

---

*This document consolidates APP_WIDE_DESIGN.md and DASHBOARD_PAGE_DESIGN.md into comprehensive UI standards.*