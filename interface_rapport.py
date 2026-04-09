import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import connect_to_db

# Global connection variable
connection = None  # Declare the global connection object

def fetch_blocked_accounts(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT username, Locked FROM Account WHERE Locked = 1"
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching blocked accounts: {e}")
        return []
    finally:
        cursor.close()

def fetch_failed_attempts(connection):
    try:
        cursor = connection.cursor()
        query = """
        SELECT username, COUNT(*) AS failed_attempts
        FROM Attempt_Log
        GROUP BY username
        ORDER BY failed_attempts DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching failed attempts: {e}")
        return []
    finally:
        cursor.close()

def fetch_blocked_ips(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT ip, blocked_time FROM Blocked_IP"
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching blocked IPs: {e}")
        return []
    finally:
        cursor.close()

def unlock_account(connection, username):
    cursor = None
    try:
        cursor = connection.cursor()
        query = "UPDATE Account SET Locked = 0 WHERE username = :username"
        cursor.execute(query, {"username": username})
        connection.commit()
        messagebox.showinfo("Success", f"Account '{username}' has been unlocked.")
    except Exception as e:
        messagebox.showerror("Error", f"Error unlocking account: {e}")
    finally:
        if cursor:
            cursor.close()

def unblock_ip(connection, ip):
    cursor = None
    try:
        cursor = connection.cursor()
        query = "DELETE FROM Blocked_IP WHERE ip = :ip"
        cursor.execute(query, {"ip": ip})
        connection.commit()
        messagebox.showinfo("Success", f"IP address '{ip}' has been unblocked.")
    except Exception as e:
        messagebox.showerror("Error", f"Error unblocking IP: {e}")
    finally:
        if cursor:
            cursor.close()

def display_reports():
    global connection  # Use the global connection object
    if connection is None:
        connection = connect_to_db(dsn="localhost:1521/xepdb1", username="YOUR_USER", password="YOUR_PASSWORD")
        if connection is None:
            messagebox.showerror("Error", "Database connection failed.")
            return
    
    print("Connection:", connection)  # Debug print to confirm connection object

    report_window = tk.Toplevel(root)
    report_window.title("Reports - Login System")
    report_window.geometry("850x700")
    report_window.configure(bg="#f0f8ff")  # Light blue background

    # Tab control
    tab_control = ttk.Notebook(report_window)

    # Style for Treeview
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
    style.map("Treeview", background=[("selected", "#4682B4")], foreground=[("selected", "white")])  # Blue selection

    # Tab 1: Blocked Accounts
    blocked_accounts_tab = ttk.Frame(tab_control, padding=10)
    tab_control.add(blocked_accounts_tab, text="Blocked Accounts")
    ttk.Label(blocked_accounts_tab, text="Blocked Accounts", font=("Arial", 16), foreground="#2e8b57").pack(pady=5)
    blocked_accounts_tree = ttk.Treeview(blocked_accounts_tab, columns=("Username", "Locked"), show="headings")
    blocked_accounts_tree.heading("Username", text="Username")
    blocked_accounts_tree.heading("Locked", text="Locked")
    for account in fetch_blocked_accounts(connection):
        blocked_accounts_tree.insert("", tk.END, values=account)
    blocked_accounts_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def unlock_selected_account():
        selected_item = blocked_accounts_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an account to unlock.")
            return
        username = blocked_accounts_tree.item(selected_item, "values")[0]
        unlock_account(connection, username)
        blocked_accounts_tree.delete(selected_item)

    unlock_button = tk.Button(
        blocked_accounts_tab, text="Unlock Account", command=unlock_selected_account,
        bg="#4682B4", fg="white", font=("Arial", 12, "bold"), width=20
    )
    unlock_button.pack(pady=10)

    # Tab 2: Failed Attempts
    failed_attempts_tab = ttk.Frame(tab_control, padding=10)
    tab_control.add(failed_attempts_tab, text="Failed Attempts")
    ttk.Label(failed_attempts_tab, text="Failed Login Attempts", font=("Arial", 16), foreground="#2e8b57").pack(pady=5)
    failed_attempts_tree = ttk.Treeview(failed_attempts_tab, columns=("Username", "Failed Attempts"), show="headings")
    failed_attempts_tree.heading("Username", text="Username")
    failed_attempts_tree.heading("Failed Attempts", text="Failed Attempts")
    for attempt in fetch_failed_attempts(connection):
        failed_attempts_tree.insert("", tk.END, values=attempt)
    failed_attempts_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Tab 3: Blocked IPs
    blocked_ips_tab = ttk.Frame(tab_control, padding=10)
    tab_control.add(blocked_ips_tab, text="Blocked IPs")
    ttk.Label(blocked_ips_tab, text="Blocked IPs", font=("Arial", 16), foreground="#2e8b57").pack(pady=5)
    blocked_ips_tree = ttk.Treeview(blocked_ips_tab, columns=("IP", "Blocked Time"), show="headings")
    blocked_ips_tree.heading("IP", text="IP Address")
    blocked_ips_tree.heading("Blocked Time", text="Blocked Time")
    for ip in fetch_blocked_ips(connection):
        blocked_ips_tree.insert("", tk.END, values=ip)
    blocked_ips_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def unblock_selected_ip():
        selected_item = blocked_ips_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an IP to unblock.")
            return
        ip = blocked_ips_tree.item(selected_item, "values")[0]
        unblock_ip(connection, ip)
        blocked_ips_tree.delete(selected_item)

    unblock_button = tk.Button(
        blocked_ips_tab, text="Unblock IP", command=unblock_selected_ip,
        bg="#4682B4", fg="white", font=("Arial", 12, "bold"), width=20
    )
    unblock_button.pack(pady=10)

    tab_control.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Main application window
root = tk.Tk()
root.title("Login Security System")
root.geometry("500x300")
root.configure(bg="#f0f8ff")  # Light blue background

# Title
title_label = tk.Label(root, text="🔐 Login Security System", font=("Arial", 20, "bold"), bg="#f0f8ff", fg="#4682B4")
title_label.pack(pady=20)

# Button to display reports with an emoji
btn_reports = tk.Button(
    root,
    text="🔓 View Reports",  # Added emoji
    command=display_reports,
    width=20,
    height=2,
    bg="#4682B4",  # Steel blue background
    fg="white",
    font=("Arial", 14, "bold"),
    activebackground="#2e8b57",  # Sea green when clicked
    activeforeground="white"
)
btn_reports.pack(pady=50)

# Run the Tkinter event loop
root.mainloop()
