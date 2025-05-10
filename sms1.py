from customtkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox, filedialog
import db1
import datetime
import os

current_teacher_id = None

def add_student():
    global current_teacher_id
    if not current_teacher_id:
         messagebox.showerror("Error", "No teacher logged in.")
         return

    student_id = idEntry.get()
    name = nameEntry.get()
    phone = phoneEntry.get()
    fees = feesEntry.get()
    course = courseBox.get()
    gender = genderBox.get()

    if student_id == '' or phone == '' or name == '' or fees == '':
        messagebox.showerror('Error', 'All fields are required')
    elif not name.replace(" ", "").isalpha():
        messagebox.showerror('Error', 'Name must contain only letters')
    elif not (phone.isdigit() and len(phone) == 10):
        messagebox.showerror('Error', 'Phone number must contain exactly 10 digits')
    elif not fees.isdigit():
        messagebox.showerror('Error', 'Fees must contain only digits')
    else:
        if db1.insert(student_id, name, phone, fees, course, gender):
             db1.log_operation(current_teacher_id, 'add', student_id)
             show_data()


def update_student():
    global current_teacher_id
    if not current_teacher_id:
         messagebox.showerror("Error", "No teacher logged in.")
         return

    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Please select a record to update")
        return

    student_id = idEntry.get()
    name = nameEntry.get()
    phone = phoneEntry.get()
    fees = feesEntry.get()
    course = courseBox.get()
    gender = genderBox.get()

    if student_id == '' or phone == '' or name == '' or fees == '':
        messagebox.showerror('Error', 'All fields are required')
    elif not name.replace(" ", "").isalpha():
        messagebox.showerror('Error', 'Name must contain only letters')
    elif not (phone.isdigit() and len(phone) == 10):
        messagebox.showerror('Error', 'Phone number must contain exactly 10 digits')
    elif not fees.isdigit():
        messagebox.showerror('Error', 'Fees must contain only digits')
    else:
        if db1.update(student_id, name, phone, fees, course, gender):
            db1.log_operation(current_teacher_id, 'update', student_id)
            show_data()

def delete_student():
    global current_teacher_id
    if not current_teacher_id:
         messagebox.showerror("Error", "No teacher logged in.")
         return

    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Please select a record to delete")
        return

    try:
        id_value = tree.item(selected)["values"][0]
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete student ID {id_value}?")
        if confirm:
            if db1.delete(id_value):
                 db1.log_operation(current_teacher_id, 'delete', id_value)
                 show_data()

    except IndexError:
         messagebox.showerror("Error", "Could not retrieve ID from selected row.")
    except Exception as e:
         messagebox.showerror("Error", f"An unexpected error occurred during deletion: {e}")


def delete_all():
    global current_teacher_id
    if not current_teacher_id:
         messagebox.showerror("Error", "No teacher logged in.")
         return

    confirm = messagebox.askyesno("Confirm Mass Deletion", "Are you sure you want to delete ALL student records? This cannot be undone.")
    if confirm:
        all_students = db1.fetch_all()
        if db1.delete_all():
             db1.log_operation(current_teacher_id, 'delete_all', 'ALL')
             show_data()

             messagebox.showinfo("Success", "All student records have been deleted.")



def show_data():
    db1.show_data(tree)

def search_student():
    query_col = searchBox.get()
    value = searchEntry.get()
    column_map = {"Id": "id", "Name": "name", "Phone": "phone", "Course": "course", "Gender": "gender", "Fees": "fees"}

    if query_col == "Search by" or value == "":
        messagebox.showerror("Error", "Please select a search category and enter a value.")
        return

    db_column = column_map.get(query_col)
    if not db_column:
        messagebox.showerror("Error", "Invalid search category selected.")
        return

    records = db1.fetch_all(column=db_column, value=value)
    tree.delete(*tree.get_children())
    for record in records:
         if len(record) == 6:
            tree.insert("", "end", values=record)
         else:
             print(f"Skipping record from search with unexpected format: {record}")


def select_record(event):
    selected = tree.focus()
    if not selected: return

    try:
        values = tree.item(selected, "values")
        if len(values) == 6:
            for entry in [idEntry, nameEntry, phoneEntry, feesEntry]:
                 entry.delete(0, "end")

            idEntry.insert(0, values[0])
            nameEntry.insert(0, values[1])
            phoneEntry.insert(0, values[2])

            if values[3] in course_option: courseBox.set(values[3])
            else: courseBox.set(course_option[0])

            if values[4] in gender_option: genderBox.set(values[4])
            else: genderBox.set(gender_option[0])

            feesEntry.insert(0, values[5])
        else:
            print(f"Selected row has unexpected data format: {values}")
    except Exception as e:
        print(f"Error selecting record: {e}")

