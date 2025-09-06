## Policy Term Transaction Rules

- Transactions can only exist in ONE policy term to avoid duplication
- A transaction is unique and cannot physically exist in two policy terms
- Transactions falling on an X-DATE should go on the renewing policy term (Policy term 2)
- ALL transactions with an effective date within a policy term must follow consistent rules
- Master Policy Term Rules are designed to be unbreakable

## Recent Updates (v4.1.0 - January 6, 2025)

1. **Configurable Default Agent Commission Rates**:
   - Added "Default Agent Rates" tab in Admin Panel
   - Users can now modify default new business (50%) and renewal (25%) rates
   - Rates stored in config_files/default_agent_commission_rates.json
   - Add New Policy form loads rates from config instead of hardcoding

2. **Mobile Sidebar Fix**: 
   - Disabled all custom CSS to allow Streamlit's native mobile behavior
   - Mobile users can now properly collapse/expand sidebar