import tkinter as tk
import itertools
import secrets
from detect_attempts import detect_login_attempt, check_and_block_ip, check_and_lock_account, get_client_ip, connect_to_db

# Define a sample dictionary for passwords
password_dictionary = [
    "123456", "password", "admin", "qwerty", "letmein",
    "welcome", "123456789", "abc123", "111111", "sunshine"
]
connection = connect_to_db(dsn="localhost:1521/xepdb1", username="YOUR_USER", password="YOUR_PASSWORD")

# Function to simulate a brute force attack
def generate_password_combinations(dictionary, max_length=10):
    """
    Generates password combinations from a dictionary up to a given length.
    """
    for length in range(1, max_length + 1):
        for combination in itertools.product(dictionary, repeat=length):
            yield ''.join(combination)

def brute_force_test(username):
    """
    Simulates a brute force attack using username-password combinations.
    """
    result_text.insert(tk.END, "🔥 Starting brute force simulation...\n\n")
    password_combinations = generate_password_combinations(password_dictionary, max_length=2)

    for password in password_combinations:
        result_text.insert(tk.END, f"💣 Testing Username: {username}, Password: {password}\n")
        result_text.update_idletasks()
        detect_login_attempt(username, password)
        check_and_lock_account(connection, username)

        # Check and block the IP if needed
        check_and_block_ip(connection, get_client_ip())

def start_simulation():
    username = username_entry.get()
    if username:
        result_text.delete(1.0, tk.END)
        brute_force_test(username)
    else:
        result_text.insert(tk.END, "⚠️ Please enter a username.\n")

# Create the main Tkinter window
root = tk.Tk()
root.title("🔥 Brute Force Attack Simulation")
root.geometry("600x400")
root.configure(bg="#2f2f2f")  # Dark grey background

# Username Field
tk.Label(root, text="👤 Username:", bg="#2f2f2f", fg="#ff0000", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
username_entry = tk.Entry(root, width=30, font=("Arial", 12), bg="#3e3e3e", fg="#ffffff", insertbackground='white')
username_entry.grid(row=0, column=1, padx=10, pady=5)

# Start Simulation Button
start_button = tk.Button(
    root,
    text="💣 Start Attack",
    command=start_simulation,
    bg="#8b0000",  # Dark red background
    fg="white",
    font=("Arial", 14, "bold"),
    activebackground="#b22222",  # Firebrick red when clicked
    activeforeground="white"
)
start_button.grid(row=1, column=0, columnspan=2, pady=10)

# Results Text Box
result_text = tk.Text(root, width=70, height=15, font=("Arial", 12), bg="#3e3e3e", fg="#ffffff", insertbackground='white')
result_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
