import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database setup
def connect_db():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE NOT NULL,
            course TEXT NOT NULL,
            marks INTEGER,
            attendance INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Add Student
def add_student():
    if name_var.get() == "" or roll_var.get() == "" or course_var.get() == "":
        messagebox.showerror("Error", "All fields are required")
        return
    try:
        conn = sqlite3.connect('students.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO student (name, roll_no, course, marks, attendance) VALUES (?, ?, ?, ?, ?)", (
            name_var.get(),
            roll_var.get(),
            course_var.get(),
            int(marks_var.get() or 0),
            int(attendance_var.get() or 0)
        ))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student added successfully!")
        clear_fields()
        view_students()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll number must be unique")

# View Students
def view_students():
    for row in student_table.get_children():
        student_table.delete(row)
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    for row in rows:
        student_table.insert('', tk.END, values=row)
    conn.close()

# Clear Input Fields
def clear_fields():
    name_var.set("")
    roll_var.set("")
    course_var.set("")
    marks_var.set("")
    attendance_var.set("")

# Get Data from selected row
def get_data(event):
    selected_row = student_table.focus()
    data = student_table.item(selected_row)
    row = data['values']
    if row:
        name_var.set(row[1])
        roll_var.set(row[2])
        course_var.set(row[3])
        marks_var.set(row[4])
        attendance_var.set(row[5])

# Update Student
def update_student():
    if name_var.get() == "" or roll_var.get() == "" or course_var.get() == "":
        messagebox.showerror("Error", "All fields are required")
        return
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("UPDATE student SET name=?, course=?, marks=?, attendance=? WHERE roll_no=?", (
        name_var.get(),
        course_var.get(),
        int(marks_var.get() or 0),
        int(attendance_var.get() or 0),
        roll_var.get()
    ))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student updated successfully!")
    clear_fields()
    view_students()

# Delete Student
def delete_student():
    if roll_var.get() == "":
        messagebox.showerror("Error", "Please enter Roll No. to delete")
        return
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM student WHERE roll_no=?", (roll_var.get(),))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student deleted successfully!")
    clear_fields()
    view_students()

# Initialize window
root = tk.Tk()
root.title("Student Management System")
root.geometry("800x500")

# Variables
name_var = tk.StringVar()
roll_var = tk.StringVar()
course_var = tk.StringVar()
marks_var = tk.StringVar()
attendance_var = tk.StringVar()

# Title
title = tk.Label(root, text="Student Management System", font=("Arial", 20, "bold"), bg="lightblue", fg="black")
title.pack(side=tk.TOP, fill=tk.X)

# Input Frame
input_frame = tk.Frame(root, bd=4, relief=tk.RIDGE, bg="white")
input_frame.place(x=20, y=60, width=350, height=400)

lbl_name = tk.Label(input_frame, text="Name", bg="white", fg="black", font=("Arial", 12))
lbl_name.grid(row=0, column=0, pady=10, padx=10, sticky="w")
txt_name = tk.Entry(input_frame, textvariable=name_var, font=("Arial", 12), bd=2, relief=tk.GROOVE)
txt_name.grid(row=0, column=1, pady=10, padx=10, sticky="w")

lbl_roll = tk.Label(input_frame, text="Roll No", bg="white", fg="black", font=("Arial", 12))
lbl_roll.grid(row=1, column=0, pady=10, padx=10, sticky="w")
txt_roll = tk.Entry(input_frame, textvariable=roll_var, font=("Arial", 12), bd=2, relief=tk.GROOVE)
txt_roll.grid(row=1, column=1, pady=10, padx=10, sticky="w")

lbl_course = tk.Label(input_frame, text="Course", bg="white", fg="black", font=("Arial", 12))
lbl_course.grid(row=2, column=0, pady=10, padx=10, sticky="w")
txt_course = tk.Entry(input_frame, textvariable=course_var, font=("Arial", 12), bd=2, relief=tk.GROOVE)
txt_course.grid(row=2, column=1, pady=10, padx=10, sticky="w")

lbl_marks = tk.Label(input_frame, text="Marks", bg="white", fg="black", font=("Arial", 12))
lbl_marks.grid(row=3, column=0, pady=10, padx=10, sticky="w")
txt_marks = tk.Entry(input_frame, textvariable=marks_var, font=("Arial", 12), bd=2, relief=tk.GROOVE)
txt_marks.grid(row=3, column=1, pady=10, padx=10, sticky="w")

lbl_attendance = tk.Label(input_frame, text="Attendance %", bg="white", fg="black", font=("Arial", 12))
lbl_attendance.grid(row=4, column=0, pady=10, padx=10, sticky="w")
txt_attendance = tk.Entry(input_frame, textvariable=attendance_var, font=("Arial", 12), bd=2, relief=tk.GROOVE)
txt_attendance.grid(row=4, column=1, pady=10, padx=10, sticky="w")

# Button Frame
btn_frame = tk.Frame(input_frame, bg="white")
btn_frame.place(x=10, y=300, width=320)

add_btn = tk.Button(btn_frame, text="Add", width=7, command=add_student)
add_btn.grid(row=0, column=0, padx=5, pady=5)

update_btn = tk.Button(btn_frame, text="Update", width=7, command=update_student)
update_btn.grid(row=0, column=1, padx=5, pady=5)

delete_btn = tk.Button(btn_frame, text="Delete", width=7, command=delete_student)
delete_btn.grid(row=0, column=2, padx=5, pady=5)

clear_btn = tk.Button(btn_frame, text="Clear", width=7, command=clear_fields)
clear_btn.grid(row=0, column=3, padx=5, pady=5)

# Display Frame
display_frame = tk.Frame(root, bd=4, relief=tk.RIDGE, bg="white")
display_frame.place(x=400, y=60, width=380, height=400)

scroll_y = tk.Scrollbar(display_frame, orient=tk.VERTICAL)
student_table = ttk.Treeview(display_frame, columns=("id", "name", "roll", "course", "marks", "attendance"), yscrollcommand=scroll_y.set)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
scroll_y.config(command=student_table.yview)

student_table.heading("id", text="ID")
student_table.heading("name", text="Name")
student_table.heading("roll", text="Roll No")
student_table.heading("course", text="Course")
student_table.heading("marks", text="Marks")
student_table.heading("attendance", text="Attendance %")
student_table['show'] = 'headings'

student_table.column("id", width=30)
student_table.column("name", width=100)
student_table.column("roll", width=70)
student_table.column("course", width=80)
student_table.column("marks", width=50)
student_table.column("attendance", width=80)

student_table.pack(fill=tk.BOTH, expand=1)
student_table.bind("<ButtonRelease-1>", get_data)

# Initialize database and view data
connect_db()
view_students()

root.mainloop()
