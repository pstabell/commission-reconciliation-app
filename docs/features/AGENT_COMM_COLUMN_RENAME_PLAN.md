# Plan for Renaming "Agent Comm (NEW 50% RWL 25%)" to "Agent Comm %"

## Date: 2025-09-27

### 1. Impact Analysis

#### Database Impact:
- **Column exists in**: `policies` table in Supabase
- **Current column name**: `Agent Comm (NEW 50% RWL 25%)`
- **Target column name**: `Agent Comm %`

#### Code Impact:
- **40+ files** contain references to this column
- **Primary file**: `commission_app.py` (main application)
- **Configuration files**: 
  - `column_mapping_config.py` (lines 54-55)
  - `config_files/column_mapping.json` (lines 19-20)
  - `config_files/schema_info.json` (line 183)

#### Functional Areas Affected:
1. Add New Policy Transaction form
2. Edit Policy forms
3. Policy Revenue Ledger display
4. Reports generation
5. Import/Export functionality
6. Reconciliation features
7. Dashboard displays
8. Column mapping admin interface

### 2. Step-by-Step Implementation Plan

#### Phase 1: Database Preparation
1. **Backup current database**
2. **Create SQL migration script**:
   ```sql
   -- Add new column
   ALTER TABLE policies ADD COLUMN "Agent Comm %" TEXT;
   
   -- Copy data from old column
   UPDATE policies SET "Agent Comm %" = "Agent Comm (NEW 50% RWL 25%)";
   
   -- After verification, drop old column
   ALTER TABLE policies DROP COLUMN "Agent Comm (NEW 50% RWL 25%)";
   ```

#### Phase 2: Code Updates
1. **Update column mapping configuration**:
   - `column_mapping_config.py`: Update both variations (lines 54-55)
   - `config_files/column_mapping.json`: Update mapping
   - `config_files/schema_info.json`: Update schema definition

2. **Search and replace in main app**:
   - Replace all occurrences of `"Agent Comm (NEW 50% RWL 25%)"` with `"Agent Comm %"`
   - Handle both uppercase and mixed case variations

3. **Update formula references**:
   - Check calculation formulas that reference this column
   - Update help text and documentation

#### Phase 3: Template and Report Updates
1. **Update saved templates**:
   - Check `config_files/prl_templates.json` for saved templates using old column name
   - Create migration script to update template configurations

2. **Update any hardcoded report configurations**

#### Phase 4: Testing Plan
1. **Test all CRUD operations**:
   - Add new policy
   - Edit existing policy
   - View policy details
   - Delete policy

2. **Test reporting features**:
   - Policy Revenue Ledger Reports
   - Export functionality
   - Import functionality

3. **Test column mapping admin**:
   - Verify new column appears correctly
   - Test remapping functionality

### 3. Risk Mitigation

#### Rollback Strategy:
1. Keep database backup before changes
2. Keep code backup (already timestamped)
3. Prepare rollback SQL script:
   ```sql
   ALTER TABLE policies ADD COLUMN "Agent Comm (NEW 50% RWL 25%)" TEXT;
   UPDATE policies SET "Agent Comm (NEW 50% RWL 25%)" = "Agent Comm %";
   ALTER TABLE policies DROP COLUMN "Agent Comm %";
   ```

#### Compatibility Considerations:
1. **Import/Export**: Update import mappings to handle both old and new column names
2. **Templates**: Auto-migrate saved templates
3. **Historical data**: Ensure no data loss during migration

### 4. Implementation Timeline

1. **Hour 1**: Database backup and migration script preparation
2. **Hour 2**: Code updates and configuration changes
3. **Hour 3**: Testing and verification
4. **Hour 4**: Documentation updates and deployment

### 5. Post-Implementation Tasks

1. Update user documentation
2. Notify users of the change (if needed)
3. Monitor for any issues
4. Update any external integrations

### 6. Alternative Approach (Less Risky)

Instead of renaming the database column, we could:
1. Keep the database column name unchanged
2. Only update the UI display name through column mapping
3. This would require minimal code changes and no database migration

**Recommendation**: Start with the alternative approach (UI-only change) first, then consider full database migration if needed.

### 7. UI-Only Implementation (Recommended First Step)

This approach changes only what users see, without touching the database:

1. **Update Admin Panel Column Mapping**:
   - Go to Admin Panel → Column Mapping
   - Find "Agent Comm (NEW 50% RWL 25%)"
   - Change the UI Field Name to "Agent Comm %"
   - Save the mapping

2. **Benefits**:
   - No database migration required
   - No risk of data loss
   - Instant rollback possible
   - Can be done without code changes

3. **Limitations**:
   - Database column name remains verbose
   - SQL queries will still use old name
   - Export files will show old name unless specifically mapped

### 8. Code References for Full Implementation

Key locations that need updates:

1. **commission_app.py**:
   - Line ~3705: Form display for Agent Comm %
   - Line ~3765: Modal display key
   - Multiple references throughout for calculations

2. **column_mapping_config.py**:
   - Lines 54-55: Both case variations
   - Line 309: Formula reference

3. **Configuration files**:
   - `config_files/column_mapping.json`
   - `config_files/schema_info.json`
   - Any saved templates in `config_files/prl_templates.json`

### 9. SQL Scripts Needed

```sql
-- Check current column usage
SELECT COUNT(*) FROM policies WHERE "Agent Comm (NEW 50% RWL 25%)" IS NOT NULL;

-- Migration script
BEGIN;
ALTER TABLE policies ADD COLUMN "Agent Comm %" TEXT;
UPDATE policies SET "Agent Comm %" = "Agent Comm (NEW 50% RWL 25%)";
-- Verify data
SELECT COUNT(*) FROM policies WHERE "Agent Comm %" != "Agent Comm (NEW 50% RWL 25%)" OR ("Agent Comm %" IS NULL AND "Agent Comm (NEW 50% RWL 25%)" IS NOT NULL);
-- If count is 0, proceed
ALTER TABLE policies DROP COLUMN "Agent Comm (NEW 50% RWL 25%)";
COMMIT;
```

### 10. Decision Points

Before proceeding, decide:

1. **UI-only or full database change?**
2. **Timing of implementation?**
3. **Need for user notification?**
4. **Backup and rollback procedures?**

### Recommendation

Start with the UI-only approach through Admin Panel column mapping. This provides:
- Immediate user benefit
- Zero risk
- Easy rollback
- Time to plan full migration if needed

The full database migration can be scheduled later if the UI-only approach proves insufficient.