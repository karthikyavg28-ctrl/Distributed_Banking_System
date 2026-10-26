
from pymongo import MongoClient
from config import BANK_DATABASES

# Store database connections
clients = {}
databases = {}

def connect_banks():
    for bank_name, settings in BANK_DATABASES.items():
        try:
            client = MongoClient(
                settings["uri"],
                serverSelectionTimeoutMS=5000
            )

            # Verify connection
            client.admin.command("ping")

            clients[bank_name] = client
            databases[bank_name] = client[settings["database"]]

            print(f"{bank_name}: Connected successfully")

        except Exception as error:
            print(f"{bank_name}: Connection failed - {error}")

    return databases


def get_database(bank_name):
    return databases.get(bank_name)


def get_account(bank_name, account_id):
    db = get_database(bank_name)

    if db is None:
        raise ConnectionError(f"{bank_name} is not connected")

    return db.accounts.find_one({
        "account_id": account_id
    })


def update_balance(bank_name, account_id, amount):
    db = get_database(bank_name)

    if db is None:
        raise ConnectionError(f"{bank_name} is not connected")

    result = db.accounts.update_one(
        {
            "account_id": account_id,
            "balance": {"$gte": -amount}
        },
        {
            "$inc": {"balance": amount}
        }
    )

    return result.modified_count == 1


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

