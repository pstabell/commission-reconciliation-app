# Configurable Default Agent Commission Rates

**Added**: January 6, 2025  
**Version**: 4.1.0

## Overview

The system now supports configurable default agent commission rates through the Admin Panel. Previously, these rates were hardcoded at 50% for new business and 25% for renewals. Users can now modify these defaults to match their business needs.

## Features

### Admin Panel Configuration
- New tab: "Default Agent Rates" in Admin Panel
- View current default rates at a glance
- Update rates with a simple form
- Changes are saved to a configuration file
- Detailed documentation about rate application

### Configuration Storage
Location: `config_files/default_agent_commission_rates.json`

```json
{
  "new_business_rate": 50.0,
  "renewal_rate": 25.0,
  "description": "Default agent commission rates (percentage) for transactions when no specific commission rule applies",
  "last_updated": "2025-09-06"
}
```

### Rate Application Logic

The system applies rates based on transaction type:

1. **NEW Transactions**: Uses `new_business_rate`
2. **RWL (Renewal) Transactions**: Uses `renewal_rate`
3. **NBS, STL, BoR Transactions**: Uses `new_business_rate` (treated as new business)
4. **CAN/XCL (Cancellation) Transactions**:
   - With Prior Policy Number → Uses `renewal_rate` (negative)
   - Without Prior Policy Number → Uses `new_business_rate` (negative)
5. **END/PCH Transactions**:
   - If Policy Origination Date = Effective Date → Uses `new_business_rate`
   - Otherwise → Uses `renewal_rate`
6. **Other Transaction Types**: 
   - With Prior Policy Number → Uses `renewal_rate`
   - Without Prior Policy Number → Uses `new_business_rate`

## Usage

### Updating Default Rates
1. Navigate to **Admin Panel** → **Default Agent Rates** tab
2. View current rates in the metrics display
3. Enter new rates in the "Update Default Rates" form
4. Click "Save Rates"
5. Confirmation message appears and page refreshes

### Important Notes
- Changes only affect **new** transactions created after the update
- Existing transactions retain their original commission rates
- Individual transactions can still be manually overridden when editing
- Default rates apply when no specific carrier/MGA commission rule exists

## Technical Implementation

### Files Modified
- `commission_app.py`: 
  - Added tab11 in Admin Panel for rate configuration
  - Updated Add New Policy Transaction form to load rates from config
  - Fixed END/PCH logic to check dates properly

### Files Created
- `config_files/default_agent_commission_rates.json`: Stores the configurable rates

### Fallback Behavior
If the configuration file is missing or corrupted:
- System falls back to original defaults (50% new, 25% renewal)
- No errors are shown to users
- Rates can be re-saved through the Admin Panel to recreate the file

## Environment Behavior
This feature works identically in both personal and production environments. The configuration file is local to each deployment.