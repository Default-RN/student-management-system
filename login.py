from customtkinter import *
from PIL import Image
from tkinter import messagebox
import db1
import sms1

def login():
    teacher_id = idEntry.get()
    password = passwordEntry.get()
    if teacher_id == '' or password == '':
        messagebox.showerror('Error', 'All fields are required')
    else:
        if db1.login_teacher(teacher_id, password):
            messagebox.showinfo('Success', 'Login Successful')
            root.destroy()
            sms1.main(teacher_id)
        else:
            pass


def open_registration():
    root.destroy()

root = CTk()
root.geometry('930x478')
root.resizable(False, False)
root.title('Teacher Login Page')

try:
    image = CTkImage(Image.open('bg.jpg'), size=(930, 478))
    imageLabel = CTkLabel(root, image=image, text='')
    imageLabel.place(x=0, y=0)
except FileNotFoundError:
    print("Warning: bg.jpg not found. Background image will not be displayed.")
    root.configure(fg_color='gray')


headingLabel = CTkLabel(root, text='Student Management System - Teacher Portal', bg_color='#FAFAFA', text_color='dark blue')
headingLabel.place(x=20, y=100)

idEntry = CTkEntry(root, placeholder_text='Enter Your Teacher ID', width=180)
idEntry.place(x=25, y=150)

passwordEntry = CTkEntry(root, placeholder_text='Enter Your Password', width=180, show='*')
passwordEntry.place(x=25, y=200)

loginButton = CTkButton(root, text='Login', cursor='hand2', command=login)
loginButton.place(x=50, y=250)

registerButton = CTkButton(root, text='Register Teacher', cursor='hand2', command=open_registration)
registerButton.place(x=50, y=300)

root.mainloop()