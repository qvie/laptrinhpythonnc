import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import csv
import hashlib

# Tạo kết nối đến cơ sở dữ liệu SQLite
def connect_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        student_id TEXT PRIMARY KEY,
                        name TEXT,
                        age INTEGER,
                        major TEXT,
                        username TEXT UNIQUE,
                        password TEXT
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password TEXT
                    )''')
    conn.commit()
    return conn, cursor

# Đăng ký sinh viên
def register_student():
    username = entry_register_username.get()
    password = entry_register_password.get()
    confirm_password = entry_register_confirm_password.get()

    if username == "" or password == "" or confirm_password == "":
        messagebox.showwarning("Input Error", "Please fill all fields")
        return

    if password != confirm_password:
        messagebox.showwarning("Input Error", "Passwords do not match")
        return

    hashed_password = hashlib.md5(password.encode()).hexdigest()

    conn, cursor = connect_db()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")
    conn.close()

# Đăng nhập sinh viên
def login_student():
    username = entry_login_username.get()
    password = entry_login_password.get()

    if username == "" or password == "":
        messagebox.showwarning("Input Error", "Please fill all fields")
        return

    hashed_password = hashlib.md5(password.encode()).hexdigest()

    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Success", "Login successful")
        root.deiconify()  # Show main window
        login_window.withdraw()  # Hide login window
        view_students()
        show_database()  # Show all data after login
    else:
        messagebox.showerror("Error", "Invalid username or password")

# Đăng xuất sinh viên
def logout_student():
    root.withdraw()  # Hide main window
    login_window.deiconify()  # Show login window

# Thêm sinh viên vào cơ sở dữ liệu
def add_student():
    student_id = entry_student_id.get()
    name = entry_name.get()
    age = entry_age.get()
    major = entry_major.get()

    if student_id == "" or name == "" or age == "" or major == "":
        messagebox.showwarning("Input Error", "Please fill all fields")
        return

    conn, cursor = connect_db()
    try:
        cursor.execute("INSERT INTO students (student_id, name, age, major) VALUES (?, ?, ?, ?)", (student_id, name, age, major))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Student ID already exists")
    conn.close()

    clear_entries()
    view_students()

# Sửa thông tin sinh viên
def edit_student():
    student_id = entry_student_id.get()
    name = entry_name.get()
    age = entry_age.get()
    major = entry_major.get()

    if student_id == "" or name == "" or age == "" or major == "":
        messagebox.showwarning("Input Error", "Please fill all fields")
        return

    conn, cursor = connect_db()
    cursor.execute("UPDATE students SET name=?, age=?, major=? WHERE student_id=?", (name, age, major, student_id))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Student updated successfully")
    clear_entries()
    view_students()

# Xóa sinh viên khỏi cơ sở dữ liệu
def delete_student():
    student_id = entry_student_id.get()

    if student_id == "":
        messagebox.showwarning("Input Error", "Please enter student ID")
        return

    conn, cursor = connect_db()
    cursor.execute("DELETE FROM students WHERE student_id=?", (student_id,))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Student deleted successfully")
    clear_entries()
    view_students()

# Xem tất cả sinh viên
def view_students():
    for row in tree.get_children():
        tree.delete(row)
    
    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)
    conn.close()

# Show toàn bộ cơ sở dữ liệu và lưu trữ vào file CSV
def show_database():
    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()

    # Hiển thị dữ liệu dưới dạng cửa sổ thông báo
    all_data = "\n".join([f"Student ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Major: {row[3]}" for row in rows])
    if all_data:
        messagebox.showinfo("Database Content", all_data)
    else:
        messagebox.showinfo("Database Content", "No data available")

    # Lưu dữ liệu vào file CSV
    with open("students_data.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Student ID", "Name", "Age", "Major"])
        writer.writerows(rows)

# Làm sạch các trường nhập liệu
def clear_entries():
    entry_student_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_major.delete(0, tk.END)

# Cấu hình giao diện đăng nhập
login_window = tk.Tk()
login_window.title("Login")

tk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=5)
entry_login_username = tk.Entry(login_window)
entry_login_username.grid(row=0, column=1, padx=10, pady=5)

tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=5)
entry_login_password = tk.Entry(login_window, show="*")
entry_login_password.grid(row=1, column=1, padx=10, pady=5)

tk.Button(login_window, text="Login", command=login_student).grid(row=2, column=0, columnspan=2, pady=10)

# Cấu hình giao diện đăng ký
tk.Label(login_window, text="Register Username:").grid(row=3, column=0, padx=10, pady=5)
entry_register_username = tk.Entry(login_window)
entry_register_username.grid(row=3, column=1, padx=10, pady=5)

tk.Label(login_window, text="Register Password:").grid(row=4, column=0, padx=10, pady=5)
entry_register_password = tk.Entry(login_window, show="*")
entry_register_password.grid(row=4, column=1, padx=10, pady=5)

tk.Label(login_window, text="Confirm Password:").grid(row=5, column=0, padx=10, pady=5)
entry_register_confirm_password = tk.Entry(login_window, show="*")
entry_register_confirm_password.grid(row=5, column=1, padx=10, pady=5)

tk.Button(login_window, text="Register", command=register_student).grid(row=6, column=0, columnspan=2, pady=10)

# Cấu hình giao diện chính
root = tk.Toplevel(login_window)
root.title("Student Management System")
root.withdraw()

# Các nhãn và trường nhập liệu
tk.Label(root, text="Student ID:").grid(row=0, column=0, padx=10, pady=5)
entry_student_id = tk.Entry(root)
entry_student_id.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Name:").grid(row=1, column=0, padx=10, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Age:").grid(row=2, column=0, padx=10, pady=5)
entry_age = tk.Entry(root)
entry_age.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Major:").grid(row=3, column=0, padx=10, pady=5)
entry_major = tk.Entry(root)
entry_major.grid(row=3, column=1, padx=10, pady=5)

# Các nút chức năng
tk.Button(root, text="Add Student", command=add_student).grid(row=4, column=0, padx=10, pady=10)
tk.Button(root, text="Edit Student", command=edit_student).grid(row=4, column=1, padx=10, pady=10)
tk.Button(root, text="Delete Student", command=delete_student).grid(row=4, column=2, padx=10, pady=10)
tk.Button(root, text="Logout", command=logout_student).grid(row=4, column=3, padx=10, pady=10)

# Bảng hiển thị thông tin sinh viên
columns = ("Student ID", "Name", "Age", "Major")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

for col in columns:
    tree.heading(col, text=col)
    
# Lấy danh sách sinh viên khi bắt đầu
view_students()

login_window.mainloop()