def show_operation_logs():

    logs = db1.fetch_logs()

    if not logs:
        messagebox.showinfo("Operation Logs", "No operation logs found.")
        return

    log_window = CTkToplevel(window)
    log_window.title("Operation Logs")
    log_window.geometry("800x400")
    log_window.grab_set()

    log_frame = CTkFrame(log_window)
    log_frame.pack(expand=True, fill="both", padx=10, pady=10)

    log_scroll_y = CTkScrollbar(log_frame)
    log_scroll_y.pack(side="right", fill="y")
    log_scroll_x = CTkScrollbar(log_frame, orientation="horizontal")
    log_scroll_x.pack(side="bottom", fill="x")

    log_tree = ttk.Treeview(log_frame,
                            columns=('Log ID', 'Teacher ID', 'Operation', 'Student Affected', 'Timestamp'),
                            show='headings',
                            yscrollcommand=log_scroll_y.set,
                            xscrollcommand=log_scroll_x.set)
    log_tree.pack(expand=True, fill="both")

    log_scroll_y.configure(command=log_tree.yview)
    log_scroll_x.configure(command=log_tree.xview)

    log_tree.heading('Log ID', text='Log ID')
    log_tree.column('Log ID', width=60, anchor=CENTER)

    log_tree.heading('Teacher ID', text='Teacher ID')
    log_tree.column('Teacher ID', width=120)

    log_tree.heading('Operation', text='Operation')
    log_tree.column('Operation', width=100, anchor=CENTER)

    log_tree.heading('Student Affected', text='Student Affected')
    log_tree.column('Student Affected', width=120)

    log_tree.heading('Timestamp', text='Timestamp')
    log_tree.column('Timestamp', width=150)

    for log_entry in logs:
        if all(k in log_entry for k in
               ['log_id', 'teacher_id', 'operation_type', 'student_id_affected', 'timestamp_str']):
            log_tree.insert("", "end", values=(
                log_entry['log_id'],
                log_entry['teacher_id'],
                log_entry['operation_type'],
                log_entry['student_id_affected'],
                log_entry['timestamp_str']
            ))
        else:
            print(f"Skipping log entry with unexpected format: {log_entry}")

    log_window.wait_window()



