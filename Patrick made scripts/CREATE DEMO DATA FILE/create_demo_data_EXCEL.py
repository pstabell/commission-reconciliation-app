import pandas as pd
import random

# --- Anonymization Functions (from before) ---
def anonymize_realistic_name(name):
    if not isinstance(name, str): return name
    name_parts = name.split()
    if any(suffix in name.upper() for suffix in ['LLC', 'INC', 'L.L.C.', 'INC.']):
        first_word = name_parts[0]
        business_words = ['Apex', 'Summit', 'Pinnacle', 'Horizon', 'Vanguard', 'Matrix', 'Synergy', 'Quantum', 'Stellar', 'Orion']
        new_first_word = random.choice(business_words)
        while new_first_word.upper() == first_word.upper():
            new_first_word = random.choice(business_words)
        name_parts[0] = new_first_word
        return " ".join(name_parts)
    if len(name_parts) == 2:
        first_name, last_name = name_parts
        if len(last_name) > 2:
            if last_name.lower().endswith('s'): last_name = last_name[:-1] + 'z'
            elif last_name.lower().endswith('n'): last_name = last_name[:-1] + 'm'
            else:
                vowels = "aeiou"
                last_name_list = list(last_name)
                for i in range(len(last_name_list) - 1, -1, -1):
                    if last_name_list[i].lower() in vowels:
                        last_name_list[i] = random.choice(vowels)
                        break
                last_name = "".join(last_name_list)
        return f"{first_name} {last_name.capitalize()}"
    return name

def scramble_policy_number(policy_number):
    if not isinstance(policy_number, str) or len(policy_number) <= 1: return policy_number
    last_char = policy_number[-1]
    main_part = policy_number[:-1]
    digits_to_scramble = [char for char in main_part if char.isdigit()]
    random.shuffle(digits_to_scramble)
    scrambled_main_part = ""
    digit_idx = 0
    for char in main_part:
        if char.isdigit():
            scrambled_main_part += digits_to_scramble[digit_idx]
            digit_idx += 1
        else: scrambled_main_part += char
    return scrambled_main_part + last_char

# --- CONFIGURATION ---
# 🔽 **CHANGE #1: This now points to your new Excel file**
input_filename = "all_policies_20250810_020027 Removed 2 Agent Paid STMT numbers.xlsx"
output_filename = "demo_client_database.xlsx"

# --- MAIN SCRIPT ---
try:
    print(f"Reading data from Excel file: '{input_filename}'...")
    df = pd.read_excel(input_filename)
    print("Data read successfully.")

    if 'Client ID' in df.columns and 'Customer' in df.columns:
        print("Anonymizing 'Customer' names consistently by 'Client ID'...")
        unique_clients = df.drop_duplicates(subset=['Client ID'])
        client_id_to_name_map = {}
        for index, row in unique_clients.iterrows():
            original_name = row['Customer']
            client_id_to_name_map[row['Client ID']] = anonymize_realistic_name(original_name)
        df['Customer'] = df['Client ID'].map(client_id_to_name_map)
        print("Customer names anonymized.")

    if 'Policy Number' in df.columns:
        print("Scrambling 'Policy Number' consistently...")
        unique_policies = df['Policy Number'].unique()
        policy_number_map = {policy: scramble_policy_number(policy) for policy in unique_policies}
        df['Policy Number'] = df['Policy Number'].map(policy_number_map)
        print("Policy numbers scrambled.")

    df.to_excel(output_filename, index=False)
    print("\n--- SUCCESS! ---")
    print(f"Consistent anonymized Excel file created: '{output_filename}'")

except FileNotFoundError:
    print(f"\n--- ERROR ---")
    print(f"The Excel file '{input_filename}' was not found.")
    print("Please make sure the script and the Excel file are in the exact same folder.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")