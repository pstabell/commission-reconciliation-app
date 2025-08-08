#!/bin/bash
# Emergency rollback script for customer search feature
cp commission_app_20250807_before_customer_search.py commission_app.py
echo "✅ Rolled back to pre-customer-search version"
echo "Please restart Streamlit and clear browser cache"