
from datetime import datetime
import uuid


def generate_transaction_id():
    """Generate a unique transaction ID."""
    return str(uuid.uuid4())


def log_transaction(
    database,
    transaction_id,
    from_account,
    to_account,
    amount,
    status
):
    """
    Store transaction details in MongoDB.
    """

    transaction_data = {
        "transaction_id": transaction_id,
        "from_account": from_account,
        "to_account": to_account,
        "amount": amount,
        "status": status,
        "timestamp": datetime.now()
    }

    try:
        database["transactions"].update_one(
            {"transaction_id": transaction_id},
            {"$set": transaction_data},
            upsert=True
        )

        print(
            f"Transaction logged: {transaction_id} - {status}"
        )

        return True

    except Exception as error:
        print(f"Transaction logging failed: {error}")
        return False
