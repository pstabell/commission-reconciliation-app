Absolutely! Here’s your **updated Master Design** for the **Policy Revenue Ledger Report** page, now ensuring that all parameters/filters are included in the **downloaded Excel file** and **printed PDF** (not just visible in the UI).

---

## **Policy Revenue Ledger Report – Master Design (with Exported Filter Parameters)**

### **Purpose**
- Show a summary table: **one row per unique policy** with all key details and a calculated Balance Due.
- Allow full customization and reordering of columns, visible filters, and report templates.
- Enable saving, re-running, and exporting reports—with all filters/parameters included in the exported file.

---

### **Key Features**

#### 1. **Customizable & Reorderable Columns**
- Multi-select for column selection.
- Drag-and-drop or up/down controls for column order.

#### 2. **Always-Visible Filters (in Exported Reports)**
- All active filters (date, customer, carrier, etc.) and report parameters are included at the top of the **Excel export** and **PDF printout**.
- This ensures anyone viewing the exported report knows exactly how it was generated.

#### 3. **Save & Load Report Templates**
- Save current column order, filters, and title as a named template.
- Load and run a saved template with one click.

#### 4. **Custom Report Title**
- User can enter a custom title before saving or exporting.

#### 5. **Export to Excel (with Filters)**
- Button to download the current report as Excel.
- The Excel file includes a header section listing all filters/parameters used.
- (Optional) Print to PDF tip/button, with filters/parameters included at the top of the printout.

#### 6. **Policy Effective Date Filters**
- Filter policies by effective date:
  - All dates
  - At least 30, 60, or 90 days old (relative to today)

#### 7. **Outstanding Balances Only**
- Only show policies with a nonzero Balance Due (UI-calculated).

---

### **UI Layout**

1. **Header & Description**
2. **Template Controls**
3. **Column & Filter Controls**
4. **Active Filters Display (in UI and Export)**
5. **Report Table**
6. **Export/Download**

---

### **Sample Pseudocode (Export Section)**

```python
# ...previous code for UI and data prep...

# --- Active Filters/Parameters ---
filters_dict = {
    "Report Title": report_title,
    "Columns": column_order,
    "Effective Date Filter": date_filter,
    # ...other filters...
}
st.markdown("**Active Filters:**")
st.write(filters_dict)

# --- Show Table ---
st.subheader(report_title)
st.dataframe(summary[column_order + ["Balance Due"]], use_container_width=True)

# --- Export to Excel (with filters/parameters at top) ---
import pandas as pd

def to_excel_with_filters(df, filters, filename):
    # Create a DataFrame for filters
    filters_df = pd.DataFrame(list(filters.items()), columns=["Parameter", "Value"])
    # Write filters and data to Excel
    with pd.ExcelWriter(filename) as writer:
        filters_df.to_excel(writer, sheet_name="Report", index=False, startrow=0)
        df.to_excel(writer, sheet_name="Report", index=False, startrow=len(filters_df) + 2)

if st.button("Download as Excel"):
    to_excel_with_filters(summary[column_order + ["Balance Due"]], filters_dict, f"{report_title}.xlsx")
    st.success("Excel file downloaded! (Filters included at top)")

st.caption("Tip: When printing to PDF, the filters/parameters will appear at the top of the report.")
```

---

### **Copilot Warning: Change Management**

> ⚠️ **Copilot Warning:**  
> Changes to this report page—especially those involving data aggregation, column logic, or template storage—could affect shared data structures, utility functions, or global variables used by other pages (such as the main Policy Revenue Ledger page, Reports, or Accounting).  
> **Before making major changes:**
> - Review any shared functions or variables.
> - Test all related pages after changes.
> - Consider versioning or backing up your code.
> - Walk through the change procedure step-by-step to avoid breaking other parts of the app.

---

**Let me know if you want to proceed with a code prototype or further refine this design!**