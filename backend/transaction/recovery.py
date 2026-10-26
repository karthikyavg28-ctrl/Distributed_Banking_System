
from database import get_database


def find_incomplete_transactions():
    """Find transactions that may require recovery."""

    print("\n--- TRANSACTION RECOVERY CHECK ---")

    incomplete_statuses = ["PREPARED", "IN_DOUBT"]

    found_transactions = []

    for bank_name in ["Bank_A", "Bank_B", "Bank_C"]:
        database = get_database(bank_name)

        if database is None:
            print(f"{bank_name}: Database unavailable")
            continue

        transactions = database["transactions"].find({
            "status": {"$in": incomplete_statuses}
        })

        for transaction in transactions:
            found_transactions.append({
                "bank": bank_name,
                "transaction_id": transaction.get("transaction_id"),
                "status": transaction.get("status"),
                "amount": transaction.get("amount")
            })

            print(
                f"{bank_name}: Transaction "
                f"{transaction.get('transaction_id')} - "
                f"{transaction.get('status')}"
            )

    if not found_transactions:
        print("No incomplete transactions found.")

    return found_transactions
