import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from database.policy_queries import (
    get_all_policies,
    purchase_policy,
    get_user_policies
)

from database.user_queries import get_user_by_id


def open_user_dashboard(user_id):

    user = get_user_by_id(user_id)
    username = user[1] if user else "User"

    # ---------------- Helper Functions ---------------- #

    def clear_table():
        for row in tree.get_children():
            tree.delete(row)

    def show_all_policies():
        clear_table()
        tree["columns"] = ("ID", "Policy Name", "Premium")
        tree["show"] = "headings"

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=200)

        policies = get_all_policies()
        for policy in policies:
            tree.insert("", "end", values=policy)

    def show_my_policies():
        clear_table()
        tree["columns"] = ("Purchase ID", "Policy Name", "Premium", "Start Date")
        tree["show"] = "headings"

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=180)

        policies = get_user_policies(user_id)
        for policy in policies:
            tree.insert("", "end", values=policy)

    def open_purchase_window():
        add_win = tk.Toplevel(root)
        add_win.title("Purchase Policy")
        add_win.geometry("350x250")
        add_win.configure(bg="#2b2b2b")
        add_win.resizable(False, False)

        tk.Label(add_win, text="Policy ID",
                 bg="#2b2b2b", fg="white").pack(pady=(20, 5))

        policy_entry = tk.Entry(add_win, bg="#3c3f41",
                                fg="white", insertbackground="white")
        policy_entry.pack(pady=5, ipady=4)

        def save_purchase():
            policy_id = policy_entry.get()

            if not policy_id:
                messagebox.showerror("Error", "Policy ID required!")
                return

            try:
                today = date.today()
                purchase_policy(user_id, policy_id, today)
                messagebox.showinfo("Success", "Policy Purchased Successfully!")
                add_win.destroy()
                show_my_policies()
            except:
                messagebox.showerror("Error", "Invalid Policy ID!")

        ttk.Button(add_win, text="Purchase",
                   command=save_purchase,
                   style="Sidebar.TButton").pack(pady=20)

    def logout():
        root.destroy()
        from gui.login import start_login
        start_login()

    # ---------------- Main Window ---------------- #

    root = tk.Tk()
    root.title("User Dashboard")
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
             text=f"Welcome, {username}",
             bg="#2b2b2b",
             fg="white",
             font=("Helvetica", 14, "bold")).pack(pady=25)

    ttk.Button(sidebar, text="View All Policies",
               command=show_all_policies,
               style="Sidebar.TButton").pack(fill="x", pady=6, padx=15)

    ttk.Button(sidebar, text="My Policies",
               command=show_my_policies,
               style="Sidebar.TButton").pack(fill="x", pady=6, padx=15)

    ttk.Button(sidebar, text="Purchase Policy",
               command=open_purchase_window,
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
