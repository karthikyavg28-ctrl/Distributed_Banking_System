# Distributed Banking Transaction System

## Project Overview

The Distributed Banking Transaction System is a Python-based academic project that demonstrates distributed transaction processing across multiple independent bank databases. The system consists of three banks: Bank A, Bank B, and Bank C. It allows transactions to be processed between bank accounts while demonstrating transaction coordination, concurrency control, transaction logging, and fault-tolerance simulation.

## Objectives

- To implement distributed transaction management across multiple databases.
- To demonstrate the Two-Phase Commit (2PC) protocol.
- To implement concurrency control for simultaneous banking transactions.
- To maintain transaction records and transaction status.
- To simulate bank failures and recovery.
- To identify incomplete transactions.

## Technologies Used

- Python
- MongoDB
- PyMongo
- Docker and Docker Compose
- MongoDB Compass
- HTML
- CSS
- JavaScript
- Visual Studio Code
- Git and GitHub

## System Architecture

The system uses three independent MongoDB database instances:

| Bank | MongoDB Port |
|---|---|
| Bank A | 27017 |
| Bank B | 27018 |
| Bank C | 27019 |

Each bank maintains its own account and transaction collections. The Python backend coordinates transactions between these databases.

## Main Modules

### 1. Distributed Database Management
Three independent MongoDB instances are configured using Docker Compose. Each bank maintains separate banking data.

### 2. Two-Phase Commit Protocol
The system implements two transaction phases:

- **Prepare Phase:** Checks database availability, account existence, and sufficient balance.
- **Commit Phase:** Performs debit and credit operations when participating banks are ready.

### 3. Concurrency Control
Python threading locks are used to control simultaneous access to individual bank accounts and prevent conflicting operations within the application process.

### 4. Transaction Logging
Each transaction is recorded with a unique transaction ID, sender account, receiver account, amount, timestamp, and transaction status.

### 5. Fault-Tolerance Simulation
The system provides functionality to simulate bank unavailability and recovery.

### 6. Transaction Recovery
The recovery module identifies incomplete transactions with statuses such as PREPARED and IN_DOUBT.

### 7. Banking Dashboard
The frontend provides an interface to display bank account balances and transaction history.

## Project Structure

```text
Distributed_Banking_System/
│
├── backend/
│   ├── transaction/
│   │   ├── recovery.py
│   │   ├── transaction_log.py
│   │   └── two_phase_commit.py
│   ├── concurrency/
│   │   └── locking.py
│   ├── fault_tolerance/
│   │   └── failure_simulator.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   └── app.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── tests/
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Installation and Execution

### Prerequisites

- Python 3.x
- Docker Desktop
- MongoDB Compass
- Visual Studio Code
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/karthikyavg28-ctrl/Distributed_Banking_System.git
```

### Step 2: Open the Project Directory

```bash
cd Distributed_Banking_System
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it in Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

```bash
pip install pymongo
```

Install any other packages required by the backend.

### Step 5: Start MongoDB Containers

Run from the project root:

```bash
docker compose up -d
```

Check the containers:

```bash
docker ps
```

### Step 6: Run the Backend

```bash
cd backend
python main.py
```

Follow the terminal instructions to execute transactions.

## Transaction Workflow

1. The user initiates a money transfer.
2. The coordinator generates a unique transaction ID.
3. Account locks are acquired.
4. The Prepare phase checks the participating bank accounts.
5. The Commit phase performs the debit and credit operations if both participants are ready.
6. Transaction details are stored in MongoDB.
7. Account locks are released.
8. The final transaction status is displayed.

## Testing and Evaluation

The project includes testing for:

- Connectivity of all three bank databases.
- Transaction preparation and execution.
- Account-level concurrency using multiple threads.
- Transaction logging.
- Simulated bank failure and recovery.
- Detection of incomplete transactions.

## Limitations

- Python threading locks operate within a single application process.
- Bank failure is simulated using an application-level availability flag.
- The current implementation does not provide full durable atomicity across independent MongoDB instances.
- Recovery detection is implemented, but complete crash-safe recovery requires additional coordinator and participant decision handling.

## Future Enhancements

- Improve durable transaction recovery.
- Handle failures during partial transaction execution.
- Implement distributed concurrency control.
- Enhance the banking dashboard.
- Add user authentication and authorization.
- Perform detailed transaction performance evaluation.

## Conclusion

The Distributed Banking Transaction System demonstrates important concepts of distributed databases and transaction management. It combines multiple MongoDB instances with Two-Phase Commit, concurrency control, transaction logging, and fault-tolerance simulation to demonstrate how distributed banking transactions can be coordinated.

## Author

**Karthik G.**

GitHub: https://github.com/karthikyavg28-ctrl

## Disclaimer

This project is developed for academic and educational purposes only. It is not intended for real banking operations or production financial transactions.