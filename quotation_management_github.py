import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# ================= DATABASE CONNECTION =================

# IMPORTANT:
# Replace the following values with your own MySQL/Aiven
# database details before running this project.

DB_CONFIG = {
    "host": "ADD_YOUR_DATABASE_HOST",
    "port": "ADD_YOUR_DATABASE_PORT",
    "user": "ADD_YOUR_DATABASE_USERNAME",
    "password": "ADD_YOUR_DATABASE_PASSWORD",
    "database": "ADD_YOUR_DATABASE_NAME",
    "ssl_disabled": False
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ================= LOGIN =================

def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if username == "" or password == "":
        messagebox.showwarning(
            "Login",
            "Please enter username and password."
        )
        return

    try:
        con = get_connection()
        cur = con.cursor()

        cur.execute(
            "SELECT id FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        result = cur.fetchone()

        cur.close()
        con.close()

        if result:
            login_window.destroy()
            open_dashboard()
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


# ================= DASHBOARD =================

def open_dashboard():

    dashboard = tk.Tk()
    dashboard.title(
        "Small Business Quotation Management System"
    )
    dashboard.geometry("430x750")

    title = tk.Label(
        dashboard,
        text="Small Business Quotation\nManagement System",
        font=("Arial", 18, "bold"),
        pady=20
    )
    title.pack()

    tk.Button(
        dashboard,
        text="Manage Clients",
        width=28,
        height=2,
        command=open_clients
    ).pack(pady=10)

    tk.Button(
        dashboard,
        text="Manage Quotations",
        width=28,
        height=2,
        command=open_projects
    ).pack(pady=10)

    tk.Button(
        dashboard,
        text="Search Quotations",
        width=28,
        height=2,
        command=open_search
    ).pack(pady=10)

    tk.Button(
        dashboard,
        text="Quotation Summary",
        width=28,
        height=2,
        command=open_summary
    ).pack(pady=10)

    tk.Button(
        dashboard,
        text="Exit",
        width=28,
        height=2,
        command=dashboard.destroy
    ).pack(pady=20)

    dashboard.mainloop()


# =========================================================
# CLIENT MANAGEMENT
# =========================================================

def open_clients():

    win = tk.Toplevel()
    win.title("Client Management")
    win.geometry("430x750")

    tk.Label(
        win,
        text="Client Management",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    form = tk.Frame(win)
    form.pack(pady=5)

    tk.Label(
        form,
        text="Client ID"
    ).grid(row=0, column=0, padx=5, pady=5)

    client_id = tk.Entry(form, width=25)
    client_id.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(
        form,
        text="Client Name"
    ).grid(row=1, column=0, padx=5, pady=5)

    client_name = tk.Entry(form, width=25)
    client_name.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(
        form,
        text="Email"
    ).grid(row=2, column=0, padx=5, pady=5)

    email = tk.Entry(form, width=25)
    email.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(
        form,
        text="Phone"
    ).grid(row=3, column=0, padx=5, pady=5)

    phone = tk.Entry(form, width=25)
    phone.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(
        form,
        text="Company"
    ).grid(row=4, column=0, padx=5, pady=5)

    company = tk.Entry(form, width=25)
    company.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(
        form,
        text="Address"
    ).grid(row=5, column=0, padx=5, pady=5)

    address = tk.Entry(form, width=25)
    address.grid(row=5, column=1, padx=5, pady=5)


    def clear():

        client_id.delete(0, tk.END)
        client_name.delete(0, tk.END)
        email.delete(0, tk.END)
        phone.delete(0, tk.END)
        company.delete(0, tk.END)
        address.delete(0, tk.END)


    def add_client():

        if client_name.get().strip() == "":
            messagebox.showwarning(
                "Client",
                "Client name is required."
            )
            return

        try:
            con = get_connection()
            cur = con.cursor()

            sql = """
            INSERT INTO clients
            (client_name, email, phone, company, address)
            VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                client_name.get(),
                email.get(),
                phone.get(),
                company.get(),
                address.get()
            )

            cur.execute(sql, values)
            con.commit()

            cur.close()
            con.close()

            messagebox.showinfo(
                "Success",
                "Client added successfully."
            )

            clear()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )


    def update_client():

        if client_id.get().strip() == "":
            messagebox.showwarning(
                "Client",
                "Enter Client ID."
            )
            return

        try:
            con = get_connection()
            cur = con.cursor()

            sql = """
            UPDATE clients
            SET client_name=%s,
                email=%s,
                phone=%s,
                company=%s,
                address=%s
            WHERE client_id=%s
            """

            values = (
                client_name.get(),
                email.get(),
                phone.get(),
                company.get(),
                address.get(),
                client_id.get()
            )

            cur.execute(sql, values)
            con.commit()

            cur.close()
            con.close()

            messagebox.showinfo(
                "Success",
                "Client updated successfully."
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )


    def delete_client():

        if client_id.get().strip() == "":
            messagebox.showwarning(
                "Client",
                "Enter Client ID."
            )
            return

        answer = messagebox.askyesno(
            "Delete",
            "Are you sure you want to delete this client?"
        )

        if not answer:
            return

        try:
            con = get_connection()
            cur = con.cursor()

            cur.execute(
                "DELETE FROM clients WHERE client_id=%s",
                (client_id.get(),)
            )

            con.commit()

            cur.close()
            con.close()

            messagebox.showinfo(
                "Success",
                "Client deleted successfully."
            )

            clear()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )


    def show_clients():

        try:
            con = get_connection()
            cur = con.cursor()

            cur.execute("""
            SELECT client_id, client_name, email, phone, company
            FROM clients
            ORDER BY client_id
            """)

            rows = cur.fetchall()

            cur.close()
            con.close()

            result_window = tk.Toplevel(win)
            result_window.title("All Clients")
            result_window.geometry("430x600")

            tree = ttk.Treeview(
                result_window,
                columns=(
                    "ID",
                    "Name",
                    "Email",
                    "Phone",
                    "Company"
                ),
                show="headings"
            )

            for col in (
                "ID",
                "Name",
                "Email",
                "Phone",
                "Company"
            ):
                tree.heading(col, text=col)
                tree.column(col, width=100)

            tree.pack(
                fill="both",
                expand=True
            )

            for row in rows:
                tree.insert(
                    "",
                    tk.END,
                    values=row
                )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )


    tk.Button(
        win,
        text="Add Client",
        width=25,
        command=add_client
    ).pack(pady=5)

    tk.Button(
        win,
        text="Update Client",
        width=25,
        command=update_client
    ).pack(pady=5)

    tk.Button(
        win,
        text="Delete Client",
        width=25,
        command=delete_client
    ).pack(pady=5)

    tk.Button(
        win,
        text="Show All Clients",
        width=25,
        command=show_clients
    ).pack(pady=5)

    tk.Button(
        win,
        text="Clear",
        width=25,
        command=clear
    ).pack(pady=5)


# =========================================================
# QUOTATION / PROJECT MANAGEMENT
# =========================================================

def open_projects():

    win = tk.Toplevel()
    win.title("Quotation Management")
    win.geometry("430x800")

    tk.Label(
        win,
        text="Quotation Management",
        font=("Arial", 18, "bold")
    ).pack(pady=12)

    form = tk.Frame(win)
    form.pack()

    tk.Label(
        form,
        text="Project ID"
    ).grid(row=0, column=0, pady=4)

    project_id = tk.Entry(form, width=25)
    project_id.grid(row=0, column=1, pady=4)

    tk.Label(
        form,
        text="Client ID"
    ).grid(row=1, column=0, pady=4)

    client_id = tk.Entry(form, width=25)
    client_id.grid(row=1, column=1, pady=4)

    tk.Label(
        form,
        text="Project Name"
    ).grid(row=2, column=0, pady=4)

    project_name = tk.Entry(form, width=25)
    project_name.grid(row=2, column=1, pady=4)

    tk.Label(
        form,
        text="Category"
    ).grid(row=3, column=0, pady=4)

    category = ttk.Combobox(
        form,
        values=[
            "Web Development",
            "Software",
            "Design",
            "Marketing",
            "Other"
        ],
        width=22
    )
    category.grid(row=3, column=1, pady=4)

    tk.Label(
        form,
        text="Start Date"
    ).grid(row=4, column=0, pady=4)

    start_date = tk.Entry(form, width=25)
    start_date.grid(row=4, column=1, pady=4)

    tk.Label(
        form,
        text="Deadline"
    ).grid(row=5, column=0, pady=4)

    deadline = tk.Entry(form, width=25)
    deadline.grid(row=5, column=1, pady=4)

    tk.Label(
        form,
        text="Budget"
    ).grid(row=6, column=0, pady=4)

    budget = tk.Entry(form, width=25)
    budget.grid(row=6, column=1, pady=4)

    tk.Label(
        form,
        text="Amount Paid"
    ).grid(row=7, column=0, pady=4)

    amount_paid = tk.Entry(form, width=25)
    amount_paid.grid(row=7, column=1, pady=4)

    tk.Label(
        form,
        text="Status"
    ).grid(row=8, column=0, pady=4)

    status = ttk.Combobox(
        form,
        values=[
            "Pending",
            "In Progress",
            "Completed",
            "Cancelled"
        ],
        width=22
    )

    status.set("Pending")
    status.grid(row=8, column=1, pady=4)

    tk.Label(
        form,
        text="Description"
    ).grid(row=9, column=0, pady=4)

    description = tk.Entry(
        form,
        width=25
    )
    description.grid(row=9, column=1, pady=4)


    def clear():

        for entry in [
            project_id,
            client_id,
            project_name,
            start_date,
            deadline,
            budget,
            amount_paid,
            description
        ]:
            entry.delete(0, tk.END)

        category.set("")
        status.set("Pending")


    def add_project():

        if (
            client_id.get().strip() == ""
            or project_name.get().strip() == ""
        ):
            messagebox.showwarning(
                "Quotation",
                "Client ID and Project Name are required."
            )
            return

        try:
            con = get_connection()
            cur = con.cursor()

            sql = """
            INSERT INTO projects
            (
                client_id,
                project_name,
                category,
                start_date,
                deadline,
                budget,
                amount_paid,
                status,
                description
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """

            values = (
                client_id.get(),
                project_name.get(),
                category.get(),
                start_date.get(),
                deadline.get(),
                budget.get() or 0,
                amount_paid.get() or 0,
                status.get(),
                description.get()
            )

            cur.execute(sql, values)
            con.commit()

            cur.close()
            con.close()

            messagebox.showinfo(
                "Success",
                "Quotation created successfully."
            )

            clear()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )


    def update_project():

        if project_id.get().strip() == "":
            messagebox.showwarning(
                "Quotation",
                "Enter Project ID."
            )
            return

        try:
            con = get_connection()
            cur = con.cursor()

            sql = """
            UPDATE projects
            SET client_id=%s,
                project_name=%s,
                category=%s,
                start_date=%s,
                deadline=%s,
                budget=%s,
                amount_paid=%s,
                status=%s,
                description=%s
            WHERE project_id=%s
            """

            values = (
                client_id.get(),
                project_name.get(),
                category.get(),
                start_date.get(),
                deadline.get(),
                budget.get() or 0,
                amount_paid.get() or 0,
                status.get(),
                description.get(),
                project_id.get()
            )

            cur.execute(sql, values)
            con.commit()

            cur.close()
            con.close()

            messagebox.showinfo(
                "Success",
                "Quotation updated successfully."
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )


    def delete_project():

        if project_id.get().strip() == "":
            messagebox.showwarning(
                "Quotation",
                "Enter Project ID."
            )
            return

        if not messagebox.askyesno(
            "Delete",
            "Delete this quotation?"
        ):
            return

        try:
            con = get_connection()
            cur = con.cursor()

            cur.execute(
                "DELETE FROM projects WHERE project_id=%s",
                (project_id.get(),)
            )

            con.commit()

            cur.close()
            con.close()

            messagebox.showinfo(
                "Success",
                "Quotation deleted successfully."
            )

            clear()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )


    def show_projects():

        try:
            con = get_connection()
            cur = con.cursor()

            sql = """
            SELECT
                p.project_id,
                c.client_name,
                p.project_name,
                p.category,
                p.budget,
                p.amount_paid,
                p.status
            FROM projects p
            JOIN clients c
                ON p.client_id = c.client_id
            ORDER BY p.project_id
            """

            cur.execute(sql)
            rows = cur.fetchall()

            cur.close()
            con.close()

            result_window = tk.Toplevel(win)
            result_window.title("All Quotations")
            result_window.geometry("450x600")

            tree = ttk.Treeview(
                result_window,
                columns=(
                    "ID",
                    "Client",
                    "Project",
                    "Category",
                    "Budget",
                    "Paid",
                    "Status"
                ),
                show="headings"
            )

            for col in (
                "ID",
                "Client",
                "Project",
                "Category",
                "Budget",
                "Paid",
                "Status"
            ):
                tree.heading(
                    col,
                    text=col
                )
                tree.column(
                    col,
                    width=90
                )

            tree.pack(
                fill="both",
                expand=True
            )

            for row in rows:
                tree.insert(
                    "",
                    tk.END,
                    values=row
                )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )


    tk.Button(
        win,
        text="Create Quotation",
        width=25,
        command=add_project
    ).pack(pady=4)

    tk.Button(
        win,
        text="Update Quotation",
        width=25,
        command=update_project
    ).pack(pady=4)

    tk.Button(
        win,
        text="Delete Quotation",
        width=25,
        command=delete_project
    ).pack(pady=4)

    tk.Button(
        win,
        text="Show All Quotations",
        width=25,
        command=show_projects
    ).pack(pady=4)

    tk.Button(
        win,
        text="Clear",
        width=25,
        command=clear
    ).pack(pady=4)


# =========================================================
# SEARCH
# =========================================================

def open_search():

    win = tk.Toplevel()
    win.title("Search Quotations")
    win.geometry("430x650")

    tk.Label(
        win,
        text="Search Quotations",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    tk.Label(
        win,
        text="Search by Project Name"
    ).pack()

    search_entry = tk.Entry(
        win,
        width=30
    )
    search_entry.pack(pady=8)


    def search():

        keyword = search_entry.get().strip()

        if keyword == "":
            messagebox.showwarning(
                "Search",
                "Enter a project name."
            )
            return

        try:
            con = get_connection()
            cur = con.cursor()

            sql = """
            SELECT
                p.project_id,
                c.client_name,
                p.project_name,
                p.category,
                p.budget,
                p.status
            FROM projects p
            JOIN clients c
                ON p.client_id = c.client_id
            WHERE p.project_name LIKE %s
            ORDER BY p.project_name
            """

            cur.execute(
                sql,
                ("%" + keyword + "%",)
            )

            rows = cur.fetchall()

            cur.close()
            con.close()

            tree = ttk.Treeview(
                win,
                columns=(
                    "ID",
                    "Client",
                    "Project",
                    "Category",
                    "Budget",
                    "Status"
                ),
                show="headings"
            )

            for col in (
                "ID",
                "Client",
                "Project",
                "Category",
                "Budget",
                "Status"
            ):
                tree.heading(
                    col,
                    text=col
                )
                tree.column(
                    col,
                    width=90
                )

            tree.pack(
                fill="both",
                expand=True,
                pady=15
            )

            for row in rows:
                tree.insert(
                    "",
                    tk.END,
                    values=row
                )

            if not rows:
                messagebox.showinfo(
                    "Search",
                    "No quotation found."
                )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )


    tk.Button(
        win,
        text="Search",
        width=25,
        command=search
    ).pack(pady=8)


# =========================================================
# SUMMARY / GROUP BY
# =========================================================

def open_summary():

    try:
        con = get_connection()
        cur = con.cursor()

        cur.execute("""
        SELECT category, COUNT(*) AS total_projects
        FROM projects
        GROUP BY category
        ORDER BY total_projects DESC
        """)

        rows = cur.fetchall()

        cur.close()
        con.close()

        win = tk.Toplevel()
        win.title("Quotation Summary")
        win.geometry("400x500")

        tk.Label(
            win,
            text="Quotation Summary by Category",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        tree = ttk.Treeview(
            win,
            columns=("Category", "Total"),
            show="headings"
        )

        tree.heading(
            "Category",
            text="Category"
        )

        tree.heading(
            "Total",
            text="Total Quotations"
        )

        tree.column(
            "Category",
            width=200
        )

        tree.column(
            "Total",
            width=150
        )

        tree.pack(
            fill="both",
            expand=True
        )

        for row in rows:
            tree.insert(
                "",
                tk.END,
                values=row
            )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


# ================= LOGIN WINDOW =================

login_window = tk.Tk()

login_window.title("Login")
login_window.geometry("400x450")

tk.Label(
    login_window,
    text="Small Business Quotation",
    font=("Arial", 18, "bold")
).pack(pady=15)

tk.Label(
    login_window,
    text="Management System",
    font=("Arial", 16)
).pack(pady=5)

tk.Label(
    login_window,
    text="Username"
).pack(pady=(30, 5))

username_entry = tk.Entry(
    login_window,
    width=30
)
username_entry.pack()

tk.Label(
    login_window,
    text="Password"
).pack(pady=(15, 5))

password_entry = tk.Entry(
    login_window,
    width=30,
    show="*"
)
password_entry.pack()

tk.Button(
    login_window,
    text="Login",
    width=25,
    height=2,
    command=login
).pack(pady=30)

login_window.mainloop()