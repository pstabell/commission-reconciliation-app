"""
Safe data operations wrapper for the commission app.
Provides consistent error handling for all data operations.
"""

import pandas as pd
import streamlit as st
from typing import Optional, List, Any, Dict, Union
import datetime

def safe_data_operation(func):
    """Decorator to wrap data operations with error handling."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"Data operation error: {str(e)}")
            return None
    return wrapper

class SafeDataFrame:
    """Wrapper class for DataFrame with safe operations."""
    
    def __init__(self, df: Optional[pd.DataFrame] = None):
        """Initialize with optional DataFrame."""
        self.df = df if df is not None else pd.DataFrame()
        self._empty = df is None or df.empty
    
    @property
    def empty(self) -> bool:
        """Check if DataFrame is empty."""
        return self._empty
    
    def __len__(self) -> int:
        """Return length of DataFrame."""
        return 0 if self._empty else len(self.df)
    
    def get_column(self, column: str, default=None) -> pd.Series:
        """Safely get a column, returning empty Series if not found."""
        if self._empty or column not in self.df.columns:
            return pd.Series(dtype=object)
        return self.df[column].fillna(default) if default is not None else self.df[column]
    
    def filter_contains(self, column: str, search_term: str, case=False) -> 'SafeDataFrame':
        """Safely filter rows containing search term."""
        if self._empty or column not in self.df.columns:
            return SafeDataFrame()
        
        try:
            mask = self.df[column].astype(str).str.contains(search_term, case=case, na=False)
            return SafeDataFrame(self.df[mask].copy())
        except:
            return SafeDataFrame()
    
    def filter_equals(self, column: str, value: Any) -> 'SafeDataFrame':
        """Safely filter rows where column equals value."""
        if self._empty or column not in self.df.columns:
            return SafeDataFrame()
        
        try:
            mask = self.df[column] == value
            return SafeDataFrame(self.df[mask].copy())
        except:
            return SafeDataFrame()
    
    def groupby_sum(self, by_columns: Union[str, List[str]], sum_column: str) -> pd.DataFrame:
        """Safely perform groupby sum operation."""
        if self._empty:
            return pd.DataFrame()
        
        # Ensure by_columns is a list
        if isinstance(by_columns, str):
            by_columns = [by_columns]
        
        # Check all columns exist
        missing_cols = [col for col in by_columns + [sum_column] if col not in self.df.columns]
        if missing_cols:
            return pd.DataFrame()
        
        try:
            return self.df.groupby(by_columns)[sum_column].sum().reset_index()
        except:
            return pd.DataFrame()
    
    def count_unique(self, column: str) -> int:
        """Safely count unique values in a column."""
        if self._empty or column not in self.df.columns:
            return 0
        
        try:
            return self.df[column].nunique()
        except:
            return 0
    
    def sum_column(self, column: str, default: float = 0.0) -> float:
        """Safely sum a column."""
        if self._empty or column not in self.df.columns:
            return default
        
        try:
            return float(self.df[column].sum())
        except:
            return default
    
    def to_dataframe(self) -> pd.DataFrame:
        """Return the underlying DataFrame."""
        return self.df
    
    def search_multiple_columns(self, search_term: str, columns: List[str]) -> 'SafeDataFrame':
        """Search across multiple columns safely."""
        if self._empty or not search_term:
            return SafeDataFrame()
        
        mask = pd.Series(False, index=self.df.index)
        for col in columns:
            if col in self.df.columns:
                try:
                    mask |= self.df[col].astype(str).str.contains(search_term, case=False, na=False)
                except:
                    continue
        
        return SafeDataFrame(self.df[mask].copy()) if mask.any() else SafeDataFrame()
    
    def format_date_columns(self, date_columns: List[str], format_str: str = '%Y-%m-%d') -> None:
        """Safely format date columns."""
        if self._empty:
            return
        
        for col in date_columns:
            if col in self.df.columns:
                try:
                    self.df[col] = pd.to_datetime(self.df[col], errors='coerce').dt.strftime(format_str)
                except:
                    continue

def create_empty_commission_dataframe() -> pd.DataFrame:
    """Create an empty DataFrame with all expected commission tracking columns."""
    columns = [
        '_id', 'Transaction ID', 'Client ID', 'Customer',
        'Policy Number', 'Prior Policy Number',
        'Carrier Name', 'MGA Name', 'Policy Type', 'Transaction Type',
        'Effective Date', 'X-DATE', 'Policy Origination Date',
        'Policy Gross Comm %', 'Agent Gross Comm %',
        'Agent Estimated Comm $', 'Agency Estimated Comm $',
        'Premium', 'Insured Name', 'STMT DATE',
        'Agency Commission Received', 'Commission Paid',
        'Balance Due', 'Notes', 'reconciliation_status',
        'reconciliation_id', 'reconciliation_date'
    ]
    
    return pd.DataFrame(columns=columns)

def safe_calculate_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Safely calculate dashboard metrics even with missing columns."""
    safe_df = SafeDataFrame(df)
    
    metrics = {
        'total_transactions': len(safe_df),
        'unique_policies': safe_df.count_unique('Policy Number'),
        'total_premium': safe_df.sum_column('Premium', 0.0),
        'total_commission_paid': safe_df.sum_column('Commission Paid', 0.0),
        'total_commission_estimated': safe_df.sum_column('Agent Estimated Comm $', 0.0),
        'total_balance_due': safe_df.sum_column('Balance Due', 0.0)
    }
    
    return metrics

def safe_display_dataframe(df: pd.DataFrame, 
                          column_config: Optional[Dict] = None,
                          hide_columns: Optional[List[str]] = None,
                          key: Optional[str] = None) -> None:
    """Safely display a dataframe with error handling."""
    if df is None or df.empty:
        st.info("No data to display")
        return
    
    try:
        # Remove columns that should be hidden
        if hide_columns:
            display_df = df.drop(columns=[col for col in hide_columns if col in df.columns], errors='ignore')
        else:
            display_df = df
        
        # Display with column config if provided
        if column_config:
            st.dataframe(display_df, column_config=column_config, use_container_width=True, key=key)
        else:
            st.dataframe(display_df, use_container_width=True, key=key)
    except Exception as e:
        st.error(f"Error displaying data: {str(e)}")
        # Fallback to simple display
        st.dataframe(df)