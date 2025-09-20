# Edit Policy Session State Duplication Fix
**Date**: 2025-01-20
**Issue**: Duplication only happens in regular browser mode, not private/incognito

## Problem
The Edit Policy page creates duplicates of the entire dataset when saving edits in regular browser mode. This does NOT happen in private/incognito mode, indicating a session state persistence issue.

## Root Cause
1. The data editor widget maintains stale session state between interactions
2. The comparison between "original" and "edited" data fails because the original reference is stale
3. When comparison fails, the code treats all rows as "new" and tries to insert them
4. This creates duplicates for every row in the dataset

## Why Private Mode Works
- Clean session state every time
- No persistent widget state
- Fresh data references for comparison

## Solution
1. Clear stale widget state before processing saves
2. Add fallback to only process rows with valid transaction IDs if comparison fails
3. Multiple safety checks to prevent mass processing

## Key Insight
Session state persistence in Streamlit can cause data editors to hold stale references. This is why clearing browser cache or using private mode often "fixes" issues.