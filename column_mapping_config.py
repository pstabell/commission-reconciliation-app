"""
Centralized Column Mapping Configuration for Commission App

This module provides a centralized system for mapping UI field names to database column names,
replacing hardcoded column references throughout the application. This ensures that when 
users rename columns in the Admin Panel, all functionality continues to work seamlessly.

Key Features:
- Centralized column mapping with fallback to hardcoded names
- Support for calculated/virtual fields that don't exist in database
- Validation functions to ensure mapping integrity
- Easy integration with existing codebase
"""

import json
import os
from typing import Dict, List, Optional, Union
import pandas as pd


class ColumnMapper:
    """Centralized column mapping manager for the commission app."""
    
    def __init__(self, mapping_file: str = "column_mapping.json"):
        self.mapping_file = mapping_file
        self._mapping_cache = None
        self._reverse_mapping_cache = None
        
        # Default UI field names that the app expects
        self.default_ui_fields = {
            # Core identification fields
            "Customer": "Customer",
            "Policy Number": "Policy Number", 
            "Client ID": "Client ID",
            "Transaction ID": "Transaction ID",
            
            # Policy details
            "Policy Type": "Policy Type",
            "Carrier Name": "Carrier Name", 
            "Effective Date": "Effective Date",            "Policy Origination Date": "Policy Origination Date",
            "X-DATE": "X-DATE",
            "Transaction Type": "Transaction Type",
              # Financial fields  
            "Premium Sold": "Premium Sold",
            "Agency Estimated Comm/Revenue (CRM)": "Agency Estimated Comm/Revenue (CRM)",
            "Policy Gross Comm %": "Policy Gross Comm %",
            "Agent Estimated Comm $": "Agent Estimated Comm $",
            "Agent Paid Amount (STMT)": "Agent Paid Amount (STMT)",
            "Agency Comm Received (STMT)": "Agency Comm Received (STMT)",
            "Policy Balance Due": "Policy Balance Due",
            
            # Calculated fields
            "Agent Comm (New 50% RWL 25%)": "Agent Comm (New 50% RWL 25%)",
            "Agent Comm (NEW 50% RWL 25%)": "Agent Comm (NEW 50% RWL 25%)",
            "Estimated Agent Comm (New 50% Renewal 25%)": "Estimated Agent Comm (New 50% Renewal 25%)",
            "Agency Estimated Comm/Revenue (CRM)": "Agency Estimated Comm/Revenue (CRM)",
            "Agency Estimated Comm/Revenue (AZ)": "Agency Estimated Comm/Revenue (AZ)",
            
            # Date fields
            "Due Date": "Due Date",
            "Statement Date": "Statement Date", 
            "STMT DATE": "STMT DATE",
            "Transaction Date": "Transaction Date",
            
            # Status fields
            "Paid": "Paid",
            "PAST DUE": "PAST DUE",
            "NEW BIZ CHECKLIST COMPLETE": "NEW BIZ CHECKLIST COMPLETE",
            
            # Other fields
            "Producer": "Producer",
            "Lead Source": "Lead Source",
            "Description": "Description",
            "NOTES": "NOTES",
            "FULL OR MONTHLY PMTS": "FULL OR MONTHLY PMTS"
        }
        
        # Fields that are calculated and not stored in database
        self.calculated_fields = {
            "Policy Balance Due",
            "PAST DUE", 
            "Agent Estimated Comm $",
            "Agency Estimated Comm/Revenue (CRM)",
            "Agency Estimated Comm/Revenue (AZ)"
        }
        
    def _load_mapping(self) -> Dict[str, str]:
        """Load column mapping from file with caching."""
        if self._mapping_cache is None:
            if os.path.exists(self.mapping_file):
                try:
                    with open(self.mapping_file, "r") as f:
                        loaded_mapping = json.load(f)
                    # Merge with defaults, prioritizing file mapping
                    self._mapping_cache = self.default_ui_fields.copy()
                    self._mapping_cache.update(loaded_mapping)
                except (json.JSONDecodeError, Exception):
                    # If file is corrupted, use defaults
                    self._mapping_cache = self.default_ui_fields.copy()
            else:
                self._mapping_cache = self.default_ui_fields.copy()
        return self._mapping_cache
    
    def _get_reverse_mapping(self) -> Dict[str, str]:
        """Get reverse mapping (database column -> UI field)."""
        if self._reverse_mapping_cache is None:
            mapping = self._load_mapping()
            self._reverse_mapping_cache = {v: k for k, v in mapping.items() if v != "(Calculated/Virtual)"}
        return self._reverse_mapping_cache
    
    def clear_cache(self):
        """Clear mapping cache to force reload."""
        self._mapping_cache = None
        self._reverse_mapping_cache = None
    
    def get_db_column(self, ui_field: str, fallback_to_ui: bool = True) -> Optional[str]:
        """
        Get database column name for a UI field.
        
        Args:
            ui_field: The UI field name
            fallback_to_ui: If True, return ui_field if no mapping found
            
        Returns:
            Database column name or None if calculated field
        """
        mapping = self._load_mapping()
        db_col = mapping.get(ui_field)
        
        if db_col == "(Calculated/Virtual)":
            return None
        elif db_col:
            return db_col
        elif fallback_to_ui:
            return ui_field
        else:
            return None
    
    def get_ui_field(self, db_column: str) -> Optional[str]:
        """Get UI field name for a database column."""
        reverse_mapping = self._get_reverse_mapping()
        return reverse_mapping.get(db_column, db_column)
    
    def is_calculated_field(self, ui_field: str) -> bool:
        """Check if a field is calculated (not stored in database)."""
        return (ui_field in self.calculated_fields or 
                self.get_db_column(ui_field, fallback_to_ui=False) is None)
    
    def get_available_db_columns(self, all_columns: List[str]) -> List[str]:
        """Get database columns that are not already mapped."""
        mapping = self._load_mapping()
        mapped_cols = {v for v in mapping.values() if v != "(Calculated/Virtual)"}
        return [col for col in all_columns if col not in mapped_cols]
    
    def validate_mapping(self, proposed_mapping: Dict[str, str], 
                        all_db_columns: List[str]) -> Dict[str, List[str]]:
        """
        Validate a proposed mapping configuration.
        
        Returns:
            Dictionary with 'errors' and 'warnings' lists
        """
        errors = []
        warnings = []
        
        # Check for duplicate database columns
        db_cols = [v for v in proposed_mapping.values() if v != "(Calculated/Virtual)"]
        if len(db_cols) != len(set(db_cols)):
            duplicates = [col for col in db_cols if db_cols.count(col) > 1]
            errors.append(f"Duplicate database column mappings: {', '.join(set(duplicates))}")
        
        # Check for unmapped required fields
        required_fields = {"Customer", "Policy Number", "Agent Estimated Comm $", "Agent Paid Amount (STMT)"}
        unmapped_required = [field for field in required_fields 
                           if field not in proposed_mapping or proposed_mapping[field] == "(Calculated/Virtual)"]
        if unmapped_required:
            warnings.append(f"Unmapped required fields: {', '.join(unmapped_required)}")
        
        # Check for invalid database columns
        invalid_cols = [v for v in proposed_mapping.values() 
                       if v != "(Calculated/Virtual)" and v not in all_db_columns]
        if invalid_cols:
            errors.append(f"Invalid database columns: {', '.join(invalid_cols)}")
        
        return {"errors": errors, "warnings": warnings}
    
    def save_mapping(self, new_mapping: Dict[str, str], 
                    all_db_columns: List[str]) -> Dict[str, Union[bool, List[str]]]:
        """
        Save a new mapping configuration after validation.
        
        Returns:
            Dictionary with 'success' bool and any 'errors' or 'warnings'
        """
        validation = self.validate_mapping(new_mapping, all_db_columns)
        
        if validation["errors"]:
            return {"success": False, "errors": validation["errors"]}
        
        try:
            with open(self.mapping_file, "w") as f:
                json.dump(new_mapping, f, indent=2)
            self.clear_cache()
            return {"success": True, "warnings": validation["warnings"]}
        except Exception as e:
            return {"success": False, "errors": [f"Failed to save mapping: {str(e)}"]}
    
    def get_ledger_column_mapping(self) -> Dict[str, str]:
        """Get mapping for Policy Revenue Ledger columns."""
        return {
            "Transaction ID": self.get_db_column("Transaction ID"),
            "Transaction Date": self.get_db_column("STMT DATE", fallback_to_ui=False) or self.get_db_column("Transaction Date"),
            "Description": self.get_db_column("Description"),
            "Credit (Commission Owed)": self.get_db_column("Agent Estimated Comm $"),
            "Debit (Paid to Agent)": self.get_db_column("Agent Paid Amount (STMT)"),
            "Transaction Type": self.get_db_column("Transaction Type")
        }
    
    def apply_column_mapping_to_dataframe(self, df: pd.DataFrame, 
                                        reverse: bool = False) -> pd.DataFrame:
        """
        Apply column mapping to rename DataFrame columns.
        
        Args:
            df: DataFrame to process
            reverse: If True, map from UI names to database names
            
        Returns:
            DataFrame with renamed columns
        """
        df_copy = df.copy()
        
        if reverse:
            # UI field names -> database column names
            rename_dict = {}
            for col in df_copy.columns:
                db_col = self.get_db_column(col, fallback_to_ui=False)
                if db_col:
                    rename_dict[col] = db_col
        else:
            # Database column names -> UI field names  
            reverse_mapping = self._get_reverse_mapping()
            rename_dict = {col: reverse_mapping.get(col, col) for col in df_copy.columns}
        
        return df_copy.rename(columns=rename_dict)


