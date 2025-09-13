import pandas as pd
import random

def anonymize_realistic_name(name):
    """Anonymizes a name to look realistic by making slight, plausible changes."""
    if not isinstance(name, str):
        return name

    name_parts = name.split()
    
    # --- For Company Names (containing LLC, Inc., etc.) ---
    if any(suffix in name.upper() for suffix in ['LLC', 'INC', 'L.L.C.', 'INC.']):
        first_word = name_parts[0]
        business_words = ['Apex', 'Summit', 'Pinnacle', 'Horizon', 'Vanguard', 'Matrix', 'Synergy', 'Quantum', 'Stellar', 'Orion']
        new_first_word = random.choice(business_words)
        while new_first_word.upper() == first_word.upper():
            new_first_word = random.choice(business_words)
        name_parts[0] = new_first_word
        return " ".join(name_parts)
    
    # --- For Personal Names (assuming format "First Last") ---
    if len(name_parts) == 2:
        first_name, last_name = name_parts
        if len(last_name) > 2:
            if last_name.lower().endswith('s'):
                last_name = last_name[:-1] + 'z' # Gomes -> GomeZ
            elif last_name.lower().endswith('n'):
                 last_name = last_name[:-1] + 'm' # Jackson -> Jacksom
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
    """Scrambles the digits of a policy number while keeping letters and the last digit in place."""
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
input_filename = "all_policies_20250810_033936 After - payments column cleaned.xlsx"
output_filename = "demo_client_database.csv"

# --- MAIN SCRIPT ---
try:
    print(f"Reading data from Excel file: '{input_filename}'...")
    df = pd.read_excel(input_filename)
    print("Data read successfully.")

    if 'Customer' in df.columns:
        print("Anonymizing 'Customer' names...")
        df['Customer'] = df['Customer'].apply(anonymize_realistic_name)
    if 'Policy Number' in df.columns:
        print("Scrambling 'Policy Number'...")
        df['Policy Number'] = df['Policy Number'].apply(scramble_policy_number)

    df.to_csv(output_filename, index=False)
    print("\n--- SUCCESS! ---")
    print(f"Anonymized CSV file created: '{output_filename}'")

except FileNotFoundError:
    print(f"\n--- ERROR ---")
    print(f"The Excel file '{input_filename}' was not found.")
    print("Please make sure the script and the Excel file are in the exact same folder.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")