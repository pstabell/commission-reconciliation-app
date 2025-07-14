# Database Migration Guide

**Created**: July 13, 2025  
**Last Updated**: July 13, 2025  
**Purpose**: Track all database schema changes and migration scripts

## Overview

This document provides a comprehensive record of all database schema changes, migration scripts, and update procedures for the Sales Commission App. Each migration is documented with its purpose, SQL scripts, rollback procedures, and impact assessment.

## Migration Naming Convention

All migration scripts follow this naming pattern:
```
YYYY-MM-DD_version_description.sql
Example: 2025-07-13_v3.6.0_contacts_commission_structure.sql
```

## Migrations

### v3.6.0 - Contacts & Commission Structure (July 13, 2025)

**Purpose**: Add carrier, MGA, and commission rule management capabilities

#### New Tables Created

##### 1. carriers
```sql
-- Create carriers table
CREATE TABLE IF NOT EXISTS carriers (
    carrier_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    carrier_name TEXT UNIQUE NOT NULL,
    naic_code TEXT,
    producer_code TEXT,
    parent_company TEXT,
    status TEXT DEFAULT 'Active' CHECK (status IN ('Active', 'Inactive')),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster lookups
CREATE INDEX idx_carriers_name ON carriers(carrier_name);
CREATE INDEX idx_carriers_status ON carriers(status);

-- Create update trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_carriers_updated_at BEFORE UPDATE
    ON carriers FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

##### 2. mgas
```sql
-- Create mgas table
CREATE TABLE IF NOT EXISTS mgas (
    mga_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    mga_name TEXT UNIQUE NOT NULL,
    contact_info JSONB DEFAULT '{}',
    appointment_date DATE,
    status TEXT DEFAULT 'Active' CHECK (status IN ('Active', 'Inactive')),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_mgas_name ON mgas(mga_name);
CREATE INDEX idx_mgas_status ON mgas(status);

-- Create update trigger
CREATE TRIGGER update_mgas_updated_at BEFORE UPDATE
    ON mgas FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

##### 3. carrier_mga_relationships
```sql
-- Create carrier-MGA relationship table
CREATE TABLE IF NOT EXISTS carrier_mga_relationships (
    relationship_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    carrier_id UUID NOT NULL REFERENCES carriers(carrier_id) ON DELETE CASCADE,
    mga_id UUID NOT NULL REFERENCES mgas(mga_id) ON DELETE CASCADE,
    is_direct BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(carrier_id, mga_id)
);

-- Create indexes for foreign keys
CREATE INDEX idx_carrier_mga_carrier ON carrier_mga_relationships(carrier_id);
CREATE INDEX idx_carrier_mga_mga ON carrier_mga_relationships(mga_id);
```

##### 4. commission_rules
```sql
-- Create commission rules table
CREATE TABLE IF NOT EXISTS commission_rules (
    rule_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    carrier_id UUID NOT NULL REFERENCES carriers(carrier_id) ON DELETE CASCADE,
    mga_id UUID REFERENCES mgas(mga_id) ON DELETE CASCADE,
    state TEXT DEFAULT 'FL',
    policy_type TEXT,
    term_months INTEGER CHECK (term_months IN (3, 6, 9, 12)),
    new_rate DECIMAL(5,2) NOT NULL CHECK (new_rate >= 0 AND new_rate <= 100),
    renewal_rate DECIMAL(5,2) CHECK (renewal_rate >= 0 AND renewal_rate <= 100),
    payment_terms TEXT CHECK (payment_terms IN ('Advanced', 'As Earned', NULL)),
    rule_description TEXT,
    rule_priority INTEGER GENERATED ALWAYS AS (
        CASE 
            WHEN mga_id IS NOT NULL THEN 1000 
            ELSE 0 
        END +
        CASE 
            WHEN state IS NOT NULL THEN 100 
            ELSE 0 
        END +
        CASE 
            WHEN policy_type IS NOT NULL THEN 10 
            ELSE 0 
        END +
        CASE 
            WHEN term_months IS NOT NULL THEN 1 
            ELSE 0 
        END
    ) STORED,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for lookups
CREATE INDEX idx_commission_rules_carrier ON commission_rules(carrier_id);
CREATE INDEX idx_commission_rules_mga ON commission_rules(mga_id);
CREATE INDEX idx_commission_rules_priority ON commission_rules(rule_priority DESC);
CREATE INDEX idx_commission_rules_lookup ON commission_rules(carrier_id, mga_id, state, policy_type);

-- Create update trigger
CREATE TRIGGER update_commission_rules_updated_at BEFORE UPDATE
    ON commission_rules FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

#### Updates to Existing Tables

##### policies table modifications
```sql
-- Add new columns to policies table (all nullable for backward compatibility)
ALTER TABLE policies 
ADD COLUMN IF NOT EXISTS carrier_id UUID REFERENCES carriers(carrier_id),
ADD COLUMN IF NOT EXISTS mga_id UUID REFERENCES mgas(mga_id),
ADD COLUMN IF NOT EXISTS commission_rule_id UUID REFERENCES commission_rules(rule_id),
ADD COLUMN IF NOT EXISTS commission_rate_override DECIMAL(5,2);

-- Create indexes for new foreign keys
CREATE INDEX IF NOT EXISTS idx_policies_carrier ON policies(carrier_id);
CREATE INDEX IF NOT EXISTS idx_policies_mga ON policies(mga_id);
CREATE INDEX IF NOT EXISTS idx_policies_rule ON policies(commission_rule_id);
```

#### Initial Data Population

##### Import carriers from Excel data
```sql
-- Insert initial carriers (examples from Excel analysis)
INSERT INTO carriers (carrier_name, status) VALUES
    ('Citizens Property Insurance', 'Active'),
    ('Progressive Insurance', 'Active'),
    ('AAA Insurance', 'Active'),
    ('State Farm', 'Active'),
    ('Neptune Flood', 'Active'),
    ('Wright National Flood', 'Active'),
    ('Olympus Insurance', 'Active'),
    ('Edison Insurance', 'Active'),
    ('Tower Hill', 'Active'),
    ('Heritage Property & Casualty', 'Active'),
    ('Universal Property & Casualty', 'Active'),
    ('SafePoint Insurance', 'Active'),
    ('Southern Fidelity', 'Active'),
    ('American Traditions', 'Active'),
    ('Centauri Specialty', 'Active'),
    ('FIGA', 'Active'),
    ('FedNat Insurance', 'Active'),
    ('Scottsdale Insurance', 'Active'),
    ('Florida Peninsula', 'Active'),
    ('American Integrity', 'Active'),
    ('Homeowners Choice', 'Active'),
    ('Mercury Insurance', 'Active')
ON CONFLICT (carrier_name) DO NOTHING;
```

##### Import MGAs
```sql
-- Insert initial MGAs
INSERT INTO mgas (mga_name, status) VALUES
    ('SureTec', 'Active'),
    ('FAIA', 'Active'),
    ('TWFG-Frenkel', 'Active'),
    ('Tower Hill Signature', 'Active'),
    ('Orchid Underwriters', 'Active'),
    ('Burns & Wilcox', 'Active'),
    ('BTIS', 'Active'),
    ('Advantage Partners', 'Active'),
    ('One80 Intermediaries', 'Active'),
    ('Distinguished Programs', 'Active'),
    ('CRC', 'Active')
ON CONFLICT (mga_name) DO NOTHING;
```

##### Create sample commission rules
```sql
-- Citizens default rule
INSERT INTO commission_rules (carrier_id, new_rate, renewal_rate, payment_terms, rule_description, is_default)
SELECT carrier_id, 10.00, 10.00, 'As Earned', 'Citizens default commission rate', true
FROM carriers WHERE carrier_name = 'Citizens Property Insurance';

-- Progressive product-specific rules (mono-line in FL)
INSERT INTO commission_rules (carrier_id, policy_type, new_rate, renewal_rate, payment_terms, rule_description)
SELECT carrier_id, 'Auto', 12.00, 12.00, 'Advanced', 'Progressive Auto commission'
FROM carriers WHERE carrier_name = 'Progressive Insurance';

-- AAA multi-product rules
INSERT INTO commission_rules (carrier_id, policy_type, new_rate, renewal_rate, payment_terms, rule_description)
SELECT carrier_id, policy_type, new_rate, renewal_rate, 'As Earned', description
FROM carriers, (VALUES 
    ('HO3', 15.00, 15.00, 'AAA Home with membership'),
    ('Auto', 12.00, 12.00, 'AAA Auto package'),
    ('PUP', 10.00, 10.00, 'AAA Umbrella')
) AS rules(policy_type, new_rate, renewal_rate, description)
WHERE carrier_name = 'AAA Insurance';
```

#### Migration Validation

##### Check table creation
```sql
-- Verify all tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('carriers', 'mgas', 'carrier_mga_relationships', 'commission_rules')
ORDER BY table_name;

-- Verify policies table modifications
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'policies'
AND column_name IN ('carrier_id', 'mga_id', 'commission_rule_id', 'commission_rate_override')
ORDER BY column_name;

-- Check data population
SELECT 'Carriers' as table_name, COUNT(*) as record_count FROM carriers
UNION ALL
SELECT 'MGAs', COUNT(*) FROM mgas
UNION ALL
SELECT 'Commission Rules', COUNT(*) FROM commission_rules;
```

#### Rollback Script

```sql
-- Remove columns from policies table
ALTER TABLE policies 
DROP COLUMN IF EXISTS carrier_id,
DROP COLUMN IF EXISTS mga_id,
DROP COLUMN IF EXISTS commission_rule_id,
DROP COLUMN IF EXISTS commission_rate_override;

-- Drop tables in reverse dependency order
DROP TABLE IF EXISTS commission_rules;
DROP TABLE IF EXISTS carrier_mga_relationships;
DROP TABLE IF EXISTS mgas;
DROP TABLE IF EXISTS carriers;

-- Drop function if no other tables use it
DROP FUNCTION IF EXISTS update_updated_at_column();
```

#### Impact Assessment

**Risk Level**: Low
- All changes are additive
- No modifications to existing data
- Full backward compatibility maintained
- Existing policies continue to function without carrier/MGA data

**Performance Impact**: Minimal
- Indexes added for all foreign keys
- Efficient rule lookup with composite index
- Priority calculation is stored, not computed

**Testing Required**:
1. Verify existing policy operations work unchanged
2. Test carrier/MGA CRUD operations
3. Validate commission rule matching
4. Ensure proper cascade deletes
5. Check update triggers function correctly

### v3.5.0 - Prior Policy Number (July 10, 2025)

**Purpose**: Add policy renewal tracking with Prior Policy Number field

#### Schema Change

```sql
-- Add Prior Policy Number column
ALTER TABLE policies 
ADD COLUMN IF NOT EXISTS "Prior Policy Number" TEXT;

-- Create index for efficient lookups
CREATE INDEX IF NOT EXISTS idx_policies_prior_policy 
ON policies("Prior Policy Number");
```

#### Data Migration

```sql
-- Rename existing column for consistency
ALTER TABLE policies 
RENAME COLUMN "NEW BIZ CHECKLIST COMPLETE" TO "Policy Checklist Complete";
```

#### Rollback

```sql
-- Remove Prior Policy Number column
ALTER TABLE policies 
DROP COLUMN IF EXISTS "Prior Policy Number";

-- Revert column rename
ALTER TABLE policies 
RENAME COLUMN "Policy Checklist Complete" TO "NEW BIZ CHECKLIST COMPLETE";
```

### v3.6.3 - Import Transaction Protection (July 14, 2025)

**Purpose**: Protect import-created transactions from accidental deletion while allowing data completion

#### Database Function Update

Updated the transaction ID validation function to accept -IMPORT suffix:

```sql
-- Update validation function to accept -IMPORT pattern
CREATE OR REPLACE FUNCTION validate_transaction_id_format(trans_id TEXT) RETURNS BOOLEAN AS $$
BEGIN
    -- Existing validation logic...
    
    ELSIF trans_id LIKE '%-IMPORT' THEN
        -- Format: XXXXXXX-IMPORT (for import-created transactions)
        RETURN LENGTH(SPLIT_PART(trans_id, '-', 1)) = 7
           AND SPLIT_PART(trans_id, '-', 2) = 'IMPORT';
    
    -- Rest of function...
END;
$$ LANGUAGE plpgsql;
```

#### Data Migration

Migrated existing import-created transactions to new format:

```sql
-- Update existing import-created transactions to use -IMPORT suffix
UPDATE policies
SET "Transaction ID" = "Transaction ID" || '-IMPORT'
WHERE "DESCRIPTION" LIKE '%Created from statement import%'
  AND "Transaction ID" NOT LIKE '%-IMPORT'
  AND "Transaction ID" !~ '-[A-Z]+-[0-9]{8}$';

-- Total: 45 transactions migrated
```

#### Application Changes

1. **Transaction ID Generation**:
   - Updated `generate_transaction_id()` to accept optional suffix parameter
   - New imports automatically use -IMPORT suffix

2. **Edit Protection**:
   - Payment fields moved to Internal Fields as read-only
   - Premium/commission fields remain editable
   - Comprehensive explanation box at top of form

3. **Delete Protection**:
   - Cannot be deleted from Edit Policy Transactions
   - Clear error message explaining why

#### Impact Assessment

**Risk Level**: Low
- Function update is backward compatible
- Migration only affects specific transactions
- No impact on existing functionality
- Full rollback possible if needed

#### Rollback Script

```sql
-- Remove -IMPORT suffix from transaction IDs
UPDATE policies
SET "Transaction ID" = SPLIT_PART("Transaction ID", '-IMPORT', 1)
WHERE "Transaction ID" LIKE '%-IMPORT';

-- Revert validation function (if needed)
-- Note: Function remains backward compatible, so revert may not be necessary
```

## Migration Best Practices

### Before Running Migrations

1. **Backup Database**
   ```sql
   -- In Supabase Dashboard, use Database Backups feature
   -- Or export schema and data
   ```

2. **Test in Development**
   - Run migration on test database first
   - Verify all functionality works as expected
   - Check for performance impacts

3. **Communication**
   - Notify users of planned maintenance
   - Schedule during low-usage periods
   - Have rollback plan ready

### Migration Execution

1. **Run in Transaction** (when possible)
   ```sql
   BEGIN;
   -- Migration SQL here
   COMMIT;
   ```

2. **Verify Each Step**
   - Check table creation
   - Validate data population
   - Test application functionality

3. **Document Results**
   - Record execution time
   - Note any issues encountered
   - Update this document

### Post-Migration

1. **Monitor Performance**
   - Check query execution times
   - Watch for errors in logs
   - Verify data integrity

2. **User Validation**
   - Have users test key workflows
   - Gather feedback on changes
   - Address any issues quickly

## Common Issues and Solutions

### Foreign Key Violations

**Issue**: Cannot add foreign key due to orphaned records
```sql
-- Find orphaned records
SELECT * FROM policies 
WHERE carrier_id IS NOT NULL 
AND carrier_id NOT IN (SELECT carrier_id FROM carriers);
```

**Solution**: Clean up data before adding constraint
```sql
-- Set orphaned records to NULL
UPDATE policies 
SET carrier_id = NULL 
WHERE carrier_id NOT IN (SELECT carrier_id FROM carriers);
```

### Performance Degradation

**Issue**: Queries slow after adding new columns

**Solution**: Add appropriate indexes
```sql
-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM policies WHERE carrier_id = '...';

-- Add index if needed
CREATE INDEX idx_policies_carrier ON policies(carrier_id);
```

### Migration Failures

**Issue**: Migration partially completes

**Solution**: Use transactions and checkpoints
```sql
-- Use savepoints for complex migrations
BEGIN;
SAVEPOINT before_carriers;
-- Create carriers table
SAVEPOINT before_rules;
-- Create rules table
-- If error, rollback to savepoint
ROLLBACK TO before_rules;
```

## Version History

| Version | Date | Description | Risk Level |
|---------|------|-------------|------------|
| v3.6.3 | 2025-07-14 | Added Import Transaction Protection | Low |
| v3.6.0 | 2025-07-13 | Added Contacts & Commission Structure | Low |
| v3.5.0 | 2025-07-10 | Added Prior Policy Number tracking | Low |
| v3.0.0 | 2025-07-03 | Initial Supabase migration | High |

---

*This document should be updated with each database schema change. Always test migrations in development before applying to production.*