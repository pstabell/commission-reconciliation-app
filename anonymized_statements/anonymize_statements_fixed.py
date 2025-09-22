import pandas as pd
import random
import os
from datetime import timedelta

# --- Fictitious Data Generators ---

def generate_fictitious_name():
    """Generates a random fictitious name."""
    first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Skyler", "Jamie", "Riley", "Cameron", "Devon",
                   "Avery", "Quinn", "Sage", "River", "Phoenix", "Dakota", "Rowan", "Harper", "Blake", "Drew"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                  "Wilson", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Moore", "Young"]
    companies = ["LLC", "Inc", "Corp", "Services", "Solutions", "Enterprises", "Group", "Holdings", "Industries", "Partners"]
    
    # Randomly decide if it's a person or company
    if random.choice([True, False]):
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    else:
        return f"{random.choice(first_names)} {random.choice(companies)}"

def scramble_policy_number(policy_number):
    """Scrambles a policy number and removes all dashes, spaces, and dots."""
    if pd.isna(policy_number):
        return policy_number
    
    # First, remove all dashes, spaces, and dots
    policy_str = str(policy_number)
    policy_str = policy_str.replace('-', '').replace(' ', '').replace('.', '')
    
    # Now scramble the alphanumeric content
    result = []
    for char in policy_str:
        if char.isdigit():
            result.append(str(random.randint(0, 9)))
        elif char.isalpha():
            result.append(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        else:
            # Skip any other special characters
            continue
    return ''.join(result)

# --- Main Script ---

# Excel files to process (look in current directory)
current_dir = os.path.dirname(os.path.abspath(__file__))
files_to_process = [
    os.path.join(current_dir, "2025-06-30 Commission Statement.xlsx"),
    os.path.join(current_dir, "2025-07-31 Commission Statement.xlsx"),
    os.path.join(current_dir, "2025-08-31 Commission Statement.xlsx")
]

# Dictionaries to store mappings for consistency across all files
name_mapping = {}
policy_mapping = {}
processed_files = []

print("Starting anonymization process for commission statements...")
print("=" * 60)

# Process each file
for filename in files_to_process:
    if not os.path.exists(filename):
        print(f"❌ File not found: '{filename}'")
        continue
    
    try:
        print(f"\n📄 Processing '{filename}'...")
        
        # Read the Excel file
        df = pd.read_excel(filename)
        print(f"   - Loaded {len(df)} rows")
        
        # Find columns that might contain sensitive data
        # Common column name variations
        name_columns = ['Insured Name', 'Insured', 'Customer', 'Client', 'Name', 'Customer Name']
        policy_columns = ['Policy', 'Policy Number', 'Policy #', 'Policy No']
        
        # Find actual column names (case-insensitive)
        actual_name_col = None
        actual_policy_col = None
        
        for col in df.columns:
            col_lower = col.lower()
            for name_col in name_columns:
                if name_col.lower() in col_lower:
                    actual_name_col = col
                    break
            for policy_col in policy_columns:
                if policy_col.lower() in col_lower:
                    actual_policy_col = col
                    break
        
        if not actual_name_col:
            print(f"   ⚠️  WARNING: No customer name column found. Checked for: {name_columns}")
        else:
            print(f"   - Found name column: '{actual_name_col}'")
            # Anonymize names consistently
            def get_fictitious_name(original_name):
                if pd.isna(original_name):
                    return original_name
                original_str = str(original_name).strip()
                if original_str and original_str not in name_mapping:
                    name_mapping[original_str] = generate_fictitious_name()
                return name_mapping.get(original_str, original_str)
            
            df[actual_name_col] = df[actual_name_col].apply(get_fictitious_name)
            print(f"   - Anonymized {len(name_mapping)} unique names")
        
        if not actual_policy_col:
            print(f"   ⚠️  WARNING: No policy number column found. Checked for: {policy_columns}")
        else:
            print(f"   - Found policy column: '{actual_policy_col}'")
            # Scramble policy numbers consistently
            def get_scrambled_policy(original_policy):
                if pd.isna(original_policy):
                    return original_policy
                original_str = str(original_policy).strip()
                if original_str and original_str not in policy_mapping:
                    policy_mapping[original_str] = scramble_policy_number(original_str)
                return policy_mapping.get(original_str, original_str)
            
            df[actual_policy_col] = df[actual_policy_col].apply(get_scrambled_policy)
            print(f"   - Scrambled {len(policy_mapping)} unique policy numbers")
        
        # Bump effective dates by 2 months and remove time component
        date_columns_updated = False
        for col in df.columns:
            col_lower = col.lower()
            # Look for 'eff date' or similar patterns
            if 'eff' in col_lower and 'date' in col_lower:
                print(f"   - Found effective date column: '{col}'")
                # Convert to datetime, add 2 months, and remove time
                df[col] = pd.to_datetime(df[col], errors='coerce')
                df[col] = df[col] + pd.DateOffset(months=2)
                # Format as date only (no time)
                df[col] = df[col].dt.strftime('%Y-%m-%d')
                print(f"   - Bumped dates by 2 months and removed time")
                date_columns_updated = True
                break
        
        if not date_columns_updated:
            print("   ⚠️  WARNING: No effective date column found")
        
        # Increase all financial amounts by 10%
        financial_keywords = ['amount', 'commission', 'premium', 'fee', 'total', 'gross', 'net', 'payment', 'paid']
        financial_columns_updated = []
        
        for col in df.columns:
            col_lower = col.lower()
            # Check if column name contains any financial keyword
            if any(keyword in col_lower for keyword in financial_keywords):
                # Skip if it's a percentage column
                if '%' in col or 'percent' in col_lower or 'rate' in col_lower:
                    continue
                
                try:
                    # Convert to numeric, ignoring errors
                    numeric_data = pd.to_numeric(df[col], errors='coerce')
                    if not numeric_data.isna().all():  # If column has numeric data
                        df[col] = numeric_data * 1.10  # Increase by 10%
                        financial_columns_updated.append(col)
                except:
                    pass
        
        if financial_columns_updated:
            print(f"   - Increased {len(financial_columns_updated)} financial columns by 10%")
        
        # Save the anonymized file with just the base filename
        base_filename = os.path.basename(filename)
        new_filename = f"ANONYMIZED_{base_filename}"
        df.to_excel(new_filename, index=False)
        processed_files.append(new_filename)
        print(f"   ✅ SUCCESS: Saved to '{new_filename}'")
        
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        continue

print("\n" + "=" * 60)
print(f"✅ Anonymization complete!")
print(f"   - Processed {len(processed_files)} files")
print(f"   - Output folder: Current directory")
print(f"   - Total unique names anonymized: {len(name_mapping)}")
print(f"   - Total unique policies scrambled: {len(policy_mapping)}")