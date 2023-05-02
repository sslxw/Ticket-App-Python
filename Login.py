import hashlib
import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import *


class Login:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Login")
        self.window.geometry('800x800')
        self.window.geometry("+600+200")
        self.window.resizable(False, False)
        photo = PhotoImage(file='lbg.png')
        self.bgImg = Label(self.window, image=photo)
        self.bgImg.pack()

        self.buttonBack = tk.Button(self.window, text='Sign up', command=self.pass_to_signup, fg='white',
                                    background='#333739', activebackground='#333739')
        self.buttonBack.place(x=400, y=600, anchor="center", width=150, height=35)
        self.buttonLogin = tk.Button(self.window, text='Login', command=self.login_check, fg='white',
                                     background='#333739', activebackground='#333739')
        self.toggleButton = tk.Button(self.window, text='Show Password', width=12, command=self.show_password,
                                      fg='white', background='#333739', activebackground='#333739')
        self.buttonLogin.place(x=400, y=475, anchor="center", width=150, height=35)
        self.studentID = tk.StringVar()
        self.studentPassword = tk.StringVar()
        self.entryStudentID = tk.Entry(self.window, textvariable=self.studentID)
        self.entryStudentPassword = tk.Entry(self.window, textvariable=self.studentPassword, show="*")
        self.entryStudentID.place(x=400, y=360, anchor="center", width=250, height=25)
        self.entryStudentPassword.place(x=400, y=410, anchor="center", width=250, height=25)
        self.toggleButton.place(x = 538, y = 398)
        self.window.mainloop()

    def pass_to_signup(self):
        self.window.destroy()
        import Signup
        Signup.Signup()

    def pass_to_student(self):
        self.window.destroy()
        self.connection.close()
        import Student
        Student.Student(self.id)

    def pass_to_admin(self):
        self.window.destroy()
        self.connection.close()
        import Admin
        Admin.Admin()

    def login_check(self):
        if len(self.entryStudentID.get()) != 10 or self.entryStudentID.get().isdigit() is False:
            messagebox.showerror("Error", "Please make sure ID only contains digits and is 10 numbers long")
            return
        elif len(self.entryStudentPassword.get()) < 6 or (self.entryStudentPassword.get()).isalnum() is False:
            messagebox.showerror("Error", "Please make sure password is longer than 6 characters \nand only contains "
                                          "numbers or letters")
            return

        self.check_acc()

    def check_acc(self):
        self.connection = sqlite3.connect("centralDB.db")
        cur = self.connection.execute(f"SELECT ID,PASSWORD FROM ACCOUNT WHERE ID = {self.entryStudentID.get()}")
        hashedP = hashlib.sha256(self.entryStudentPassword.get().encode()).hexdigest()

        for i in cur:
            if self.entryStudentID.get() == i[0] and hashedP == i[1]:
                self.login()
                return
            else:
                messagebox.showerror("Error", "ID or password is incorrect")
                return

        messagebox.showerror("Error", "User does not exist")

    def login(self):
        cur = self.connection.execute(f"SELECT USER_TYPE FROM ACCOUNT WHERE ID = {self.entryStudentID.get()}")

        for i in cur:
            type = i[0]

        if type == 'student':
            self.id = self.entryStudentID.get()
            self.pass_to_student()
        elif type == 'admin':
            self.pass_to_admin()

    def show_password(self):
        if self.entryStudentPassword.cget('show') == '':
            self.entryStudentPassword.config(show='*')
            self.toggleButton.config(text='Show Password')
        else:
            self.entryStudentPassword.config(show='')
            self.toggleButton.config(text='Hide Password')



