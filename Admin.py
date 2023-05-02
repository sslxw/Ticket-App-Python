import csv
import re
import tkinter
import tkinter as tk
from tkinter import *
import random
import sqlite3
from tkinter import messagebox
from datetime import datetime

class Admin:
    def __init__(self):
        self.connection = sqlite3.connect("centralDB.db")

        self.window = tk.Tk()
        self.window.title("Admin")
        self.window.geometry('800x800')
        self.window.geometry("+600+200")
        self.window.resizable(False,False)
        self.photo = PhotoImage(file='abg.png')
        self.bgImg = Label(self.window, image=self.photo)
        self.bgImg.pack()

        self.sportsName = StringVar()
        self.sportsLocation = StringVar()
        self.sportsCapacity = StringVar()
        self.sportsDate = StringVar()
        self.sportsTime = StringVar()

        self.entryName = tk.Entry(self.window, textvariable=self.sportsName)
        self.entryLocation = tk.Entry(self.window, textvariable=self.sportsLocation)
        self.entryCapacity = tk.Entry(self.window, textvariable=self.sportsCapacity)
        self.entryDate = tk.Entry(self.window, textvariable=self.sportsDate, fg="black")
        self.entryTime = tk.Entry(self.window, textvariable=self.sportsTime, fg="black")
        self.buttonCreate = tk.Button(self.window, text='Create', command=self.admin_check, fg='white', background='#333739',
                                      activebackground='#333739')
        self.buttonLogin = tk.Button(self.window, text='Logout', command=self.logout, fg='white', background='#333739',
                                    activebackground='#333739')

        self.buttonBackup = tk.Button(self.window, text='Backup', command=self.admin_backup, fg='white', background='#333739',
                                    activebackground='#333739')

        self.entryName.place(x=520, y=300, anchor="center", width=250, height=25)

        self.entryLocation.place(x=520, y=350, anchor="center", width=250, height=25)

        self.entryCapacity.place(x=520, y=400, anchor="center", width=250, height=25)

        self.entryDate.place(x=520, y=450, anchor="center", width=250, height=25)

        self.buttonCreate.place(x=520, y=500, anchor="center", width=150, height=35)

        self.buttonBackup.place(x=400, y=750, anchor="center", width=150, height=35)

        self.buttonLogin.place(x=400, y=700, anchor="center", width=150, height=35)

        self.entryDate.insert(0, "YYYY-MM-DD HH:MM")

        self.window.mainloop()

    def logout(self):
        self.window.destroy()
        self.connection.close()
        import Signup
        Signup.Signup()

    def admin_create(self):
        eventID = random.randint(10000, 99999)
        eventName = self.entryName.get()
        eventLocation = self.entryLocation.get()
        eventCapacity = self.entryCapacity.get()
        eventDate = self.entryDate.get()

        self.connection.execute("INSERT INTO EVENT \
                             (EID,ENAME,LOCATION,CAPACITY,RESERVED,DATE_TIME) VALUES \
                             (?, ?, ?, ?, 0, ?)", (eventID, eventName, eventLocation, eventCapacity, eventDate))
        self.connection.commit()

        self.entryName.delete(0, END)
        self.entryLocation.delete(0, END)
        self.entryCapacity.delete(0, END)
        self.entryDate.delete(0, END)
        self.entryTime.delete(0, END)

        messagebox.showinfo("Event created", "Event created successfully")

    def admin_check(self):
        dateReg = "^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01]) ([01][0-9]|2[0-3]):([0-5][0-9])$"
        datePat = re.compile(dateReg)

        if len(self.entryName.get()) == 0:
            tkinter.messagebox.showerror(title="Error", message="Please provide an input for event name")
            return
        elif len(self.entryLocation.get()) == 0:
            tkinter.messagebox.showerror(title="Error", message="Please provide an input for event location")
            return
        elif len(self.entryCapacity.get()) == 0 or self.entryCapacity.get().isdigit() is False:
            tkinter.messagebox.showerror(title="Error", message="Please provide an input for event capacity")
            return
        elif len(self.entryDate.get()) == 0 or not re.search(datePat, self.entryDate.get()):
            tkinter.messagebox.showerror(title="Error", message="Please provide a correct input for event date & time ex: YYYY-MM-DD HH:MM")
            return

        self.admin_create()

    def admin_backup(self):
        file = open("backup.csv", 'a')
        csvf = csv.writer(file)

        csvf.writerow(["---------------------------------------------------------------------"])

        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        list1 = ["Backup was created at", current_time]
        csvf.writerow(list1)

        for table in ["ACCOUNT", "EVENT", "BOOKING"]:
            csvf.writerow([f"{table} Table"])
            cursor = self.connection.execute(f"SELECT * FROM {table}")
            for x in cursor:
                csvf.writerow(x)

        csvf.writerow(["---------------------------------------------------------------------"])
        file.close()
        messagebox.showinfo("Backup", "Backup done successfully")


