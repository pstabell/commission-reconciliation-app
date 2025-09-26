#!/usr/bin/env python3
"""
Debug script to add comprehensive logging to trace where the statement total is calculated and displayed.
This will help identify why it's showing $3,179.13 instead of $1,568.94.
"""

import re

# Read the commission_app.py file
with open('commission_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add debug output after the statement total calculation
debug_code = '''
                                    # EXTENSIVE DEBUGGING FOR STATEMENT TOTAL CALCULATION
                                    st.markdown("### 🔍 DEBUG: Statement Total Calculation")
                                    
                                    # Show all available columns in the dataframe
                                    st.write("**Available columns in uploaded file:**")
                                    st.write(list(df.columns))
                                    
                                    # Show the current column mapping
                                    st.write("\\n**Current column mapping:**")
                                    st.write(st.session_state.column_mapping)
                                    
                                    # Check for Total Agent Comm column
                                    st.write("\\n**🔍 CHECKING FOR TOTAL AGENT COMM COLUMNS:**")
                                    total_agent_comm_columns = [col for col in df.columns if 'total' in col.lower() and 'agent' in col.lower() and 'comm' in col.lower()]
                                    if total_agent_comm_columns:
                                        st.warning(f"⚠️ Found 'Total Agent Comm' columns that might be causing issues: {total_agent_comm_columns}")
                                        for tac_col in total_agent_comm_columns:
                                            tac_amounts = pd.to_numeric(df[tac_col], errors='coerce').fillna(0)
                                            tac_total = tac_amounts.sum()
                                            st.write(f"- Column '{tac_col}' total: ${tac_total:,.2f}")
                                            if abs(tac_total - 3179.13) < 0.01:
                                                st.error(f"❌ Column '{tac_col}' matches the incorrect total of $3,179.13!")
                                                st.write(f"  This column has values: {tac_amounts[tac_amounts != 0].head(10).to_list()}")
'''

# Find where to insert the debug code (already done in previous edit)
# Now let's add debugging to where the reconciliation total is displayed

# Add debugging to trace where $3,179.13 is displayed in the verification check
verification_debug = '''
                    # DEBUG: Show what's in the statement total
                    if statement_total_key in st.session_state:
                        st.write(f"**DEBUG: Statement total key value = ${st.session_state[statement_total_key]:,.2f}**")
                        if abs(st.session_state[statement_total_key] - 3179.13) < 0.01:
                            st.error("❌ Statement total is incorrectly set to $3,179.13")
                        elif abs(st.session_state[statement_total_key] - 1568.94) < 0.01:
                            st.success("✅ Statement total is correctly set to $1,568.94")
'''

# Search for where the verification check displays the total
pattern = r'(# Show statement total for verification if available\s*\n\s*if statement_total_key in st\.session_state)'
match = re.search(pattern, content, re.MULTILINE)

if match:
    # Insert debug code after the pattern
    insert_pos = match.end()
    # Find the next line after the if statement
    next_line_pos = content.find('\n', insert_pos) + 1
    
    # Insert the debug code
    new_content = content[:next_line_pos] + verification_debug + '\n' + content[next_line_pos:]
    
    # Save the modified content
    with open('commission_app_debug.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Added verification debug code")
else:
    print("❌ Could not find verification check pattern")

# Also add debugging to track what columns are being displayed in tables
table_debug = '''
                            # DEBUG: Log what columns are being displayed
                            st.write("**DEBUG: Columns in filtered_df:**")
                            st.write(list(filtered_df.columns))
                            if 'Total Agent Comm' in filtered_df.columns:
                                st.warning("⚠️ 'Total Agent Comm' column found in display - this might be the issue!")
                                total_agent_comm_sum = pd.to_numeric(filtered_df['Total Agent Comm'], errors='coerce').fillna(0).sum()
                                st.write(f"Total Agent Comm sum: ${total_agent_comm_sum:,.2f}")
                            if 'Pay Amount' in filtered_df.columns:
                                pay_amount_sum = pd.to_numeric(filtered_df['Pay Amount'], errors='coerce').fillna(0).sum()
                                st.write(f"Pay Amount sum: ${pay_amount_sum:,.2f}")
'''

print("\n📋 Summary of debugging additions:")
print("1. Added extensive debugging to statement total calculation")
print("2. Added verification debugging to check if total is $3,179.13 vs $1,568.94")
print("3. Added table column debugging to track what's being displayed")
print("\nThe debug output will help identify:")
print("- Which column is being summed")
print("- Whether 'Total Agent Comm' column exists and is causing the issue")
print("- The exact values being calculated")