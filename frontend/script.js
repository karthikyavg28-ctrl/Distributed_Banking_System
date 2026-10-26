const API_URL = "http://127.0.0.1:5000";


// ===============================
// LOAD BANK BALANCES
// ===============================
async function loadBalances() {
    try {
        const response = await fetch(`${API_URL}/api/balances`);

        if (!response.ok) {
            throw new Error("Failed to load balances");
        }

        const accounts = await response.json();

        const container = document.getElementById("accountCards");
        container.innerHTML = "";

        let total = 0;

        accounts.forEach(account => {
            total += Number(account.balance);

            const card = document.createElement("div");
            card.className = "account-card";

            card.innerHTML = `
                <h3>${account.bank}</h3>

                <p>
                    <strong>Account:</strong>
                    ${account.account_id}
                </p>

                <p>
                    <strong>Holder:</strong>
                    ${account.holder || "Account Holder"}
                </p>

                <p class="balance">
                    ₹${Number(account.balance).toLocaleString("en-IN")}
                </p>
            `;

            container.appendChild(card);
        });

        document.getElementById("totalBalance").textContent =
            `₹${total.toLocaleString("en-IN")}`;

    } catch (error) {
        console.error(error);

        document.getElementById("message").textContent =
            "Unable to connect to banking server.";
    }
}


// ===============================
// LOAD TRANSACTION HISTORY
// ===============================
async function loadTransactions() {
    const container = document.getElementById("transactionHistory");

    try {
        const response = await fetch(`${API_URL}/api/transactions`);

        if (!response.ok) {
            throw new Error("Unable to load transactions");
        }

        const transactions = await response.json();

        // Remove duplicate records
        // because the same transaction may be logged in multiple banks
        const uniqueTransactions = [
            ...new Map(
                transactions.map(tx => [tx.transaction_id, tx])
            ).values()
        ];

        container.innerHTML = "";

        if (uniqueTransactions.length === 0) {
            container.textContent = "No transactions found.";
            return;
        }

        uniqueTransactions.forEach(tx => {

            const item = document.createElement("div");

            item.className = "account-card";

            item.innerHTML = `
                <h3>${tx.status || "UNKNOWN"}</h3>

                <p>
                    Transaction ID:
                    ${tx.transaction_id}
                </p>

                <p>
                    From:
                    ${tx.from_account}
                </p>

                <p>
                    To:
                    ${tx.to_account}
                </p>

                <p>
                    Amount:
                    ₹${Number(tx.amount).toLocaleString("en-IN")}
                </p>

                <p>
                    Date:
                    ${tx.timestamp
                        ? new Date(tx.timestamp).toLocaleString("en-IN")
                        : "N/A"}
                </p>
            `;

            container.appendChild(item);
        });

    } catch (error) {
        console.error(error);

        container.textContent =
            "Unable to load transaction history.";
    }
}


// ===============================
// TRANSFER MONEY
// ===============================
document.getElementById("transferForm").addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();

        const fromBank =
            document.getElementById("fromBank").value;

        const toBank =
            document.getElementById("toBank").value;

        const amount =
            Number(document.getElementById("amount").value);

        const message =
            document.getElementById("message");


        // Check that banks are different
        if (fromBank === toBank) {

            message.textContent =
                "Sender and receiver banks must be different.";

            return;
        }


        // Check amount
        if (amount <= 0) {

            message.textContent =
                "Enter a valid amount.";

            return;
        }


        message.textContent =
            "Processing transaction...";


        try {

            const response = await fetch(
                `${API_URL}/api/transfer`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({

                        from_bank: fromBank,

                        from_account:
                            getAccountId(fromBank),

                        to_bank: toBank,

                        to_account:
                            getAccountId(toBank),

                        amount: amount
                    })
                }
            );


            const result = await response.json();


            if (result.success) {

                message.textContent =
                    "Transaction completed successfully.";

                // Clear amount field
                document.getElementById("amount").value = "";


                // Refresh balances
                await loadBalances();


                // Refresh transaction history
                await loadTransactions();

            } else {

                message.textContent =
                    "Transaction failed.";
            }


        } catch (error) {

            console.error(error);

            message.textContent =
                "Unable to connect to banking server.";
        }
    }
);


// ===============================
// GET ACCOUNT ID
// ===============================
function getAccountId(bank) {

    const accounts = {

        "Bank_A": "A1001",

        "Bank_B": "B1001",

        "Bank_C": "C1001"
    };

    return accounts[bank];
}


// ===============================
// INITIAL PAGE LOAD
// ===============================
loadBalances();

loadTransactions();