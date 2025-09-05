# Schema Migration to Supabase - Troubleshooting Guide

## Purpose
This document details our journey migrating the commission tracker database schema to a new Supabase project for SaaS development. The goal was to create an identical database structure in a new Supabase instance while keeping the original personal app untouched.

## Initial Setup
- **Original Database**: Working Supabase instance (project: ddiahkzvmymacejqlnvc)
- **New Database**: Fresh Supabase project (project: msvlbovpctnmwbdztqiu)
- **Schema File**: `schema.sql` containing complete database structure

## Failed Attempts

### 1. Direct psql Connection
**What we tried:**
```bash
psql -h "db.msvlbovpctnmwbdztqiu.supabase.co" -p 6543 -U "postgres.msvlbovpctnmwbdztqiu" -d "postgres" -f schema.sql
```

**Why it failed:**
- DNS resolution errors: "could not translate host name"
- Incorrect connection format for Supabase
- Wrong port number (tried 6543 instead of 5432)
- Incorrect username format

### 2. AWS Pooler Connection
**What we tried:**
```bash
psql -h aws-0-us-east-1.pooler.supabase.com -p 5432 -U postgres.msvlbovpctnmwbdztqiu -d postgres -f schema.sql
```

**Why it failed:**
- "Tenant or user not found" error
- Wrong pooler hostname (each Supabase project has unique pooler URLs)

### 3. Connection String Approach
**What we tried:**
```bash
psql "postgresql://postgres:PASSWORD@db.msvlbovpctnmwbdztqiu.supabase.co:5432/postgres" -f schema.sql
```

**Why it failed:**
- Persistent DNS resolution issues
- PowerShell formatting issues with quotes

### 4. Supabase CLI Migration
**What we tried:**
```bash
npx supabase db push --db-url "postgresql://..." --file schema.sql
```

**Why it failed:**
- CLI doesn't support `--file` flag
- Schema had function/constraint ordering issues
- Function `validate_transaction_id_format` was used before being defined

### 5. SQL Editor Issues
**Initial problem:**
- SQL Editor showed "snippet with ID not found" errors
- Couldn't execute any queries
- Required time for project initialization

## Successful Solution

### Step 1: Fix Function Order
Created `reorganize_schema.py` to reorder SQL statements:
1. Extensions
2. Sequences
3. **Functions** (moved before constraints)
4. Tables
5. Indexes
6. Constraints
7. Triggers
8. RLS policies

### Step 2: Manual Schema Cleanup
Created `clean_schema.sql` with:
- Complete function definitions
- Proper table creation order
- Foreign keys added after all tables exist
- Check constraints using functions placed after function definitions

### Step 3: SQL Editor Migration
1. Waited for Supabase project to fully initialize
2. Accessed SQL Editor (not Database section)
3. Created new query
4. Pasted entire `clean_schema.sql` contents
5. Executed successfully

## Key Learnings

1. **Function Dependencies**: PostgreSQL requires functions to exist before they're referenced in constraints
2. **Supabase Connection Strings**: Each project has unique connection details found in Settings > Database
3. **Project Initialization**: New Supabase projects need time to fully initialize before SQL Editor works
4. **Schema Organization**: Proper ordering is crucial:
   - Create referenced tables before dependent tables
   - Define functions before using them in constraints
   - Add foreign keys after all tables exist

## Files Created During Migration
- `reorganize_schema.py` - Python script to reorder schema sections
- `clean_schema.sql` - Properly ordered schema for successful import
- Various migration files in `supabase/migrations/` (can be deleted if not using CLI)

## Final Result
Successfully migrated all 11 tables with:
- All constraints and relationships intact
- All functions and triggers working
- RLS policies properly configured
- Identical structure to original database

This approach ensures we can maintain our personal app while developing the SaaS version on a separate, identical database.