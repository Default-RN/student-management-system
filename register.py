import string
from customtkinter import *
from PIL import Image
from tkinter import messagebox
import db1

logged_in_teacher_id = None

def register():
    teacher_id = idEntry.get()
    password = passwordEntry.get()

    if teacher_id == '' or password == '':
        messagebox.showerror('Error', 'All fields are required')
        return

    try:


        if not any(char in "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~" for char in password):
                messagebox.showerror('Password Error', 'Password must contain at least one special character.')
                return

        if db1.check_password_exists(password):
            messagebox.showerror('Password Error', 'This password is already in use. Please choose a different one.')
            return
    except AttributeError:
         messagebox.showerror('DB Error', 'Database module is missing the check_password_exists function.')
         print("ERROR: Ensure db1.py has a function named 'check_password_exists(password)'")
         return
    except Exception as e:
        messagebox.showerror('DB Error', f'Error checking password uniqueness: {e}')
        return

    try:
        if db1.register_teacher(teacher_id, password):
            messagebox.showinfo('Success', 'Teacher Registration Successful')
            root.destroy()
            import login
    except Exception as e:
        messagebox.showerror('Registration Error', f'An error occurred during registration: {e}')


def back_to_login():
    root.destroy()
    import login

root = CTk()
root.geometry('930x580')
root.resizable(False, False)
root.title('Teacher Registration Page')

bg_image = CTkImage(Image.open('reg.png'), size=(930, 580))
bg_label = CTkLabel(root, image=bg_image, text="")
bg_label.place(x=0, y=0)

card = CTkFrame(root, fg_color='white', corner_radius=20, width=450, height=400)
card.place(relx=0.5, rely=0.5, anchor=CENTER)

headingLabel = CTkLabel(card, text='Create Teacher Account', font=('Arial Black', 24), text_color='black')
headingLabel.pack(pady=(30, 20))

idEntry = CTkEntry(card,
                     placeholder_text='Enter Your Teacher ID',
                     width=350, height=40, corner_radius=8,
                     text_color='black',
                     fg_color='white',
                     placeholder_text_color='gray')
idEntry.pack(pady=10)

passwordEntry = CTkEntry(card,
                         placeholder_text='Create Password',
                         width=350, height=40, corner_radius=8,
                         show='*',
                         text_color='black',
                         fg_color='white',
                         placeholder_text_color='gray')
passwordEntry.pack(pady=10)

registerButton = CTkButton(card,
                           text='Register Teacher',
                           width=350, height=40, corner_radius=8,
                           fg_color='#007bff',
                           hover_color='#0056b3',
                           text_color='white',
                           command=register)
registerButton.pack(pady=(25, 10))

backButton = CTkButton(card,
                      text='Back to Login',
                      width=350, height=40, corner_radius=8,
                      fg_color='red',
                      hover_color='light red',
                      text_color='white',
                      command=back_to_login)
backButton.pack()

root.mainloop()