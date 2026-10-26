from flask import Flask, jsonify, request
from database import connect_banks
from transaction.coordinator import execute_transfer

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)

# Connect to all banks
connect_banks()


@app.route("/")
def home():
    return app.send_static_file("index.html")


@app.route("/api/balances", methods=["GET"])
def get_balances():
    from database import get_database

    balances = []

    for bank_name, account_id in [
        ("Bank_A", "A1001"),
        ("Bank_B", "B1001"),
        ("Bank_C", "C1001")
    ]:
        database = get_database(bank_name)

        if database is not None:
            account = database["accounts"].find_one(
                {"account_id": account_id}
            )

            if account:
                balances.append({
                    "bank": bank_name,
                    "account_id": account_id,
                    "holder": account.get("holder", ""),
                    "balance": account.get("balance", 0)
                })

    return jsonify(balances)

@app.route("/api/transactions", methods=["GET"])
def get_transactions():
    from database import get_database

    transactions = []

    for bank_name in ["Bank_A", "Bank_B", "Bank_C"]:
        database = get_database(bank_name)

        if database is not None:
            records = database["transactions"].find().sort(
                "timestamp", -1
            ).limit(20)

            for record in records:
                transactions.append({
                    "transaction_id": record.get("transaction_id"),
                    "from_account": record.get("from_account"),
                    "to_account": record.get("to_account"),
                    "amount": record.get("amount"),
                    "status": record.get("status"),
                    "timestamp": str(record.get("timestamp", ""))
                })

    return jsonify(transactions)    


@app.route("/api/transfer", methods=["POST"])
def transfer():
    data = request.get_json()

    from_bank = data.get("from_bank")
    from_account = data.get("from_account")
    to_bank = data.get("to_bank")
    to_account = data.get("to_account")
    amount = float(data.get("amount", 0))

    result = execute_transfer(
        from_bank,
        from_account,
        to_bank,
        to_account,
        amount
    )

    return jsonify({
        "success": result
    })


if __name__ == "__main__":
    app.run(debug=True)