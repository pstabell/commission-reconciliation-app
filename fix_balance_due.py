import sqlite3
import re

def clean_currency(value):
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    value = str(value).replace(",", "").replace("$", "").strip()
    try:
        return float(value)
    except ValueError:
        return 0.0

def update_balance_due(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, [Agent Estimated Comm $], [Paid Amount] FROM policies")
    rows = cursor.fetchall()
    for row in rows:
        rowid, agent_comm, paid_amt = row
        agent_comm_clean = clean_currency(agent_comm)
        paid_amt_clean = clean_currency(paid_amt)
        balance_due = agent_comm_clean - paid_amt_clean
        cursor.execute("UPDATE policies SET [BALANCE DUE]=? WHERE rowid=?", (balance_due, rowid))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    db_path = "commissions.db"
    update_balance_due(db_path)
    print("BALANCE DUE updated for all rows.")
