# App-Wide Design Standards
**Purpose**: Design standards and patterns that apply across all pages

## 🎯 Terminology Standards

### Transaction vs Policy
**Consistent usage across all pages:**

| Term | Definition | When to Use |
|------|------------|-------------|
| Transaction | Individual database record | Referring to rows in database |
| Policy | Unique policy number | Counting distinct policies |
| Policy Transaction | Transaction for a policy | When clarity needed |
| Transaction Type | NEW, RWL, END, CAN, etc. | Categorizing records |

### Examples:
- ✅ "Showing 195 transactions"
- ❌ "Showing 195 policies" (when it's transactions)
- ✅ "87 unique policies"
- ✅ "Filter by transaction type"

## 🎨 Visual Standards

### Color Coding for Transaction Types
- NEW: Green (#28a745)
- RWL: Blue (#007bff)
- END: Orange (#ffc107)
- CAN/XCL: Red (#dc3545)
- -STMT-/-VOID-/-ADJ-: Gray (#6c757d)

### Status Indicators
- ✓ Success/Match (green)
- ✏️ Manual Override (yellow)
- ⚠️ Warning/Missing (orange)
- 🔒 Locked/Protected (gray)
- ❌ Error (red)

### Number Formatting
- Currency: $X,XXX.XX
- Percentages: XX.X%
- Counts: X,XXX (with commas)

## 🔧 Common Components

### Page Headers
Every page should clearly state what it displays:
- "All Policy Transactions" not "All Policies"
- "Edit Transaction Records" not "Edit Policies"
- Include help icon with tooltip explaining the page

### Data Tables
- Sortable columns
- Pagination with options (25, 50, 100)
- Export buttons (CSV, Excel)
- Search/filter capabilities

### Forms
- Group related fields
- Clear labels
- Help text for complex fields
- Validation messages
- Save confirmation

## 📊 Navigation Standards

### Menu Organization
1. **Overview** - Dashboard, summaries
2. **Data Management** - View, edit, import
3. **Financial** - Reconciliation, reports
4. **Admin** - Settings, maintenance
5. **Help** - Documentation, support

### Breadcrumbs
Show current location:
```
Dashboard > All Transactions > Edit Transaction #ABC123
```

## 🔒 Security Patterns

### Protected Records
Always clearly indicate:
- Which records are locked
- Why they're locked
- Where to go to manage them

### Permission Messages
- Clear explanation of restrictions
- Helpful alternatives
- Contact info for elevated access

## 📱 Responsive Design

### Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

### Priority Content
On smaller screens, prioritize:
1. Key metrics
2. Action buttons
3. Essential data columns

## 🌐 Session Management

### State Persistence
These should persist across pages:
- Search terms
- Filter selections
- Sort preferences
- View modes (formula/actual)

### Clear State Indicators
Show when:
- Filters are active
- Search is applied
- Non-default view mode

## 📝 Help Integration

### Inline Help
- Tooltips on complex fields
- Info icons with explanations
- Link to relevant documentation

### Contextual Help
- Page-specific help sections
- Common tasks for that page
- Troubleshooting tips

## 🎯 Performance Standards

### Loading States
- Show spinner for operations > 1 second
- Progress bars for bulk operations
- Estimated time for long processes

### Data Limits
- Paginate large datasets
- Lazy load when appropriate
- Cache frequently accessed data

---

*These standards ensure consistency across all pages and improve user experience.*