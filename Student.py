
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import logging

logging.basicConfig(filename='bookingTransactions.log',
                    filemode='a',
                    format='%(asctime)s - %(message)s',
                    level=logging.DEBUG)


class Student:
    def __init__(self, id):

        self.id = id
        self.window = Tk()
        self.window.title("Student")
        self.window.geometry('800x800')
        self.window.geometry("+600+200")
        self.window.resizable(False, False)
        photo1 = PhotoImage(file='sbg1.png')  # book a ticket
        photo2 = PhotoImage(file='sbg2.png')  # view my tickets

        self.connection = sqlite3.connect("centralDB.db")

        self.tabs = ttk.Notebook(self.window, style="Notebook.Heading")
        self.bookTab = Frame(self.tabs)
        self.viewTab = Frame(self.tabs)
        self.tabs.add(self.bookTab, text='Book a Ticket')
        self.tabs.add(self.viewTab, text="View my tickets")
        self.tabs.pack(expand=True, fill='x', )
        self.bgImg1 = Label(self.bookTab, image=photo1)
        self.bgImg2 = Label(self.viewTab, image=photo2)
        self.bgImg1.pack()
        self.bgImg2.pack()

        style = ttk.Style(self.window)
        style.theme_use("clam")
        style.configure("Treeview", background="#333739", fieldbackground="#333739", foreground="#ffffff")
        style.configure("Treeview.Heading", background="#333739", foreground="#ffffff")
        style.configure("Notebook.Heading", background="#333739", foreground="#ffffff")
        style.configure("Notebook.Heading.Tab", background="#333739", foreground="#ffffff")

        self.eventList = ttk.Treeview(self.bookTab, columns=(1, 2, 3, 4), show='headings', height=8)
        self.eventList.column("1", width=60)
        self.eventList.column("2", width=300)
        self.eventList.column("3", width=120)
        self.eventList.column("4", width=180)
        self.eventList.heading(1, text='Event ID')
        self.eventList.heading(2, text='Event Name')
        self.eventList.heading(3, text='Location')
        self.eventList.heading(4, text='Date & Time')

        self.bookButton = Button(self.bookTab, text="Book", command=self.bookFunc, fg='white',
                                 background='#333739', activebackground='#333739')
        self.buttonBack1 = Button(self.bookTab, text='Logout', command=self.logout, fg='white', background='#333739',
                                  activebackground='#333739')

        # BOOK A TICKET PLACE
        self.eventList.place(x=20, y=200, width=750)
        self.bookButton.place(x=330, y=400, width=150, height=35)
        self.buttonBack1.place(x=330, y=600, width=150, height=35)

        # VIEW MY TICKETS TAB
        self.showEvent = ttk.Treeview(self.viewTab, columns=(1, 2, 3, 4), show='headings', height=8)
        self.showEvent.column("1", width=60)
        self.showEvent.column("2", width=300)
        self.showEvent.column("3", width=120)
        self.showEvent.column("4", width=180)
        self.showEvent.heading(1, text='Event ID')
        self.showEvent.heading(2, text='Event Name')
        self.showEvent.heading(3, text='Location')
        self.showEvent.heading(4, text='Date & Time')
        self.showButton = Button(self.viewTab, text="Show", command=self.viewStudentTickets, fg='white',
                                 background='#333739', activebackground='#333739')
        self.buttonBack2 = Button(self.viewTab, text='Logout', command=self.logout, fg='white', background='#333739',
                                  activebackground='#333739')

        # VIEW MY TICKET PLACE
        self.showEvent.place(x=20, y=200, width=750)
        self.showButton.place(x=330, y=400, width=150, height=35)
        self.buttonBack2.place(x=330, y=600, width=150, height=35)

        self.showAvailable()

        self.window.mainloop()

    def logout(self):
        self.connection.close()
        self.window.destroy()
        import Signup
        Signup.Signup()

    def viewStudentTickets(self):
        self.clearTree()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        table = self.connection.execute(f"SELECT E_ID,ENAME,LOCATION,DATE_TIME FROM BOOKING WHERE S_ID = {self.id} AND DATE_TIME > '{current_time}'")
        count = 0
        for rows in table:
            self.showEvent.insert(parent='', index=count, text='', values=(rows[0], rows[1], rows[2], rows[3]))
            count += 1

    def bookFunc(self):
        try:
            cur = self.eventList.focus()
            eid = self.eventList.item(cur)["values"][0]
            table = self.connection.execute(
                f"SELECT EID,ENAME,LOCATION,DATE_TIME FROM EVENT WHERE CAPACITY != RESERVED AND EID = {eid}")
            for i in table:
                eidd = i[0]
                enamee = i[1]
                locationn = i[2]
                datee_timee = i[3]
                acdt = datetime.strptime(datee_timee, "%Y-%m-%d %H:%M")
                current_time = datetime.now()
                if acdt < current_time:
                    messagebox.showerror("Error", "Event is outdated")
                    return
                else:
                    self.finalBook(eidd, enamee, locationn, datee_timee)
                    return
            else:
                messagebox.showerror("Error", "Event is full")
                return
        except IndexError:
            messagebox.showerror("Error", "You have not selected an event")

    def showAvailable(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        table = self.connection.execute(f"SELECT EID, ENAME, LOCATION, DATE_TIME FROM EVENT WHERE DATE_TIME > '{current_time}'")
        count = 0
        for rows in table:
            self.eventList.insert(parent='', index=count, text='', values=(rows[0], rows[1], rows[2], rows[3]))
            count += 1

    def finalBook(self, eid, ename, location, date_time):
        table = self.connection.execute(f"SELECT S_ID FROM BOOKING WHERE S_ID = {self.id} AND E_ID = {eid}")
        for i in table:
            messagebox.showerror("Error", "You have already booked this event")
            return

        self.connection.execute("INSERT INTO BOOKING (S_ID, E_ID, ENAME,LOCATION, DATE_TIME) VALUES (?, ?, ?, ?, ?)",
                                (self.id, eid, ename, location, date_time))
        self.connection.commit()

        self.connection.execute(f"UPDATE EVENT SET RESERVED = RESERVED + 1 WHERE EID = {eid}")
        self.connection.commit()

        messagebox.showinfo("Success", f"You have successfully booked a ticket for {ename}")
        logging.info(f"{ename}, {location}, {self.id}")

    def clearTree(self):
        for i in self.showEvent.get_children():
            self.showEvent.delete(i)
