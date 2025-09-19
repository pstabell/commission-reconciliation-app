"""
Test script to verify empty data handling throughout the app.
This simulates what new users experience with no data.
"""

import pandas as pd
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_validation_utils import (
    check_data_availability, validate_commission_data,
    safe_column_access, safe_filter_contains
)
from safe_data_operations import (
    SafeDataFrame, create_empty_commission_dataframe,
    safe_calculate_metrics, safe_display_dataframe
)

def test_empty_dataframe():
    """Test operations on empty dataframe."""
    print("Testing Empty DataFrame Operations")
    print("=" * 50)
    
    # Create empty dataframe
    empty_df = pd.DataFrame()
    safe_df = SafeDataFrame(empty_df)
    
    # Test basic properties
    print(f"Empty check: {safe_df.empty}")  # Should be True
    print(f"Length: {len(safe_df)}")  # Should be 0
    
    # Test column operations
    print(f"\nColumn access test:")
    result = safe_df.get_column('Customer')
    print(f"  - Get non-existent column: {len(result)} rows")  # Should be 0
    
    # Test filtering
    print(f"\nFilter test:")
    filtered = safe_df.filter_contains('Customer', 'Test')
    print(f"  - Filter on empty df: {len(filtered)} rows")  # Should be 0
    
    # Test groupby
    print(f"\nGroupby test:")
    grouped = safe_df.groupby_sum('Policy Type', 'Premium')
    print(f"  - Groupby on empty df: {len(grouped)} rows")  # Should be 0
    
    # Test metrics calculation
    print(f"\nMetrics test:")
    metrics = safe_calculate_metrics(empty_df)
    print(f"  - Total transactions: {metrics['total_transactions']}")  # Should be 0
    print(f"  - Total premium: ${metrics['total_premium']:,.2f}")  # Should be 0.00

def test_missing_columns():
    """Test operations on dataframe with missing expected columns."""
    print("\n\nTesting Missing Columns")
    print("=" * 50)
    
    # Create dataframe with only some columns
    partial_df = pd.DataFrame({
        'Customer': ['John Doe', 'Jane Smith'],
        'Policy Number': ['POL001', 'POL002']
    })
    safe_df = SafeDataFrame(partial_df)
    
    print(f"DataFrame has {len(safe_df)} rows")
    
    # Test accessing missing column
    premium = safe_df.get_column('Premium', default=0)
    print(f"Missing column 'Premium': {list(premium)}")  # Should be empty series
    
    # Test sum on missing column
    total = safe_df.sum_column('Commission Paid', default=0.0)
    print(f"Sum of missing column: ${total:,.2f}")  # Should be 0.00
    
    # Test validation
    is_valid, error_msg = validate_commission_data(partial_df)
    print(f"\nValidation result: {is_valid}")
    print(f"Error message: {error_msg}")

def test_safe_operations():
    """Test safe operations prevent crashes."""
    print("\n\nTesting Safe Operations")
    print("=" * 50)
    
    # Operations that would normally crash
    empty_df = pd.DataFrame()
    
    print("Testing operations that would normally crash:")
    
    # This would crash: empty_df['Customer'].str.contains('test')
    # Safe version:
    safe_df = SafeDataFrame(empty_df)
    result = safe_df.filter_contains('Customer', 'test')
    print(f"  ✅ Filter contains: {len(result)} results (no crash)")
    
    # This would crash: empty_df.groupby('Policy Type')['Premium'].sum()
    # Safe version:
    result = safe_df.groupby_sum('Policy Type', 'Premium')
    print(f"  ✅ Groupby sum: {len(result)} results (no crash)")
    
    # This would crash: empty_df['Policy Number'].nunique()
    # Safe version:
    count = safe_df.count_unique('Policy Number')
    print(f"  ✅ Count unique: {count} (no crash)")

def test_commission_dataframe_template():
    """Test the empty commission dataframe template."""
    print("\n\nTesting Commission DataFrame Template")
    print("=" * 50)
    
    template_df = create_empty_commission_dataframe()
    print(f"Template has {len(template_df.columns)} columns")
    print(f"First 5 columns: {list(template_df.columns[:5])}")
    
    # Verify key columns exist
    key_columns = ['Transaction ID', 'Customer', 'Policy Number', 'Premium', 'Commission Paid']
    for col in key_columns:
        exists = col in template_df.columns
        print(f"  - {col}: {'✅' if exists else '❌'}")

if __name__ == "__main__":
    print("EMPTY DATA HANDLING TEST SUITE")
    print("=" * 50)
    print("This tests how the app handles empty/missing data\n")
    
    test_empty_dataframe()
    test_missing_columns()
    test_safe_operations()
    test_commission_dataframe_template()
    
    print("\n\n✅ All tests completed!")
    print("The safe operations prevent crashes when data is empty or columns are missing.")