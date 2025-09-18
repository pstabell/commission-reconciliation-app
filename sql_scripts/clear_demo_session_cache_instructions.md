# Clearing Session Cache for Demo User

If the demo user is not seeing the updated carriers and MGAs after running the fix script, they need to clear their session cache. Here are the options:

## Option 1: Logout and Login Again
1. Click the logout button
2. Login again with the demo credentials
3. This will create a fresh session with the updated data

## Option 2: Clear Browser Cache
1. In Chrome: Ctrl+Shift+Delete (Windows) or Cmd+Shift+Delete (Mac)
2. Select "Cached images and files"
3. Click "Clear data"
4. Refresh the page

## Option 3: Force Refresh in App
If the app has a refresh button in the Commission Structure section, use it to reload the carriers and MGAs data.

## Technical Details
The app caches data in two places:
1. `st.session_state.carriers_data` - List of all carriers for the user
2. `st.session_state.mgas_data` - List of all MGAs for the user
3. `st.session_state[f'mgas_for_carrier_{carrier_id}']` - MGAs associated with specific carriers

When you logout and login, these session state variables are cleared and reloaded from the database.