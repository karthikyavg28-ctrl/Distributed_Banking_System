from database import connect_banks
from fault_tolerance.failure_simulator import (
    simulate_bank_failure,
    simulate_bank_recovery
)
from transaction.two_phase_commit import prepare_transaction

# Connect to all banks
connect_banks()

# Simulate Bank_B failure
simulate_bank_failure("Bank_B")

# Try the Prepare phase (should fail)
result = prepare_transaction(
    "Bank_B",
    "B1001",
    0,
    "FAILURE_TEST_001"
)

print("\nTest result:", result)

# Restore Bank_B
simulate_bank_recovery("Bank_B")