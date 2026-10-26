
from transaction.two_phase_commit import two_phase_commit


def execute_transfer(
    from_bank,
    from_account,
    to_bank,
    to_account,
    amount
):
    print("\n================================")
    print(" DISTRIBUTED BANKING SYSTEM")
    print("================================")

    if amount <= 0:
        print("Invalid transaction amount")
        return False

    if from_bank == to_bank and from_account == to_account:
        print("Sender and receiver cannot be the same account")
        return False

    print(f"From Bank : {from_bank}")
    print(f"To Bank   : {to_bank}")
    print(f"Amount    : {amount}")

    result = two_phase_commit(
        from_bank,
        from_account,
        to_bank,
        to_account,
        amount
    )

    if result:
        print("\nFINAL STATUS: SUCCESS")
    else:
        print("\nFINAL STATUS: FAILED")

    return result
