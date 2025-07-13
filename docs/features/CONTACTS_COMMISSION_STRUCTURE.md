# Contacts & Commission Structure System

**Created**: July 13, 2025  
**Version**: 3.6.0  
**Status**: Implemented

## Overview

The Contacts & Commission Structure system provides comprehensive management of insurance carriers, MGAs (Managing General Agencies), and automated commission rate calculations. This feature transforms commission management from manual entry to intelligent automation while maintaining complete backward compatibility.

## Key Features

### 1. Contacts Page
A dedicated page with two main tabs for managing business relationships:

#### Carriers Tab
- **Add/Edit Carriers**: Comprehensive carrier information management
- **Fields Tracked**:
  - Carrier Name (unique)
  - NAIC Code
  - Producer Code
  - Parent Company
  - Status (Active/Inactive)
  - Notes
- **Commission Rules**: Define default and specific rates per carrier
- **Direct Appointments**: Track which carriers have direct relationships

#### MGAs Tab
- **MGA Management**: Complete MGA relationship tracking
- **Contact Information**: Store detailed contact data in JSON format
- **Carrier Relationships**: Map which MGAs work with which carriers
- **Appointment Dates**: Track when relationships were established
- **Status Tracking**: Active/Inactive status management

### 2. Commission Rules Engine

The heart of the system - intelligent commission rate calculation based on multiple factors:

#### Rule Components
- **Carrier**: Which insurance carrier (required)
- **MGA**: Which MGA or Direct appointment (optional)
- **Policy Type**: Specific policy types (HO3, Auto, etc.)
- **State**: Currently Florida-focused, expandable
- **Term**: Policy duration in months
- **Transaction Type**: NEW vs RWL (renewal)

#### Rule Priority System
Rules are applied based on specificity (higher number = higher priority):
```
Base Priority Calculation:
- Carrier default: 0
- + State specified: +100
- + Policy Type specified: +10
- + MGA specified: +1000
- + Term specified: +1

Example:
- Citizens default: Priority 0
- Citizens + Florida: Priority 100
- Citizens + HO3: Priority 10
- Citizens + SureTec MGA + HO3: Priority 1010
```

#### Payment Terms
- **Advanced**: Commission paid upfront
- **As Earned**: Commission paid over policy term
- Special conditions tracked in notes

### 3. Integration with Policy Management

#### Add New Policy Enhancement
- **Carrier Dropdown**: Searchable selection of active carriers
- **MGA Dropdown**: Filtered by selected carrier's relationships
- **Auto-Population**: Commission rates fill based on applicable rules
- **Override Capability**: Manual override with reason tracking
- **Rule Display**: Shows which rule is being applied

#### Edit Policy Transaction
- **Carrier/MGA Assignment**: Add or update carrier relationships
- **Rate Comparison**: Shows rule rate vs actual rate
- **Reset to Rule**: Option to revert to calculated rate
- **Warning System**: Alerts when rates differ from rules

### 4. Modern Policy Types Configuration

#### Admin Panel Enhancement
- **Compact Grid Layout**: Visual organization of policy types
- **Category Grouping**:
  - Personal Lines (HO3, HO6, DP3, Auto)
  - Commercial (BOP, GL, WC)
  - Specialty (Flood, Wind, Boat, Cyber)
- **Configuration File**: `policy_types_updated.json`
- **Safe Management**: No direct database modifications
- **Backup/Restore**: Download configuration for safety

## Database Schema

### New Tables

