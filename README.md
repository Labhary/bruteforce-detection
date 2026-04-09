# Brute Force Attack Detection System

A security system that detects and blocks brute force login attacks in real time, backed by an Oracle Database. Includes a login interface, an admin report dashboard, and a brute force attack simulator for testing the detection logic.

---

## What it does

- Logs every failed login attempt (username, password, IP, timestamp) into an Oracle database
- Automatically **locks an account** after more than 5 failed attempts within 2 minutes
- Automatically **blocks an IP address** after more than 10 failed attempts within 2 minutes
- Admin dashboard to view blocked accounts, failed attempts per user, and blocked IPs — with the ability to unlock/unblock directly from the UI
- Brute force simulator to test the detection system using a password dictionary

---

## Project structure

```
BFDetection/
├── db_connection.py        # Oracle DB connection handler
├── detect_attempts.py      # Core detection logic (logging, locking, blocking)
├── interface.py       # Login interface (simulates a real login form)
├── interface_rapport.py    # Admin dashboard (reports, unlock accounts, unblock IPs)
├── main.py                 # Brute force attack simulator (for testing only)
└── README.md
```

---

## How it works

### 1. Database (Oracle 21c XE)

Three tables are used:

**Account** — stores user credentials
```sql
CREATE TABLE Account (
    username VARCHAR2(50) PRIMARY KEY,
    password VARCHAR2(50),
    Locked   NUMBER(1) DEFAULT 0
);
```

**Attempt_Log** — logs every failed login attempt
```sql
CREATE TABLE Attempt_Log (
    id           NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ip           VARCHAR2(50),
    username     VARCHAR2(50),
    password     VARCHAR2(50),
    Attempt_time TIMESTAMP
);
```

**Blocked_IP** — stores blocked IP addresses
```sql
CREATE TABLE Blocked_IP (
    ip           VARCHAR2(50) PRIMARY KEY,
    blocked_time TIMESTAMP DEFAULT SYSTIMESTAMP
);
```

### 2. Detection Logic (`detect_attempts.py`)

- `check_credentials()` — verifies username/password against the Account table
- `log_attempt()` — inserts a failed attempt record into Attempt_Log
- `check_and_lock_account()` — locks the account if more than 5 failed attempts in 2 minutes
- `check_and_block_ip()` — blocks the IP if more than 10 failed attempts in 2 minutes
- `get_client_ip()` — retrieves the machine's local IP address

### 3. Login Interface (`interface.py`)

A Tkinter form that:
- Checks if the IP is blocked before allowing any attempt
- Checks if the account is locked
- Verifies credentials and triggers detection logic on failure

### 4. Admin Dashboard (`interface_rapport.py`)

A tabbed Tkinter window showing:
- **Blocked Accounts** — with an Unlock button
- **Failed Attempts** — ranked by number of failures per username
- **Blocked IPs** — with an Unblock button

### 5. Brute Force Simulator (`main.py`)

Tests the system by generating password combinations from a dictionary and firing login attempts, triggering the account lock and IP block mechanisms automatically.

---

## Requirements

```
Python 3.x
oracledb
tkinter (built-in)
Oracle Database 21c Express Edition
```

Install Python dependency:
```bash
pip install oracledb
```

---

## Setup

**1. Create the database tables** using the SQL statements above in Oracle SQL Developer or SQL*Plus.

**2. Configure your database credentials.**

The connection details are currently hardcoded in the files. Before running, update the DSN, username, and password in each file to match your Oracle setup:
```python
connection = connect_to_db(dsn="localhost:1521/xepdb1", username="YOUR_USER", password="YOUR_PASSWORD")
```

> ⚠️ Never commit real credentials to GitHub. Consider moving them to a `.env` file and loading with `python-dotenv`.

**3. Run the login interface:**
```bash
python interface.py
```

**4. Run the admin dashboard:**
```bash
python interface_rapport.py
```

**5. Run the brute force simulator (for testing only):**
```bash
python main.py
```

---

## Notes

- The system uses **parameterized queries** throughout, which prevents SQL injection
- Account locking and IP blocking use a **2-minute sliding window** — the time window can be adjusted in `detect_attempts.py`
- This project is a **demonstration/educational system** — in production, passwords should be hashed (e.g. bcrypt), not stored in plaintext
