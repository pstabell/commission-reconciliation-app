
import os

file_path = r"C:\Users\Patri\OneDrive\STABELL DOCUMENTS\STABELL FILES\TECHNOLOGY\PROGRAMMING\SALES COMMISSIONS APP\commission_app.py"
with open(file_path, "r") as f:
    lines = f.readlines()

# Find the start of the block to be removed
start_index = -1
for i, line in enumerate(lines):
    if "if st.button('Delete Selected Payments', key='delete_payments_btn'):" in line:
        start_index = i
        break

if start_index != -1:
    # Find the end of the block
    end_index = -1
    for i in range(start_index, len(lines)):
        if 'st.warning("No records were selected for deletion.")' in lines[i]:
            end_index = i
            break

    if end_index != -1:
        # Remove the block
        del lines[start_index : end_index + 1]

        with open(file_path, "w") as f:
            f.writelines(lines)
        print("File updated successfully.")
    else:
        print("Error: Could not find the end of the block to be removed.")
else:
    print("Error: Could not find the start of the block to be removed.")
