import tkinter as tk
from tkinter import messagebox
from db_connection import connect_to_db
from detect_attempts import detect_login_attempt, check_credentials, check_and_lock_account, check_and_block_ip, get_client_ip
def handle_login():
    """
    Handles the login attempt by capturing user input and providing detailed feedback.
    """
    username = username_entry.get()
    password = password_entry.get()
    ip = get_client_ip()  # Function to extract user's IP address

    if not username or not password:
        messagebox.showerror("Error", "Both username and password are required.")
        return

    # Connect to the database
    connection = connect_to_db(dsn="localhost:1521/xepdb1", username="YOUR_USER", password="YOUR_PASSWORD")
    if connection is None:
        messagebox.showerror("Error", "Database connection failed. Please try again later.")
        return

    try:
        # Check if IP is blocked
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Blocked_IP WHERE ip = :ip", {"ip": ip})
        result = cursor.fetchone()

        if result and result[0] > 0:
            messagebox.showerror("IP Blocked", "Your IP is blocked. Please contact an administrator.")
            return

        # Check if account is locked
        cursor.execute("SELECT Locked FROM Account WHERE username = :username", {"username": username})
        result = cursor.fetchone()

        if result and result[0] == 1:
            messagebox.showerror("Account Locked", "Your account is locked. Please contact an administrator.")
            return

        # Check if credentials are valid
        if check_credentials(connection, username, password):
            messagebox.showinfo("Success", "Login successful!")
        else:
            # Log invalid login attempt
            detect_login_attempt(username, password)  # Logs the invalid attempt with IP

            # Check and lock the account if needed
            check_and_lock_account(connection, username)

            # Check and block the IP if needed
            check_and_block_ip(connection, ip)

            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    finally:
        connection.close()


root = tk.Tk()
root.title("🔐 Login Attempt Interface")
root.geometry("400x200")
root.configure(bg="#f0f8ff")  # Light blue background

# Username Field
tk.Label(root, text="👤 Username:", bg="#f0f8ff", fg="#000000", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
username_entry = tk.Entry(root, width=30, font=("Arial", 12))
username_entry.grid(row=0, column=1, padx=10, pady=5)

# Password Field
tk.Label(root, text="🔑 Password:", bg="#f0f8ff", fg="#000000", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
password_entry = tk.Entry(root, show="*", width=30, font=("Arial", 12))  # Masked input for password
password_entry.grid(row=1, column=1, padx=10, pady=5)

# Login Button
login_button = tk.Button(
    root,
    text="🔓 Log In",
    command=handle_login,
    bg="#4682B4",  # Steel blue background
    fg="white",
    font=("Arial", 14, "bold"),
    activebackground="#2e8b57",  # Sea green when clicked
    activeforeground="white"
)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

# Run the Tkinter event loop
root.mainloop()
