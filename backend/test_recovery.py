from database import connect_banks
from transaction.recovery import find_incomplete_transactions

connect_banks()

print("\nChecking incomplete transactions...")

incomplete = find_incomplete_transactions()

print("\nTotal incomplete transactions:", len(incomplete))