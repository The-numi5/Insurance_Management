import tkinter as tk
from tkinter import ttk, messagebox
from database.user_queries import get_all_users
from database.policy_queries import get_all_policies, add_policy
from database.claim_queries import get_all_claims


def open_admin_dashboard(admin_id):

    # Helper Functions

    def clear_table():
        for row in tree.get_children():
            tree.delete(row)

    def show_users():
        clear_table()
        tree["columns"] = ("ID", "Username", "Role")
        tree["show"] = "headings"

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)

        users = get_all_users()
        for user in users:
            tree.insert("", "end", values=user)

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

    def show_claims():
        clear_table()
        tree["columns"] = ("Claim ID", "Username", "Policy", "Amount", "Status")
        tree["show"] = "headings"

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)

        claims = get_all_claims()
        for claim in claims:
            tree.insert("", "end", values=claim)
            
    def open_add_policy_window():
        add_win = tk.Toplevel(root)
        add_win.title("Add Policy")
        add_win.geometry("350x250")
        add_win.configure(bg="#2b2b2b")
        add_win.resizable(False, False)

        tk.Label(add_win, text="Policy Name",
                 bg="#2b2b2b", fg="white").pack(pady=(20, 5))

        name_entry = tk.Entry(add_win, bg="#3c3f41",
                              fg="white", insertbackground="white")
        name_entry.pack(pady=5, ipady=4)

        tk.Label(add_win, text="Base Premium",
                 bg="#2b2b2b", fg="white").pack(pady=(15, 5))

        premium_entry = tk.Entry(add_win, bg="#3c3f41",
                                 fg="white", insertbackground="white")
        premium_entry.pack(pady=5, ipady=4)

        def save_policy():
            name = name_entry.get()
            premium = premium_entry.get()

            if not name or not premium:
                messagebox.showerror("Error", "All fields required!")
                return

            try:
                premium = float(premium)
                add_policy(name, premium)
                messagebox.showinfo("Success", "Policy Added Successfully!")
                add_win.destroy()
                show_policies()  # refresh table
            except ValueError:
                messagebox.showerror("Error", "Premium must be a number!")

        ttk.Button(add_win, text="Save Policy",
                   command=save_policy,
                   style="Sidebar.TButton").pack(pady=20)


    def logout():
        root.destroy()
        from gui.login import start_login
        start_login()


    # Main Window
    

    root = tk.Tk()
    root.title("Admin Dashboard")
    root.geometry("950x550")
    root.configure(bg="#1e1e1e")

    
    # Style Configuration
    

    style = ttk.Style()
    style.theme_use("clam")

    # Treeview Styling
    
    style.configure(
        "Treeview",
        background="#2b2b2b",
        foreground="white",
        fieldbackground="#2b2b2b",
        rowheight=28
    )

    style.configure(
        "Treeview.Heading",
        background="#3c3f41",
        foreground="white",
        font=("Helvetica", 10, "bold")
    )

    style.map("Treeview",
              background=[("selected", "#007acc")])

    # Button Styling
    
    style.configure(
        "Sidebar.TButton",
        background="#3c3f41",
        foreground="white",
        padding=8,
        borderwidth=0
    )

    style.map(
        "Sidebar.TButton",
        background=[("active", "#007acc")],
        foreground=[("active", "white")]
    )

    
    # Sidebar


    sidebar = tk.Frame(root, bg="#2b2b2b", width=220)
    sidebar.pack(side="left", fill="y")

    tk.Label(
        sidebar,
        text="Admin Panel",
        bg="#2b2b2b",
        fg="white",
        font=("Helvetica", 15, "bold")
    ).pack(pady=25)

    ttk.Button(sidebar, text="View Users", command=show_users,
               style="Sidebar.TButton").pack(fill="x", pady=6, padx=15)

    ttk.Button(sidebar, text="View Policies", command=show_policies,
               style="Sidebar.TButton").pack(fill="x", pady=6, padx=15)

    ttk.Button(sidebar, text="View Claims", command=show_claims,
               style="Sidebar.TButton").pack(fill="x", pady=6, padx=15)

    ttk.Button(sidebar, text="Logout", command=logout,
               style="Sidebar.TButton").pack(fill="x", pady=25, padx=15)
    
    ttk.Button(sidebar, text="Add Policy",
           command=open_add_policy_window,
           style="Sidebar.TButton").pack(fill="x", pady=6, padx=15)


    
    # Main Content Area
    

    content = tk.Frame(root, bg="#1e1e1e")
    content.pack(side="right", expand=True, fill="both")

    tree = ttk.Treeview(content)
    tree.pack(expand=True, fill="both", padx=25, pady=25)

    root.mainloop()