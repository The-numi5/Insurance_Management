'''import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from database.policy_queries import (
    get_all_policies,
    purchase_policy,
    get_user_policies
)

from database.claim_queries import (
    add_claim,
    get_agent_claims
)


def open_agent_dashboard(agent_id):

    # ---------------- Helper Functions ---------------- #

    def clear_table():
        for row in tree.get_children():
            tree.delete(row)

    def show_policies():
        clear_table()
        tree["columns"] = ("ID", "Policy Name", "Premium")
        tree["show"] = "headings"

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=200)

        policies = get_all_policies()
        for policy in policies:
            tree.insert("", "end", values=policy)

    def show_my_claims():
        clear_table()
        tree["columns"] = ("Claim ID", "Policy ID", "Amount", "Status")
        tree["show"] = "headings"

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=180)

        claims = get_agent_claims(agent_id)
        for claim in claims:
            tree.insert("", "end", values=claim)

    def open_purchase_window():
        add_win = tk.Toplevel(root)
        add_win.title("Purchase Policy")
        add_win.geometry("350x250")
        add_win.configure(bg="#2b2b2b")
        add_win.resizable(False, False)

        tk.Label(add_win, text="User ID",
                 bg="#2b2b2b", fg="white").pack(pady=(20, 5))

        user_entry = tk.Entry(add_win, bg="#3c3f41",
                              fg="white", insertbackground="white")
        user_entry.pack(pady=5, ipady=4)

        tk.Label(add_win, text="Policy ID",
                 bg="#2b2b2b", fg="white").pack(pady=(15, 5))

        policy_entry = tk.Entry(add_win, bg="#3c3f41",
                                fg="white", insertbackground="white")
        policy_entry.pack(pady=5, ipady=4)

        def save_purchase():
            user_id = user_entry.get()
            policy_id = policy_entry.get()

            if not user_id or not policy_id:
                messagebox.showerror("Error", "All fields required!")
                return

            try:
                today = date.today()
                purchase_policy(user_id, policy_id, today)
                messagebox.showinfo("Success", "Policy Purchased!")
                add_win.destroy()
            except:
                messagebox.showerror("Error", "Invalid Data!")

        ttk.Button(add_win, text="Purchase",
                   command=save_purchase,
                   style="Sidebar.TButton").pack(pady=20)

    def open_claim_window():
        claim_win = tk.Toplevel(root)
        claim_win.title("Create Claim")
        claim_win.geometry("350x250")
        claim_win.configure(bg="#2b2b2b")
        claim_win.resizable(False, False)

        tk.Label(claim_win, text="Policy ID",
                 bg="#2b2b2b", fg="white").pack(pady=(20, 5))

        policy_entry = tk.Entry(claim_win, bg="#3c3f41",
                                fg="white", insertbackground="white")
        policy_entry.pack(pady=5, ipady=4)

        tk.Label(claim_win, text="Amount",
                 bg="#2b2b2b", fg="white").pack(pady=(15, 5))

        amount_entry = tk.Entry(claim_win, bg="#3c3f41",
                                fg="white", insertbackground="white")
        amount_entry.pack(pady=5, ipady=4)

        def save_claim():
            policy_id = policy_entry.get()
            amount = amount_entry.get()

            if not policy_id or not amount:
                messagebox.showerror("Error", "All fields required!")
                return

            try:
                amount = float(amount)
                add_claim(agent_id, policy_id, amount)
                messagebox.showinfo("Success", "Claim Submitted!")
                claim_win.destroy()
                show_my_claims()
            except:
                messagebox.showerror("Error", "Invalid Input!")

        ttk.Button(claim_win, text="Submit",
                   command=save_claim,
                   style="Sidebar.TButton").pack(pady=20)

    def logout():
        root.destroy()
        from gui.login import start_login
        start_login()

    # ---------------- Main Window ---------------- #

    root = tk.Tk()
    root.title("Agent Dashboard")
    root.geometry("950x550")
    root.configure(bg="#1e1e1e")

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview",
                    background="#2b2b2b",
                    foreground="white",
                    fieldbackground="#2b2b2b",
                    rowheight=28)

    style.configure("Treeview.Heading",
                    background="#3c3f41",
                    foreground="white",
                    font=("Helvetica", 10, "bold"))

    style.map("Treeview",
              background=[("selected", "#007acc")])

    style.configure("Sidebar.TButton",
                    background="#3c3f41",
                    foreground="white",
                    padding=8)

    # ---------------- Sidebar ---------------- #

    sidebar = tk.Frame(root, bg="#2b2b2b", width=220)
    sidebar.pack(side="left", fill="y")

    tk.Label(sidebar,
             text="Agent Panel",
             bg="#2b2b2b",
             fg="white",
             font=("Helvetica", 15, "bold")).pack(pady=25)

    ttk.Button(sidebar, text="View Policies",
               command=show_policies,
               style="Sidebar.TButton").pack(fill="x", pady=6, padx=15)

    ttk.Button(sidebar, text="Purchase Policy",
               command=open_purchase_window,
               style="Sidebar.TButton").pack(fill="x", pady=6, padx=15)

    ttk.Button(sidebar, text="My Claims",
               command=show_my_claims,
               style="Sidebar.TButton").pack(fill="x", pady=6, padx=15)

    ttk.Button(sidebar, text="Create Claim",
               command=open_claim_window,
               style="Sidebar.TButton").pack(fill="x", pady=6, padx=15)

    ttk.Button(sidebar, text="Logout",
               command=logout,
               style="Sidebar.TButton").pack(fill="x", pady=25, padx=15)

    # ---------------- Main Content ---------------- #

    content = tk.Frame(root, bg="#1e1e1e")
    content.pack(side="right", expand=True, fill="both")

    tree = ttk.Treeview(content)
    tree.pack(expand=True, fill="both", padx=25, pady=25)

    root.mainloop()
'''
import tkinter as tk
from tkinter import ttk, messagebox
from database.user_queries import add_user, get_all_users
from database.policy_queries import (
    get_all_policies,
    purchase_policy,
    get_user_policies
)
from database.user_queries import (
    add_user_by_agent,
    get_users_by_agent
)

