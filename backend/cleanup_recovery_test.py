from database import connect_banks

dbs = connect_banks()

result = dbs["Bank_A"]["transactions"].update_one(
    {
        "transaction_id": "RECOVERY_DEMO_002",
        "status": "PREPARED"
    },
    {
        "$set": {
            "status": "ABORTED",
            "recovery_reason": "Recovery demonstration completed"
        }
    }
)

print("Updated records:", result.modified_count)