def main(teacher_id):
    global current_teacher_id, window, idEntry, nameEntry, phoneEntry, feesEntry
    global courseBox, genderBox, searchBox, searchEntry, tree
    global course_option, gender_option

    current_teacher_id = teacher_id

    window = CTk()
    window.geometry('950x600')
    window.resizable(False, False)
    window.title(f'Student Management System (Teacher: {current_teacher_id})')
    window.configure(fg_color='#161630')

    try:
        logo = CTkImage(Image.open('piche.png'), size=(930, 158))
        logoLabel = CTkLabel(window, image=logo, text='')
        logoLabel.grid(row=0, column=0, columnspan=2)
    except FileNotFoundError:
        print("Warning: piche.png not found.")
        placeholderLogo = CTkLabel(window, text="Student Management System", font=("Arial", 24, "bold"), text_color="white", height=158)
        placeholderLogo.grid(row=0, column=0, columnspan=2, sticky="nsew")
        window.grid_rowconfigure(0, weight=0)

    leftFrame = CTkFrame(window, fg_color='#161630')
    leftFrame.grid(row=1, column=0, padx=10, sticky="ns")
    bold_font = ('arial', 15, 'bold')

    idLabel = CTkLabel(leftFrame, text='Student Id', font=bold_font, text_color='white')
    idLabel.grid(row=1, column=0, padx=20, pady=15, sticky='w')
    idEntry = CTkEntry(leftFrame, font=bold_font, width=180)
    idEntry.grid(row=1, column=1, padx=5)

    nameLabel = CTkLabel(leftFrame, text='Name', font=bold_font, text_color='white')
    nameLabel.grid(row=2, column=0, padx=20, pady=15, sticky='w')
    nameEntry = CTkEntry(leftFrame, font=bold_font, width=180)
    nameEntry.grid(row=2, column=1, padx=5)

    phoneLabel = CTkLabel(leftFrame, text='Phone', font=bold_font, text_color='white')
    phoneLabel.grid(row=3, column=0, padx=20, pady=15, sticky='w')
    phoneEntry = CTkEntry(leftFrame, font=bold_font, width=180)
    phoneEntry.grid(row=3, column=1, padx=5)

    courseLabel = CTkLabel(leftFrame, text='Course', font=bold_font, text_color='white')
    courseLabel.grid(row=4, column=0, padx=20, pady=15, sticky='w')
    course_option = ['BBA', 'BCA', 'MBA', 'MCA', 'B-TECH', 'M-TECH']
    courseBox = CTkComboBox(leftFrame, values=course_option, width=180, font=bold_font, state='readonly')
    courseBox.grid(row=4, column=1, padx=5)
    courseBox.set(course_option[0])

    genderLabel = CTkLabel(leftFrame, text='Gender', font=bold_font, text_color='white')
    genderLabel.grid(row=5, column=0, padx=20, pady=15, sticky='w')
    gender_option = ['Male', 'Female', 'Other']
    genderBox = CTkComboBox(leftFrame, values=gender_option, width=180, font=bold_font, state='readonly')
    genderBox.grid(row=5, column=1, padx=5)
    genderBox.set(gender_option[0])

    feesLabel = CTkLabel(leftFrame, text='Fees', font=bold_font, text_color='white')
    feesLabel.grid(row=6, column=0, padx=20, pady=15, sticky='w')
    feesEntry = CTkEntry(leftFrame, font=bold_font, width=180)
    feesEntry.grid(row=6, column=1, padx=5)


    rightFrame = CTkFrame(window, fg_color='#161630')
    rightFrame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
    window.grid_columnconfigure(1, weight=1)

    search_options = ['Id', 'Name', 'Phone', 'Course', 'Gender', 'Fees']
    searchBox = CTkComboBox(rightFrame, values=search_options, state='readonly', font=bold_font, width=100)
    searchBox.grid(row=0, column=0, padx=5, pady=(0, 5))
    searchBox.set('Search by')

    searchEntry = CTkEntry(rightFrame, font=bold_font, width=150)
    searchEntry.grid(row=0, column=1, padx=5, pady=(0, 5))

    searchButton = CTkButton(rightFrame, text='Search', width=80, command=search_student, font=bold_font)
    searchButton.grid(row=0, column=2, padx=5, pady=(0, 5))

    showallButton = CTkButton(rightFrame, text='Show All', width=80, command=show_data, font=bold_font)
    showallButton.grid(row=0, column=3, padx=5, pady=(0, 5))

    treeFrame = CTkFrame(rightFrame, fg_color="transparent")
    treeFrame.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=5)
    rightFrame.grid_rowconfigure(1, weight=1)

    treeScrollY = CTkScrollbar(treeFrame)
    treeScrollY.pack(side="right", fill="y")
    treeScrollX = CTkScrollbar(treeFrame, orientation="horizontal")
    treeScrollX.pack(side="bottom", fill="x")

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background="#2D2D2D", foreground="white", fieldbackground="#3D3D3D", rowheight=25)
    style.map('Treeview', background=[('selected', '#0052cc')])

    tree = ttk.Treeview(treeFrame, height=15,
                        columns=('Id', 'Name', 'Phone', 'Course', 'Gender', 'Fees'),
                        show='headings', yscrollcommand=treeScrollY.set, xscrollcommand=treeScrollX.set)
    tree.pack(expand=True, fill="both")
    treeScrollY.configure(command=tree.yview)
    treeScrollX.configure(command=tree.xview)

    tree.column("Id", width=80, anchor=CENTER)
    tree.column("Name", width=150)
    tree.column("Phone", width=100, anchor=CENTER)
    tree.column("Course", width=100, anchor=CENTER)
    tree.column("Gender", width=80, anchor=CENTER)
    tree.column("Fees", width=80, anchor=E)

    for col in tree['columns']:
        tree.heading(col, text=col, anchor=CENTER)

    tree.bind("<ButtonRelease-1>", select_record)

    buttonFrame = CTkFrame(window, fg_color='#161630')
    buttonFrame.grid(row=2, column=0, columnspan=2, pady=10)

    # Action Buttons
    addButton = CTkButton(buttonFrame, text="Add Student", command=add_student, font=bold_font, width=120)
    addButton.grid(row=0, column=0, pady=5, padx=10)

    updateButton = CTkButton(buttonFrame, text="Update Student", command=update_student, font=bold_font, width=120)
    updateButton.grid(row=0, column=1, pady=5, padx=10)

    deleteButton = CTkButton(buttonFrame, text="Delete Student", command=delete_student, font=bold_font, width=120)
    deleteButton.grid(row=0, column=2, pady=5, padx=10)

    deleteallButton = CTkButton(buttonFrame, text="Delete All", command=delete_all, font=bold_font, width=120, fg_color="red", hover_color="#8B0000")
    deleteallButton.grid(row=0, column=3, pady=5, padx=10)

    logButton = CTkButton(buttonFrame, text="Show Logs", command=show_operation_logs, font=bold_font, width=120)
    logButton.grid(row=0, column=4, pady=5, padx=10)


    show_data()

    window.mainloop()