from database.connection import get_connection
from datetime import date


def open_agent_dashboard(agent_id):

    # =============================
    # Helper functions
    # =============================

    def clear_table():
        for row in tree.get_children():
            tree.delete(row)
    def show_my_users():
        clear_table()
        tree["columns"] = ("User ID", "Username", "Role")
        tree["show"] = "headings"

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=180)

        users = get_users_by_agent(agent_id)

        for user in users:
            tree.insert("", "end", values=user)


    # =============================
    # ADD USER
    # =============================
    def open_add_user_window():
        win = tk.Toplevel(root)
        win.title("Add User")
        win.geometry("350x250")
        win.configure(bg="#2b2b2b")

        tk.Label(win, text="Username", bg="#2b2b2b", fg="white").pack(pady=10)
        username_entry = tk.Entry(win, bg="#3c3f41", fg="white")
        username_entry.pack(ipady=4)

        tk.Label(win, text="Password", bg="#2b2b2b", fg="white").pack(pady=10)
        password_entry = tk.Entry(win, bg="#3c3f41", fg="white")
        password_entry.pack(ipady=4)

        def save_user():
            username = username_entry.get()
            password = password_entry.get()


            if not username or not password:
                messagebox.showerror("Error", "All fields required!")
                return

            try:
                add_user_by_agent(username, password, "user", agent_id)
                messagebox.showinfo("Success", "User added successfully!")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(win, text="Create User", command=save_user).pack(pady=20)

    # =============================
    # SELL POLICY
    # =============================
    def open_sell_policy_window():
        win = tk.Toplevel(root)
        win.title("Sell Policy")
        win.geometry("400x350")
        win.configure(bg="#2b2b2b")

        users = get_all_users()
        policies = get_all_policies()

        # User dropdown
        tk.Label(win, text="Select User", bg="#2b2b2b", fg="white").pack(pady=10)
        user_var = tk.StringVar()
        user_menu = ttk.Combobox(
            win,
            textvariable=user_var,
            values=[f"{u[0]} - {u[1]}" for u in users],
            state="readonly"
        )
        user_menu.pack(pady=5)

        # Policy dropdown
        tk.Label(win, text="Select Policy", bg="#2b2b2b", fg="white").pack(pady=10)
        policy_var = tk.StringVar()
        policy_menu = ttk.Combobox(
            win,
            textvariable=policy_var,
            values=[f"{p[0]} - {p[1]}" for p in policies],
            state="readonly"
        )
        policy_menu.pack(pady=5)

        def sell_policy():
            if not user_var.get() or not policy_var.get():
                messagebox.showerror("Error", "Select user and policy!")
                return

            user_id = int(user_var.get().split(" - ")[0])
            policy_id = int(policy_var.get().split(" - ")[0])

            try:
                purchase_policy(user_id, policy_id, date.today())
                messagebox.showinfo("Success", "Policy sold successfully!")
                win.destroy()
                show_sold_policies()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(win, text="Sell Policy", command=sell_policy).pack(pady=25)

    # =============================
    # VIEW SOLD POLICIES
    # =============================
    def show_sold_policies():
        clear_table()

        tree["columns"] = ("Purchase ID", "Policy Name", "Premium", "Start Date")
        tree["show"] = "headings"

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)

        # show all users' policies (simple approach)
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                up.purchase_id,
                p.policy_name,
                p.base_premium,
                up.start_date
            FROM USER_POLICIES up
            JOIN POLICIES p ON up.policy_id = p.policy_id
        """)

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            tree.insert("", "end", values=row)

    # =============================
    # LOGOUT
    # =============================
    def logout():
        root.destroy()
        from gui.login import start_login
        start_login()

    # =============================
    # MAIN WINDOW
    # =============================
    root = tk.Tk()
    root.title("Agent Dashboard")
    root.geometry("950x550")
    root.configure(bg="#1e1e1e")

    style = ttk.Style()
    style.theme_use("clam")

    # Sidebar
    sidebar = tk.Frame(root, bg="#2b2b2b", width=220)
    sidebar.pack(side="left", fill="y")

    tk.Label(
        sidebar,
        text="Agent Panel",
        bg="#2b2b2b",
        fg="white",
        font=("Helvetica", 15, "bold")
    ).pack(pady=25)

    ttk.Button(
        sidebar,
        text="My Added Users",
        command=show_my_users
    ).pack(fill="x", pady=6, padx=15)


    ttk.Button(
        sidebar,
        text="Add User",
        command=open_add_user_window
    ).pack(fill="x", pady=6, padx=15)

    ttk.Button(
        sidebar,
        text="Sell Policy",
        command=open_sell_policy_window
    ).pack(fill="x", pady=6, padx=15)

    ttk.Button(
        sidebar,
        text="View Sold Policies",
        command=show_sold_policies
    ).pack(fill="x", pady=6, padx=15)

    ttk.Button(
        sidebar,
        text="Logout",
        command=logout
    ).pack(fill="x", pady=25, padx=15)

    # Content
    content = tk.Frame(root, bg="#1e1e1e")
    content.pack(side="right", expand=True, fill="both")

    tree = ttk.Treeview(content)
    tree.pack(expand=True, fill="both", padx=25, pady=25)

    root.mainloop()