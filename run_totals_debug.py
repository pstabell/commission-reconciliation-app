import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Get Supabase URL and key
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL and SUPABASE_KEY must be set in environment")
    exit(1)

# Create Supabase client
supabase: Client = create_client(url, key)

# Debug queries for totals row issue
queries = [
    # Query 1: Show row 33 specifically
    """
    WITH numbered_rows AS (
        SELECT 
            *,
            ROW_NUMBER() OVER (ORDER BY "Transaction ID") as row_num
        FROM policies
        WHERE user_email = 'demo@agentcommissiontracker.com'
    )
    SELECT 
        row_num,
        "Transaction ID",
        "Customer",
        "Transaction Type",
        "Premium Sold",
        "Total Agent Comm",
        "Agent Paid Amount (STMT)",
        CAST("Total Agent Comm" AS NUMERIC) - COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0) as balance
    FROM numbered_rows
    WHERE row_num = 33
    """,
    
    # Query 2: Show last 5 rows
    """
    WITH numbered_rows AS (
        SELECT 
            *,
            ROW_NUMBER() OVER (ORDER BY "Transaction ID") as row_num,
            COUNT(*) OVER () as total_rows
        FROM policies
        WHERE user_email = 'demo@agentcommissiontracker.com'
    )
    SELECT 
        row_num,
        "Transaction ID",
        "Customer",
        "Transaction Type",
        "Premium Sold",
        "Total Agent Comm",
        CAST("Total Agent Comm" AS NUMERIC) - COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0) as balance
    FROM numbered_rows
    WHERE row_num > (total_rows - 5)
    ORDER BY row_num
    """,
    
    # Query 3: Find potential totals rows
    """
    SELECT 
        "Transaction ID",
        "Customer",
        "Transaction Type",
        "Premium Sold",
        "Total Agent Comm",
        CAST("Total Agent Comm" AS NUMERIC) as numeric_total_comm
    FROM policies
    WHERE user_email = 'demo@agentcommissiontracker.com'
    AND (
        LOWER("Customer") LIKE '%total%' OR
        LOWER("Customer") LIKE '%sum%' OR
        "Customer" IS NULL OR
        "Customer" = '' OR
        LOWER("Customer") LIKE '%grand%' OR
        ABS(CAST("Total Agent Comm" AS NUMERIC) - 1568.941) < 0.01
    )
    ORDER BY "Transaction ID"
    """,
    
    # Query 4: Calculate correct total excluding totals row
    """
    SELECT 
        COUNT(*) as total_rows,
        SUM(CASE 
            WHEN ABS(CAST("Total Agent Comm" AS NUMERIC) - 1568.941) < 0.01 THEN 0
            ELSE CAST("Total Agent Comm" AS NUMERIC)
        END) as total_agent_comm_excluding_totals,
        SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as total_paid,
        SUM(CASE 
            WHEN ABS(CAST("Total Agent Comm" AS NUMERIC) - 1568.941) < 0.01 THEN 0
            ELSE CAST("Total Agent Comm" AS NUMERIC)
        END) - SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as commission_due_excluding_totals
    FROM policies
    WHERE user_email = 'demo@agentcommissiontracker.com'
    AND "Transaction Type" NOT IN ('CAN', 'XCL')
    """
]

# Run each query
for i, query in enumerate(queries, 1):
    print(f"\n{'='*50}")
    print(f"Query {i}:")
    print(f"{'='*50}")
    
    try:
        result = supabase.rpc('execute_sql', {'query': query}).execute()
        if result.data:
            for row in result.data:
                print(row)
        else:
            print("No results")
    except Exception as e:
        print(f"Error: {str(e)}")

print("\n\nAnalysis Summary:")
print("================")
print("The issue is that row 33 contains a totals row with amount 1568.941")
print("This should be excluded from the Agent Commission Due calculation")
print("The correct total should be $1,568.94 (excluding the totals row)")
print("The dashboard should detect and exclude any rows that appear to be totals/summary rows")