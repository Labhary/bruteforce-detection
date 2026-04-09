import oracledb
import socket
from datetime import datetime, timedelta
from db_connection import connect_to_db 

def get_client_ip():
  
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def check_credentials(connection, username, password):

    try:
        cursor = connection.cursor()
        # Query to check if username and password exist in the Account table
        query = "SELECT COUNT(*) FROM Account WHERE username = :username AND password = :password"
        cursor.execute(query, {"username": username, "password": password})
        result = cursor.fetchone()
        return result[0] > 0  # Returns True if count > 0
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Database error: {error.message}")
        return False
    finally:
        cursor.close()

def log_attempt(connection, ip, username, password):

    try:
        cursor = connection.cursor()
        # SQL query to insert the attempt
        sql = """
        INSERT INTO Attempt_Log (ip, username, password, Attempt_time)
        VALUES (:ip, :username, :password, :attempt_time)
        """
        cursor.execute(sql, {
            "ip": ip,
            "username": username,
            "password": password,
            "attempt_time": datetime.now()
        })
        connection.commit()
        print("Invalid login attempt logged successfully.")
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Database error: {error.message}")
    finally:
        cursor.close()

def detect_login_attempt(username, password):
    """
    Detects login attempts, checks credentials, and logs invalid attempts.
    """
    connection = connect_to_db(dsn="localhost:1521/xepdb1", username="YOUR_USER", password="YOUR_PASSWORD")
    if connection is None:
        print("Unable to connect to the database. Exiting.")
        return

    ip = get_client_ip()  # Automatically retrieve the client IP

    if not check_credentials(connection, username, password):
        # Log invalid login attempt
        log_attempt(connection, ip, username, password)
        print(f"Invalid login attempt detected for Username: {username}, IP: {ip}")
    else:
        print("Login successful!\n")

    connection.close()

def check_and_lock_account(connection, username):
    """
    Checks if the user has entered a correct username but incorrect password
    more than 5 times within 2 minutes. Locks the account if the condition is met.
    """
    try:
        cursor = connection.cursor()

        # Query to count failed login attempts within the last 2 minutes for the username
        query = """
        SELECT COUNT(*)
        FROM Attempt_Log
        WHERE username = :username
          AND Attempt_time >= :time_limit
        """
        time_limit = datetime.now() - timedelta(minutes=2)
        cursor.execute(query, {"username": username, "time_limit": time_limit})
        failed_attempts = cursor.fetchone()[0]

        if failed_attempts > 4:
            # Lock the account if there are more than 5 failed attempts
            lock_query = "UPDATE Account SET Locked = 1 WHERE username = :username"
            cursor.execute(lock_query, {"username": username})
            connection.commit()
            print(f"Account for username '{username}' has been locked.")
    except Exception as e:
        print(f"Error checking and locking account: {e}")
    finally:
        cursor.close()


def check_and_block_ip(connection, ip):
 
    try:
        cursor = connection.cursor()

        # Query to count failed login attempts within the last 2 minutes for the IP
        query = """
        SELECT COUNT(*)
        FROM Attempt_Log
        WHERE ip = :ip
          AND Attempt_time >= :time_limit
        """
        time_limit = datetime.now() - timedelta(minutes=2)
        cursor.execute(query, {"ip": ip, "time_limit": time_limit})
        failed_attempts = cursor.fetchone()[0]

        if failed_attempts > 10:
            # Block the IP if there are more than 10 failed attempts
            block_query = "INSERT INTO Blocked_IP (ip) VALUES (:ip)"
            cursor.execute(block_query, {"ip": ip})
            connection.commit()
            print(f"IP '{ip}' has been blocked due to multiple failed login attempts.")
    except Exception as e:
        print(f"Error checking and blocking IP: {e}")
    finally:
        cursor.close()