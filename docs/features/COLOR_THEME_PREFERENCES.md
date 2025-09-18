# Transaction Color Theme Preferences

## Overview
As of January 2025, the Sales Commission App allows users to customize how STMT (statement) and VOID transactions are displayed throughout the application. Users can choose between a light theme (powder blue) and a dark theme (dark blue) based on their browser mode preference.

## Feature Location
**Admin Panel → System Tools tab → Display Preferences section**

## Available Themes

### Light Theme (Default)
- **STMT Transactions**: Light powder blue background (#e6f3ff)
- **VOID Transactions**: Light red background (#ffe6e6)
- Best for: Users with light mode browsers or who prefer softer colors

### Dark Theme
- **STMT Transactions**: Dark blue background (#4a90e2) with white text
- **VOID Transactions**: Dark red background (#e85855) with white text
- Best for: Users with dark mode browsers or who prefer higher contrast

## How to Change Your Theme

1. Navigate to **Admin Panel** from the main navigation menu
2. Click on the **System Tools** tab
3. Scroll down to the **Display Preferences** section
4. Select your preferred theme:
   - **light** - For powder blue/light red colors
   - **dark** - For dark blue/dark red colors
5. Click **Save Color Theme Preference**
6. The app will refresh and apply your new color theme

## Where Colors Are Applied

The color theme affects transaction displays in the following areas:
- **Dashboard** - Recent Activity section
- **All Policy Transactions** - Main transaction table
- **Search & Filter Results** - Filtered transaction displays
- **Policy Revenue Ledger Reports** - Report previews and detailed transaction views
- **Reconciliation** - Matched and unreconciled transaction tables

## Technical Details

### Configuration Storage
User preferences are stored in `/config_files/user_preferences.json`:
```json
{
    "color_theme": {
        "transaction_colors": "light",
        "description": "Choose between 'light' (powder blue) or 'dark' (dark blue) colors for STMT transactions"
    }
}
```

### Implementation
- The `style_special_transactions()` function checks the user preference before applying colors
- The `combined_styling()` function in Policy Revenue Ledger Reports also respects the preference
- Excel exports maintain the original light blue (#e6f3ff) color regardless of theme selection

### Note on Excel Exports
Excel exports always use the light theme colors to ensure consistent formatting in spreadsheet applications.

## Troubleshooting

If your color preference isn't applying:
1. Ensure you've saved your preference in the Display Preferences section
2. Try refreshing your browser (Ctrl+F5 or Cmd+Shift+R)
3. Check that the `config_files/user_preferences.json` file exists
4. If issues persist, use the "Clear Session State" button in System Tools

## History
- **January 2025**: Feature added to allow users to choose between light (powder blue) and dark (dark blue) themes for STMT/VOID transaction highlighting