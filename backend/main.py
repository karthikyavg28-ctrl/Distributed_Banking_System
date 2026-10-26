
from database import connect_banks
from transaction.coordinator import execute_transfer
from database import test_bank_accounts


def main():

    print("Connecting to distributed banks...")

    databases = connect_banks()
    test_bank_accounts()

    if len(databases) != 3:
        print("Please ensure all three banks are connected.")
        return

    print("\nAvailable Banks:")
    print("1. Bank_A")
    print("2. Bank_B")
    print("3. Bank_C")

    print("\nStarting Bank Transfer")

    from_bank = input("Enter sender bank: ")
    from_account = input("Enter sender account ID: ")

    to_bank = input("Enter receiver bank: ")
    to_account = input("Enter receiver account ID: ")

    try:
        amount = float(input("Enter transfer amount: "))
    except ValueError:
        print("Invalid amount")
        return

    execute_transfer(
        from_bank,
        from_account,
        to_bank,
        to_account,
        amount
    )


if __name__ == "__main__":
    main()
