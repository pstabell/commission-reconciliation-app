#!/usr/bin/env python3
"""
Fix for policy types issues:
1. Add missing remove_policy_type method
2. Update add_policy_type to provide better error messages
3. Fix the UI to show all existing policy types properly
"""

# First, let's create the patch for user_policy_types_db.py

REMOVE_METHOD = '''
    def remove_policy_type(self, code: str) -> bool:
        """Remove a policy type if it's not a system default."""
        # List of protected system defaults that cannot be removed
        protected_types = ["GL", "WC", "BOP", "CPK", "CARGO", "AUTO", "EXCESS", "CYBER", "D&O", "E&O", "EPLI", "OTHER"]
        
        if code in protected_types:
            return False  # Cannot remove protected types
        
        config = self.get_user_policy_types()
        
        # Filter out the type to remove
        original_count = len(config['policy_types'])
        config['policy_types'] = [
            pt for pt in config['policy_types'] 
            if pt['code'] != code
        ]
        
        # Check if anything was removed
        if len(config['policy_types']) == original_count:
            return False  # Type didn't exist
        
        # Save the updated configuration
        return self.save_user_policy_types(
            config['policy_types'], 
            config['default'], 
            config.get('categories')
        )
'''

ADD_METHOD_IMPROVED = '''
    def add_policy_type(self, code: str, name: str, category: str = 'Other', active: bool = True) -> bool:
        """Add a new policy type. Returns True if successful, False if already exists."""
        config = self.get_user_policy_types()
        
        # Check if already exists (case-insensitive)
        for pt in config['policy_types']:
            if pt['code'].upper() == code.upper():
                # Already exists - this is not an error, just inform the user
                print(f"Policy type '{code}' already exists with name '{pt['name']}'")
                return False
        
        # Add new type
        config['policy_types'].append({
            'code': code.upper(),  # Always store in uppercase
            'name': name,
            'category': category,
            'active': active
        })
        
        # Save
        return self.save_user_policy_types(
            config['policy_types'], 
            config['default'], 
            config.get('categories')
        )
'''

print("Fix created. To apply:")
print("1. Add the remove_policy_type method to UserPolicyTypes class")
print("2. Update the add_policy_type method for better error handling")
print("3. Update the UI in commission_app.py to show ALL existing policy types, not just 'active' ones")
print("\nThe main issue is that AUTOP already exists in the default policy types.")
print("Users need to see the complete list of existing types to avoid trying to add duplicates.")