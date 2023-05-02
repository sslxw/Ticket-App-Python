import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sqlite3
import hashlib


class Signup:
    def __init__(self):
        self.connection = sqlite3.connect("centralDB.db")
        self.create_table()
        self.create_admin()

        self.window = tk.Tk()
        self.window.title("Sign up")
        self.window.geometry('800x800')
        self.window.geometry("+600+200")  # to position the window in the center
        self.window.resizable(False,False)
        self.photo = PhotoImage(file='bg.png')
        self.bgImg = Label(self.window, image=self.photo)
        self.bgImg.pack()

        self.firstName = StringVar()
        self.lastName = StringVar()
        self.studentID = StringVar()
        self.studentPassword = StringVar()
        self.studentEmail = StringVar()
        self.studentPhone = StringVar()

        self.entryFirstName = tk.Entry(self.window, textvariable=self.firstName)

        self.entryLastName = tk.Entry(self.window, textvariable=self.lastName)

        self.entryStudentID = tk.Entry(self.window, textvariable=self.studentID)

        self.entryStudentPassword = tk.Entry(self.window, textvariable=self.studentPassword, show="*")

        self.entryStudentEmail = tk.Entry(self.window, textvariable=self.studentEmail)

        self.entryStudentPhone = tk.Entry(self.window, textvariable=self.studentPhone)

        self.buttonSignup = tk.Button(self.window, text='Sign up', command=self.signup_check, fg='white',
                                      background='#333739', activebackground='#333739')
        self.buttonLogin = tk.Button(self.window, text='Login', command=self.Login, fg='white', background='#333739',
                                     activebackground='#333739')

        self.toggleButton = tk.Button(self.window, text='Show Password', width=12, command=self.show_password, fg='white',
                                      background='#333739', activebackground='#333739')

        self.entryFirstName.place(x=400, y=293, anchor="center", width=250, height=25)

        self.entryLastName.place(x=400, y=343, anchor="center", width=250, height=25)

        self.entryStudentID.place(x=400, y=397, anchor="center", width=250, height=25)

        self.entryStudentPassword.place(x=400, y=450, anchor="center", width=250, height=25)

        self.entryStudentEmail.place(x=400, y=500, anchor="center", width=250, height=25)

        self.entryStudentPhone.place(x=400, y=550, anchor="center", width=250, height=25)

        self.buttonSignup.place(x=400, y=600, anchor="center", width=150, height=35)

        self.toggleButton.place(x=538, y=438)

        self.buttonLogin.place(x=400, y=725, anchor="center", width=150, height=35)

        self.window.mainloop()

    def Login(self):
        self.window.destroy()
        self.connection.close()
        import Login
        Login.Login()

    def signup_check(self):
        import re
        emailReg = "^([a-zA-Z0-9\._-]+)(@ksu.edu.sa)$"
        emailPat = re.compile(emailReg)
        phoneReg = "^(05)[0-9]{8}$"
        phonePat = re.compile(phoneReg)

        if (self.entryFirstName.get()).isalpha() is False:
            messagebox.showerror("Error", "Please make sure first name only contains letters")
            return
        elif (self.entryLastName.get()).isalpha() is False:
            messagebox.showerror("Error", "Please make sure last name only contains letters")
            return
        elif (len(self.entryStudentID.get()) != 10) or (self.entryStudentID.get()).isdigit() is False:
            messagebox.showerror("Error", "Please make sure ID is 10 digits long and digits only")
            return
        elif len(self.entryStudentPassword.get()) < 6 or (self.entryStudentPassword.get()).isalnum() is False:
            messagebox.showerror("Error", "Please make sure password is longer than 6 characters \nand only contains "
                                          "numbers or letters")
            return
        elif not re.search(emailPat, self.entryStudentEmail.get().lower()):
            messagebox.showerror("Error", "Please make sure you have entered a valid ksu.edu.sa email")
            return
        elif not re.search(phonePat, self.entryStudentPhone.get()):
            messagebox.showerror("Error", "Please make sure phone number is 10 digits long and starts with 05")
            return

        if self.check_email() == False:
            return
        if self.check_phone() == False:
            return
        self.signup_submit()

    def create_table(self):

        self.connection.execute('''CREATE TABLE IF NOT EXISTS ACCOUNT
                               (
                                ID              VARCHAR(10)     PRIMARY KEY     NOT NULL,
                                FIRST_NAME      TEXT                            NOT NULL,
                                LAST_NAME       TEXT                            NOT NULL,
                                PASSWORD        TEXT                            NOT NULL,
                                EMAIL           VARCHAR(20)                     NOT NULL,
                                PHONE           VARCHAR(10)                     NOT NULL,
                                USER_TYPE       TEXT
                       );''')
        self.connection.commit()

        self.connection.execute('''CREATE TABLE IF NOT EXISTS EVENT
                               (
                                EID             VARCHAR(5)     PRIMARY KEY      NOT NULL,
                                ENAME           TEXT                            NOT NULL,
                                LOCATION        TEXT                            NOT NULL,
                                CAPACITY        INT                             NOT NULL,
                                RESERVED        INT                             NOT NULL,
                                DATE_TIME       DATETIME                        NOT NULL
                       );''')
        self.connection.commit()

        self.connection.execute('''CREATE TABLE IF NOT EXISTS BOOKING
                                     (
                                      S_ID           VARCHAR(10)        NOT NULL,
                                      E_ID           VARCHAR(5)         NOT NULL,
                                      ENAME          TEXT               NOT NULL,
                                      LOCATION       TEXT               NOT NULL,
                                      DATE_TIME      DATETIME           NOT NULL,
                                      FOREIGN KEY(S_ID) REFERENCES ACCOUNT(ID),
                                      FOREIGN KEY(E_ID) REFERENCES EVENT(EID)
                             );''')
        self.connection.commit()

    def create_admin(self):
        p = "admin000"
        password = hashlib.sha256(p.encode()).hexdigest()
        try:
            self.connection.execute(f"INSERT INTO ACCOUNT \
                        (ID,FIRST_NAME,LAST_NAME,PASSWORD,EMAIL,PHONE, USER_TYPE) VALUES \
                        ('9999999999','admin','admin','{password}','admin@ksu.edu.sa','0500000000', 'admin')")
            self.connection.commit()
        except sqlite3.IntegrityError:
            print("")

    def signup_submit(self):
        first_name = self.entryFirstName.get()
        last_name = self.entryLastName.get()
        studentID = self.entryStudentID.get()
        passwordN = self.entryStudentPassword.get()
        email = self.entryStudentEmail.get()
        phone = self.entryStudentPhone.get()
        utype = "student"

        password = hashlib.sha256(passwordN.encode()).hexdigest()

        try:
            self.connection.execute("INSERT INTO ACCOUNT \
                       (ID,FIRST_NAME,LAST_NAME,PASSWORD,EMAIL,PHONE, USER_TYPE) VALUES \
                       (?, ?, ?, ?, ?, ?, ?)", (studentID, first_name, last_name, password, email, phone, utype))
            self.connection.commit()

            self.entryFirstName.delete(0, "end")
            self.entryLastName.delete(0, "end")
            self.entryStudentID.delete(0, "end")
            self.entryStudentPassword.delete(0, "end")
            self.entryStudentEmail.delete(0, "end")
            self.entryStudentPhone.delete(0, "end")

            messagebox.showinfo("Account created", "Account created successfully")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Account already exists")

    def check_email(self):
        em = self.connection.execute(f"SELECT EMAIL FROM ACCOUNT WHERE EMAIL = '{self.entryStudentEmail.get()}'")
        for i in em:
            messagebox.showerror("Error", "Email is already taken")
            return False

    def check_phone(self):
        ph = self.connection.execute(f"SELECT PHONE FROM ACCOUNT WHERE PHONE = '{self.entryStudentPhone.get()}'")
        for i in ph:
            messagebox.showerror("Error", "Phone is already taken")
            return False

    def show_password(self):
        if self.entryStudentPassword.cget('show') == '':
            self.entryStudentPassword.config(show='*')
            self.toggleButton.config(text='Show Password')
        else:
            self.entryStudentPassword.config(show='')
            self.toggleButton.config(text='Hide Password')