# Global instance for easy import
column_mapper = ColumnMapper()


def get_mapped_column(ui_field: str, fallback_to_ui: bool = True) -> Optional[str]:
    """Convenience function to get database column name."""
    return column_mapper.get_db_column(ui_field, fallback_to_ui)


def get_ui_field_name(db_column: str) -> str:
    """Convenience function to get UI field name."""
    return column_mapper.get_ui_field(db_column) or db_column


def is_calculated_field(ui_field: str) -> bool:
    """Convenience function to check if field is calculated."""
    return column_mapper.is_calculated_field(ui_field)


def safe_column_reference(df: pd.DataFrame, ui_field: str, 
                         default_value=None, return_series: bool = True):
    """
    Safely reference a column in a DataFrame using UI field name.
    
    Args:
        df: DataFrame to reference
        ui_field: UI field name 
        default_value: Value to return/fill if column not found
        return_series: If True, return Series; if False, return values
        
    Returns:
        Series or values from the mapped column, or default_value if not found
    """
    db_col = get_mapped_column(ui_field)
    
    if db_col and db_col in df.columns:
        if return_series:
            return df[db_col]
        else:
            return df[db_col].values
    else:
        if return_series:
            return pd.Series([default_value] * len(df), index=df.index)
        else:
            return [default_value] * len(df)


def get_formula_columns() -> Dict[str, str]:
    """Get mapping of calculated columns to their formulas."""
    return {
        "Agent Estimated Comm $": "Premium Sold * (Policy Gross Comm % / 100) * (Agent Comm % / 100)",
        "Agency Estimated Comm/Revenue (CRM)": "Premium Sold * (Policy Gross Comm % / 100)",
        "Policy Balance Due": "Agent Estimated Comm $ - Agent Paid Amount (STMT)",
        "PAST DUE": "Policy Balance Due (for overdue policies)",
        "Agent Comm (New 50% RWL 25%)": "50% for NEW transactions, 25% for RWL/RENEWAL"
    }
