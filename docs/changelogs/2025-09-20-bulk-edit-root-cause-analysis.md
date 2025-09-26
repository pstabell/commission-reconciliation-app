# Bulk Edit Duplicate Crisis - Root Cause Analysis
**Date**: 2025-09-20
**Status**: CRITICAL - Needs Proper Fix

## The Real Problem

### Symptom
- Single edits: Work fine (mostly)
- Bulk edits: Create massive duplicates (425 → 1,188 records)
- Database has 3x the records that should exist
- App shows filtered view (383) while database has 1,188

### Root Cause
1. **Session State Failure**: The `original_data` from session state becomes stale/corrupted during bulk edits
2. **Comparison Fails**: When session state comparison fails, the code treats ALL rows as "new"
3. **Fallback Logic**: Instead of aborting, it processes everything as INSERT instead of UPDATE
4. **Transaction ID Check Bypassed**: The safety checks are inside the wrong conditional blocks

### Why Current Fix Doesn't Work
```python
# This comparison ALWAYS fails for bulk edits:
original_data = st.session_state.get(editor_key)
if original_data is not None and not original_data.empty and len(original_data) == len(edited_data):
```

When this fails, it jumps to "process all rows" which creates duplicates.

## The Right Solution

### Principle: Never INSERT existing Transaction IDs
1. Remove complex session state comparisons
2. For every row with a Transaction ID: UPDATE only
3. Only INSERT if Transaction ID is genuinely missing/new
4. Make Transaction ID the single source of truth

### Implementation Needed
1. Simplify the save logic to remove session state dependency
2. Always check database for Transaction ID existence
3. Bulk operations should be UPDATE-only by default
4. Add explicit "Add New Row" functionality separate from edit