# Color Theme Preferences Feature - January 18, 2025

## Summary
Added user-selectable color themes for STMT and VOID transaction highlighting, allowing users to choose between light (powder blue) and dark (high contrast) color schemes.

## Problem
- Users requested the ability to switch between the original powder blue color (#e6f3ff) and the newer dark blue color (#4a90e2) for STMT transactions
- The dark blue was implemented for better visibility in dark mode but some users preferred the original light colors

## Solution
1. Created a user preferences configuration system
2. Added Display Preferences section in Admin Panel → System Tools tab
3. Implemented theme selection with live preview
4. Updated all transaction display functions to respect user preference

## Changes Made

### New Files
- `/config_files/user_preferences.json` - Stores user's color theme preference

### Modified Files
- `commission_app.py`:
  - Updated `style_special_transactions()` function to check user preference
  - Updated `combined_styling()` function in PRL Reports to respect preference
  - Added Display Preferences UI in System Tools tab

### Color Schemes
- **Light Theme**: 
  - STMT: #e6f3ff (powder blue)
  - VOID: #ffe6e6 (light red)
- **Dark Theme**:
  - STMT: #4a90e2 (dark blue with white text)
  - VOID: #e85855 (dark red with white text)

## Usage
1. Go to Admin Panel → System Tools tab
2. Find Display Preferences section
3. Select preferred theme (light or dark)
4. Click "Save Color Theme Preference"

## Technical Notes
- Excel exports maintain light colors for consistency
- Preference persists across sessions
- Theme applies to all dataframe displays that show transactions