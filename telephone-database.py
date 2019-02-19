# Code derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/

import tkinter as tk

from tkinter import *

import shelve

data = shelve.open('database')

LARGE_FONT = ("Helvetica", 25)


class Telephone(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        root = tk.Frame(self)

        root.pack(side="top", fill="both", expand=True)

        root.grid_rowconfigure(3, weight=1)
        root.grid_columnconfigure(3, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            frame = F(root, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Phonebook", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Create/Edit Records",
                           command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = tk.Button(self, text="Search Records",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = tk.Button(self, text="Delete Records",
                            command=lambda: controller.show_frame(PageThree))

        button3.pack()

        button4 = tk.Button(self, text="Show All Records",
                            command=lambda: controller.show_frame(PageFour))

        button4.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Create/Edit Records", font=LARGE_FONT)
        self.cmd = IntVar()

        self.label.grid(row=0, column=2)

        self.label1 = tk.Label(self, text="Name")
        self.label2 = tk.Label(self, text="Phone")
        self.label3 = tk.Label(self, text="Address")

        self.entry1 = tk.Entry(self, width=20)
        self.entry2= tk.Entry(self, width=20)
        self.entry3 = tk.Entry(self, width=20)

        self.label1.grid(row=1, column=1)
        self.label2.grid(row=2, column=1)
        self.label3.grid(row=3,column=1)

        self.entry1.grid(row=1, column=2)
        self.entry2.grid(row=2, column=2)
        self.entry3.grid(row=3, column=2)

        self.radio1 = Radiobutton(self, text="Personal",variable=self.cmd,value=1)
        self.radio2 = Radiobutton(self, text="Business",variable=self.cmd,value=2)

        self.ve = tk.Label(self)
        self.ve.grid(row=7,column=2)

        self.radio1.grid(row=4,column=1)
        self.radio2.grid(row=4,column=2)

        self.button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))

        self.button1.grid(row=6, column=2)


        self.button2 = tk.Button(self, text="Save Record",
                            command=lambda: self.save_record())

        self.button2.grid(row=5, column=2)


    def save_record(self):
        c = self.cmd.get()  # radio button value
        e1 = self.entry1.get()  # name
        e2 = self.entry2.get()  # phone
        e3 = self.entry3.get()  # address
        text = self.ve

        if len(e1) == 0:
            text.config(text="Check all inputs.",fg='red')
        elif len(e2) == 0:
            text.config(text="Check all inputs.",fg='red')
        elif len(e3) == 0:
            text.config(text="Check all inputs.",fg='red')
        else:
            if c == 1:
                lst = [e2, e3, "Personal"]
                data[e1] = lst
                text.config(text="Success. Database Updated.",fg='green')
            elif c == 2:
                lst = [e2, e3, "Business"]
                data[e1] = lst
                text.config(text="Success. Database Updated.",fg='green')
        for keys in data.keys():
            print(keys," ", data[keys])



class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Search Records", font=LARGE_FONT)
        self.label.grid(row=0,column=2)

        self.label1 = tk.Label(self, text="Search by Name:")
        self.entry1 = tk.Entry(self, width=20)

        self.label1.grid(row=1,column=1)
        self.entry1.grid(row=1,column=2)

        self.founddata = tk.Label(self)
        self.founddata.grid(row=4,column=2)

        self.button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        self.button2 = tk.Button(self, text="Search",
                            command=lambda: self.find_record())

        self.button2.grid(row=2,column=2)
        self.button1.grid(row=3,column=2)

    def find_record(self):

        e1 = self.entry1.get()
        text = self.founddata
        keys = data.keys()

        if e1 in keys:
            text.config(text="Record Found:\n"+e1+"\nPhone: "+data[e1][0]+"\nAddress: "+data[e1][1]+"\nType: "+data[e1][2]+"\n",fg='black')
        else:
            text.config(text="No Record Found",fg='red')

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Delete Contact", font=LARGE_FONT)
        self.label.grid(row=0,column=2)

        self.label1 = tk.Label(self, text="Search by Name:")
        self.entry1 = tk.Entry(self, width=20)

        self.button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))

        self.button2 = tk.Button(self, text="Find and Delete",
                            command=lambda: self.delete_entry())

        self.infoLabel = tk.Label(self)

        self.label1.grid(row=1,column=1)
        self.entry1.grid(row=1,column=2)
        self.button1.grid(row=3,column=2)
        self.button2.grid(row=2,column=2)
        self.infoLabel.grid(row=5,column=2)


    def delete_entry(self):

        e1 = self.entry1.get()      # entry text
        info = self.infoLabel
        keys = data.keys()

        if e1 not in keys:
            info.config(text="No such name. Try again.",fg='red')
        else:
            info.config(text="Record successfully deleted:\n"+e1+"\nPhone: "+data[e1][0]+"\nAddress: "+data[e1][1]+"\nType: "+data[e1][2]+"\n",fg='green')
            del data[e1]

class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="All Records", font=LARGE_FONT)
        self.label.grid(row=0,column=2)

        self.label1 = tk.Label(self,text="")
        self.label1.grid(row=2, column=2)

        self.button1 = tk.Button(self, text="Refresh/List All Records",
                            command=lambda: self.show_records())
        self.button2 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))

        self.button1.grid(row=1,column=2)
        self.button2.grid(row=3,column=2)



    def show_records(self):

        records = self.label1
        string = ""

        for key in data.keys():
            string = string + "Name:"+key+"\nPhone: "+data[key][0]+"\nAddress: "+data[key][1]+"\nType: "+data[key][2]+"\n\n"

        records.config(text=string)

app = Telephone()
app.mainloop()


