from database import connect_banks

dbs = connect_banks()

accounts = [
    ("Bank_A", "A1001"),
    ("Bank_B", "B1001"),
    ("Bank_C", "C1001")
]

print("\n--- CURRENT ACCOUNT BALANCES ---")

for bank, account_id in accounts:
    account = dbs[bank]["accounts"].find_one(
        {"account_id": account_id}
    )

    if account:
        print(
            bank,
            account_id,
            "Balance:",
            account["balance"]
        )
    else:
        print(bank, account_id, "NOT FOUND")