#### carriers
```sql
CREATE TABLE carriers (
    carrier_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    carrier_name TEXT UNIQUE NOT NULL,
    naic_code TEXT,
    producer_code TEXT,
    parent_company TEXT,
    status TEXT DEFAULT 'Active',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### mgas
```sql
CREATE TABLE mgas (
    mga_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    mga_name TEXT UNIQUE NOT NULL,
    contact_info JSONB,
    appointment_date DATE,
    status TEXT DEFAULT 'Active',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### carrier_mga_relationships
```sql
CREATE TABLE carrier_mga_relationships (
    relationship_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    carrier_id UUID REFERENCES carriers(carrier_id),
    mga_id UUID REFERENCES mgas(mga_id),
    is_direct BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### commission_rules
```sql
CREATE TABLE commission_rules (
    rule_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    carrier_id UUID REFERENCES carriers(carrier_id),
    mga_id UUID REFERENCES mgas(mga_id),
    state TEXT DEFAULT 'FL',
    policy_type TEXT,
    term_months INTEGER,
    new_rate DECIMAL(5,2) NOT NULL,
    renewal_rate DECIMAL(5,2),
    payment_terms TEXT,
    rule_description TEXT,
    rule_priority INTEGER,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Updated Tables

#### policies (backward compatible additions)
```sql
ALTER TABLE policies 
ADD COLUMN carrier_id UUID REFERENCES carriers(carrier_id),
ADD COLUMN mga_id UUID REFERENCES mgas(mga_id),
ADD COLUMN commission_rule_id UUID REFERENCES commission_rules(rule_id),
ADD COLUMN commission_rate_override DECIMAL(5,2);
```

All new columns are nullable to maintain backward compatibility.

## Island Architecture

The Contacts page follows the application's island architecture pattern:

### Complete Isolation
- **Independent Module**: No dependencies on other pages
- **Error Containment**: Failures don't affect other functionality
- **Separate Data Loading**: Fresh data queries per page load
- **No Shared State**: Complete isolation from other pages

### Benefits
- **Bulletproof Design**: Can't crash other pages
- **Easy Debugging**: Issues isolated to Contacts module
- **Independent Development**: Built without touching existing code
- **Future Ready**: Prepared for modular architecture migration

## Real-World Data Import

### Initial Data Population
From Excel analysis, the system imported:
- **22 Unique Carriers**: Citizens, Progressive, AAA, State Farm, etc.
- **11 Distinct MGAs**: SureTec, FAIA, Tower Hill Signature, etc.
- **46 Commission Structures**: Various carrier/MGA combinations

### Commission Rate Patterns
- **NEW Rates**: Range from 6% to 20%
- **RWL Rates**: Often 2-4% lower than NEW
- **Same Rate**: Some carriers (Citizens) maintain same rate
- **Product-Specific**: Many carriers have different rates per product

### Complex Structures Handled
Examples of real-world complexity:
- **AAA**: 15% Home, 12% Auto, 10% Umbrella
- **Progressive**: Mono-line in FL (Auto only at 12%)
- **Citizens**: Flat 10% for both NEW and RWL
- **Specialty Products**: Higher rates for niche coverage

## User Interface

### Carrier Commission Rules Display
```
Citizens Property Insurance
├── Default Commission: NEW: 10% | RWL: 10% ✏️
└── Payment Terms: As Earned

Progressive Insurance
├── Default Commission: [No Default - Product Specific]
└── Specific Rules: [+ Add Rule]
    ├── Direct, Auto → NEW: 12% | RWL: 12% 🗑️
    ├── Direct, Boat → NEW: 10% | RWL: 10% 🗑️
    └── Direct, Renters → NEW: 15% | RWL: 15% 🗑️
```

### Rule Application Display
When adding a new policy:
```
Commission Details
├── Policy Gross Comm %: 15.00 [Auto-populated]
├── Applied Rule: "AAA Direct Home - 15%" [Info text]
├── ⚠️ Override Commission [Checkbox]
└── Override Reason: [Text field - appears if checked]
```

## Benefits

### For Users
- **Time Savings**: No manual commission rate lookup
- **Accuracy**: Reduces calculation errors
- **Flexibility**: Override when needed with tracking
- **Transparency**: Clear indication of applied rules

### For Business
- **Standardization**: Consistent commission application
- **Audit Trail**: Track overrides and exceptions
- **Scalability**: Handle complex carrier relationships
- **Reporting**: Commission rule usage analytics

## Future Enhancements

### Planned Features
1. **Rule Templates**: Copy rules between similar carriers
2. **Bulk Updates**: Update multiple rules simultaneously
3. **Rule History**: Track commission rate changes over time
4. **Multi-State Support**: Expand beyond Florida
5. **API Integration**: Import carrier data from external sources
6. **Commission Tiers**: Volume-based rate structures

### Potential Expansions
- Email notifications for rate changes
- Commission reconciliation reports
- Carrier performance analytics
- Automated rule suggestions based on patterns

## Technical Implementation Notes

### Performance Considerations
- Indexed lookups for fast rule matching
- Cached carrier/MGA lists for dropdowns
- Lazy loading for large datasets
- Efficient rule priority calculations

### Data Integrity
- Unique constraints on carrier/MGA names
- Foreign key relationships maintained
- Update triggers for timestamp tracking
- Nullable columns for backward compatibility

### Error Handling
- Graceful fallback to manual entry
- Clear error messages for users
- Logging for debugging
- Transaction rollback on failures

## Configuration Files

### policy_types_updated.json
```json
{
  "policy_types": {
    "personal": [
      {"code": "HO3", "name": "Homeowners 3", "active": true},
      {"code": "HO6", "name": "Condo", "active": true},
      {"code": "DP3", "name": "Dwelling", "active": true},
      {"code": "Auto", "name": "Personal Auto", "active": true}
    ],
    "commercial": [
      {"code": "BOP", "name": "Business Owners", "active": true},
      {"code": "GL", "name": "General Liability", "active": true},
      {"code": "WC", "name": "Workers Comp", "active": true}
    ],
    "specialty": [
      {"code": "Flood", "name": "Flood", "active": true},
      {"code": "Wind", "name": "Wind/Hail", "active": true},
      {"code": "Boat", "name": "Watercraft", "active": true}
    ]
  }
}
```

## Conclusion

The Contacts & Commission Structure system represents a major advancement in commission management capabilities. By implementing intelligent automation while maintaining complete backward compatibility, it provides immediate value without disrupting existing workflows. The island architecture ensures the feature remains isolated and maintainable, setting a pattern for future feature development.

---

*This documentation provides a complete reference for the Contacts & Commission Structure system implemented in version 3.6.0.*