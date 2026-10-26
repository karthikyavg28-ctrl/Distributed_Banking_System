from fault_tolerance.failure_simulator import is_bank_available
from concurrency.locking import acquire_account_lock, release_account_lock
from fault_tolerance.failure_simulator import is_bank_available

from transaction.transaction_log import log_transaction


def prepare_transaction(bank_name, account_id, amount, transaction_id):
    """
    Phase 1: Prepare
    Check whether the bank can participate in the transaction.
    """

    if not is_bank_available(bank_name):
        print(f"{bank_name}: Bank is unavailable. PREPARE FAILED.")
        return False

    from database import get_database

    database = get_database(bank_name)

    database = get_database(bank_name)

    if database is None:
        print(f"{bank_name}: Database unavailable")
        return False

    account = database["accounts"].find_one({
        "account_id": account_id
    })

    if account is None:
        print(f"{bank_name}: Account not found")
        return False

    if account["balance"] < amount:
        print(f"{bank_name}: Insufficient balance")
        return False

    print(f"{bank_name}: PREPARED")
    return True


def commit_transaction(bank_name, account_id, amount, operation):
    """
    Phase 2: Commit
    Apply the transaction to the bank account.
    """

    from database import get_database

    database = get_database(bank_name)

    if database is None:
        return False

    if operation == "DEBIT":
        result = database["accounts"].update_one(
            {
                "account_id": account_id,
                "balance": {"$gte": amount}
            },
            {"$inc": {"balance": -amount}}
        )

    elif operation == "CREDIT":
        result = database["accounts"].update_one(
            {"account_id": account_id},
            {"$inc": {"balance": amount}}
        )

    else:
        return False

    # Debugging output
    print(f"{bank_name}: Matched documents = {result.matched_count}")
    print(f"{bank_name}: Modified documents = {result.modified_count}")

    updated_account = database["accounts"].find_one({
        "account_id": account_id
    })

    if updated_account:
        print(f"{bank_name}: Updated balance = {updated_account['balance']}")
    else:
        print(f"{bank_name}: Account not found after update")

    return result.modified_count == 1



def two_phase_commit(from_bank, from_account, to_bank, to_account, amount):
    from database import get_database
    from transaction.transaction_log import generate_transaction_id

    transaction_id = generate_transaction_id()

    print("\nTransaction ID:", transaction_id)

    # Acquire locks in a consistent order to reduce deadlock risk.
    account_keys = sorted(set([
        (from_bank, from_account),
        (to_bank, to_account)
    ]))

    acquired_locks = []

    try:
        print("\n--- CONCURRENCY CONTROL ---")

        for bank_name, account_id in account_keys:
            lock = acquire_account_lock(bank_name, account_id)
            acquired_locks.append((bank_name, account_id, lock))

        print("\n--- PHASE 1: PREPARE ---")

        sender_ready = prepare_transaction(
            from_bank, from_account, amount, transaction_id
        )

        receiver_ready = prepare_transaction(
            to_bank, to_account, 0, transaction_id
        )

        if not sender_ready or not receiver_ready:
            print("\nTransaction ABORTED")

            for bank_name in set([from_bank, to_bank]):
                database = get_database(bank_name)
                if database is not None:
                    log_transaction(
                        database, transaction_id,
                        f"{from_bank}:{from_account}",
                        f"{to_bank}:{to_account}",
                        amount, "ABORTED"
                    )

            return False

        print("\n--- PHASE 2: COMMIT ---")

        debit_success = commit_transaction(
            from_bank, from_account, amount, "DEBIT"
        )

        if not debit_success:
            print("Debit failed. Transaction requires recovery.")
            return False

        credit_success = commit_transaction(
            to_bank, to_account, amount, "CREDIT"
        )

        if not credit_success:
            print("Credit failed. Transaction requires recovery.")
            return False

        print("\nTransaction COMMITTED successfully!")

        for bank_name in set([from_bank, to_bank]):
            database = get_database(bank_name)
            if database is not None:
                log_transaction(
                    database, transaction_id,
                    f"{from_bank}:{from_account}",
                    f"{to_bank}:{to_account}",
                    amount, "COMMITTED"
                )

        return True

    finally:
        print("\n--- RELEASING ACCOUNT LOCKS ---")

        for bank_name, account_id, lock in reversed(acquired_locks):
            release_account_lock(bank_name, account_id, lock)
