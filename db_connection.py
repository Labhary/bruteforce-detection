import tkinter as tk
import oracledb

# Default DSN
default_dsn = "localhost:1521/xepdb1"

# Function to connect to the database
def connect_to_db(dsn, username, password):
    """Connect to the Oracle database."""
    try:
        connection = oracledb.connect(user=username, password=password, dsn=dsn)
        return connection
    except oracledb.DatabaseError as e:
        error, = e.args
        return f"Connection error: {error.message}"

def attempt_connection():
    """Attempt to connect to the database using provided credentials."""
    username = username_entry.get()
    password = password_entry.get()
    dsn = dsn_entry.get()
    result = connect_to_db(dsn, username, password)
    if isinstance(result, str):  # If an error message is returned
        result_label.config(text=result, fg="red")
    else:
        result_label.config(text="✅ Connection successful!", fg="green")

# Create the main Tkinter window
root = tk.Tk()
root.title("Oracle DB Connection")
root.geometry("500x200")
root.configure(bg="#f0f8ff")  # Light blue background

# Username Field
tk.Label(root, text="👤 Username:", bg="#f0f8ff", fg="#000000", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
username_entry = tk.Entry(root, width=30, font=("Arial", 12))
username_entry.grid(row=0, column=1, padx=10, pady=10)

# Password Field
tk.Label(root, text="🔒 Password:", bg="#f0f8ff", fg="#000000", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
password_entry = tk.Entry(root, show="*", width=30, font=("Arial", 12))
password_entry.grid(row=1, column=1, padx=10, pady=10)

# DSN Field with default value
tk.Label(root, text="🌐 DSN:", bg="#f0f8ff", fg="#000000", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
dsn_entry = tk.Entry(root, width=30, font=("Arial", 12))
dsn_entry.insert(0, default_dsn)
dsn_entry.grid(row=2, column=1, padx=10, pady=10)

# Connect Button
connect_button = tk.Button(
    root,
    text="🔗 Connect",
    command=attempt_connection,
    bg="#4682B4",  # Steel blue background
    fg="white",
    font=("Arial", 14, "bold"),
    activebackground="#2e8b57",  # Sea green when clicked
    activeforeground="white"
)
connect_button.grid(row=3, column=0, columnspan=2, pady=10)

# Result Label
result_label = tk.Label(root, text="", bg="#f0f8ff", font=("Arial", 12))
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# Run the Tkinter event loop
root.mainloop()
