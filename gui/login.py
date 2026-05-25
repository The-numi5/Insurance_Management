import tkinter as tk
from tkinter import messagebox, ttk
from database.user_queries import verify_user


def start_login():

    def login():
        username = username_entry.get()
        password = password_entry.get()
        role = role_var.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        user = verify_user(username, password, role)

        if user:
            messagebox.showinfo("Success", "Login Successful!")

            user_id, username, role = user
            root.destroy()

            if role == "admin":
                from gui.admin_dash import open_admin_dashboard
                open_admin_dashboard(user_id)

            elif role == "user":
                from gui.user_dash import open_user_dashboard
                open_user_dashboard(user_id)

            elif role == "agent":
                from gui.agent_dash import open_agent_dashboard
                open_agent_dashboard(user_id)

        else:
            messagebox.showerror("Error", "Invalid credentials!")

    # =============================
    # Main Window
    # =============================
    root = tk.Tk()
    root.title("Insurance Management System")
    root.geometry("450x500")
    root.configure(bg="#1e1e1e")
    root.resizable(False, False)

    # =============================
    # Style Configuration
    # =============================
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Login.TButton",
        background="#007acc",
        foreground="white",
        padding=8,
        borderwidth=0
    )

    style.map(
        "Login.TButton",
        background=[("active", "#005f99")],
        foreground=[("active", "white")]
    )

    style.configure(
        "Custom.TMenubutton",
        background="#3c3f41",
        foreground="white"
    )

    # =============================
    # Center Card Frame
    # =============================
    card = tk.Frame(root, bg="#2b2b2b", padx=40, pady=40)
    card.place(relx=0.5, rely=0.5, anchor="center")

    # Title
    tk.Label(
        card,
        text="Insurance Management",
        font=("Helvetica", 16, "bold"),
        bg="#2b2b2b",
        fg="white"
    ).pack(pady=(0, 25))

    # Username
    tk.Label(card, text="Username", bg="#2b2b2b", fg="white").pack(anchor="w")
    username_entry = tk.Entry(
        card,
        bg="#3c3f41",
        fg="white",
        insertbackground="white",
        relief="flat"
    )
    username_entry.pack(fill="x", pady=(0, 15), ipady=6)

    # Password
    tk.Label(card, text="Password", bg="#2b2b2b", fg="white").pack(anchor="w")
    password_entry = tk.Entry(
        card,
        show="*",
        bg="#3c3f41",
        fg="white",
        insertbackground="white",
        relief="flat"
    )
    password_entry.pack(fill="x", pady=(0, 15), ipady=6)

    # Role Dropdown
    tk.Label(card, text="Role", bg="#2b2b2b", fg="white").pack(anchor="w")
    role_var = tk.StringVar(value="user")

    role_menu = ttk.OptionMenu(card, role_var, "user", "admin", "user", "agent")
    role_menu.pack(fill="x", pady=(0, 20))

    # Login Button (Styled)
    ttk.Button(
        card,
        text="Login",
        command=login,
        style="Login.TButton"
    ).pack(fill="x", pady=(10, 0))

    root.mainloop()