-- IMPORT DATA FOR DEMO ACCOUNT
-- Generated from private database on 2025-09-18 08:45:53.340189
-- Run this in Supabase SQL Editor

-- Step 1: Delete existing demo data
DELETE FROM commission_rules WHERE user_email = 'Demo@AgentCommissionTracker.com';
DELETE FROM carrier_mga_relationships WHERE user_email = 'Demo@AgentCommissionTracker.com';
DELETE FROM mgas WHERE user_email = 'Demo@AgentCommissionTracker.com';
DELETE FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- Step 2: Insert carriers
