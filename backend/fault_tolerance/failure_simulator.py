
# Store simulated bank availability
bank_availability = {
    "Bank_A": True,
    "Bank_B": True,
    "Bank_C": True
}


def simulate_bank_failure(bank_name):
    """Mark a bank as unavailable."""

    if bank_name not in bank_availability:
        print(f"Unknown bank: {bank_name}")
        return False

    bank_availability[bank_name] = False

    print("\n--- FAILURE SIMULATION ---")
    print(f"{bank_name}: Bank marked as UNAVAILABLE")

    return True


def simulate_bank_recovery(bank_name):
    """Mark a bank as available again."""

    if bank_name not in bank_availability:
        print(f"Unknown bank: {bank_name}")
        return False

    bank_availability[bank_name] = True

    print("\n--- BANK RECOVERY ---")
    print(f"{bank_name}: Bank marked as AVAILABLE")

    return True


def is_bank_available(bank_name):
    """Check simulated bank availability."""

    return bank_availability.get(bank_name, False)


if __name__ == "__main__":
    simulate_bank_failure("Bank_B")
    print("Bank available:", is_bank_available("Bank_B"))

    simulate_bank_recovery("Bank_B")
    print("Bank available:", is_bank_available("Bank_B"))
