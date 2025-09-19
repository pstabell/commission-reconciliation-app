-- Check the most recent reconciliation in commission_payments_simple
SELECT id, policy_number, customer, payment_amount, statement_date, payment_timestamp
FROM commission_payments_simple
ORDER BY payment_timestamp DESC
LIMIT 5;

-- Check if the statement_date is being saved correctly
SELECT statement_date, COUNT(*) as count
FROM commission_payments_simple
GROUP BY statement_date
ORDER BY statement_date DESC;