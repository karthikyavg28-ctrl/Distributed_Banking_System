
BANK_DATABASES = {
    "Bank_A": {
        "uri": "mongodb://localhost:27017/",
        "database": "banking_system"
    },
    "Bank_B": {
        "uri": "mongodb://localhost:27018/",
        "database": "banking_system"
    },
    "Bank_C": {
        "uri": "mongodb://localhost:27019/",
        "database": "banking_system"
    }
}

ACCOUNT_COLLECTION = "accounts"
TRANSACTION_COLLECTION = "transactions"


def test_bank_accounts():
    for bank_name, database in databases.items():
        print(f"\nChecking {bank_name}")

        accounts = list(
            database["accounts"].find(
                {},
                {"_id": 0}
            )
        )

        print("Accounts found:", accounts)

