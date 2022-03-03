from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import re
import os

import pymysql

from View import model
from View.model import getAccountNumberFromFace


class FATM(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.faceRecognizer,self.ready = model.trainClassifier()
        self.attributes("-fullscreen", True)
        self.frames = {}
        for F in (MainPanel, AdminPanel):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        for path,subdir,filenames in os.walk("data/"):
            os.chmod(path, 0o777)
            for filename in filenames:
                pass

        self.showFrame(MainPanel)

    def showFrame(self, page):
        frame = self.frames[page]
        frame.tkraise()


class MainPanel(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        #  Background Image
        self.bg = PhotoImage(file="View/mainBack.PNG")
        self.closeImg = PhotoImage(file="View/close.png")
        label1 = Label(self, image=self.bg)

        label1.place(x=0, y=0, relwidth=1, relheight=1)
        self.close = Button(self, image=self.closeImg, command=self.closeFunc, bd=0)
        self.close.place(x=1100, y=10, width=30, height=30)

        self.withdrawl = Button(self, text=" Cash Withdrawl ", padx=30, pady=3, fg="white", bg="#006daf",
                                activebackground="#00497f", bd=0, state="normal", relief="groove",
                                highlightcolor="#00497f", activeforeground="white", font=("Comic Sans MS", 17),
                                command=self.withdrawlFunc)
        self.withdrawl.place(x=1000, y=180)

        self.deposit = Button(self, text="  Deposit Cash    ", padx=30, pady=3, fg="white", bg="#006daf",
                              activebackground="#00497f", bd=0, state="normal", relief="groove",
                              highlightcolor="#00497f", activeforeground="white", font=("Comic Sans MS", 17),
                              command=self.depositFunc)
        self.deposit.place(x=1000, y=280)

        self.balance = Button(self, text="Balance Enquiry   ", padx=30, pady=3, fg="white", bg="#006daf",
                              activebackground="#00497f",
                              bd=0, state="normal", relief="groove", highlightcolor="#00497f", activeforeground="white",
                              font=("Comic Sans MS", 17), command=self.balanceEnquiryFunc)
        self.balance.place(x=1000, y=380)

        self.pin = Button(self, text="   Pin Change   ", padx=30, pady=3, fg="white", bg="#006daf",
                          activebackground="#00497f",
                          bd=0, state="normal", relief="groove", highlightcolor="#00497f", activeforeground="white",
                          font=("Comic Sans MS", 17), command=self.pinFunc)
        self.pin.place(x=0, y=180)

        self.transfer = Button(self, text="  Transfer Funds", padx=24, pady=3, fg="white", bg="#006daf",
                               activebackground="#00497f", bd=0, state="normal", relief="groove",
                               highlightcolor="#00497f",
                               activeforeground="white", font=("Comic Sans MS", 17), command=self.transferFunc)
        self.transfer.place(x=-20, y=280)

        self.admin = Button(self, text="  Admin Login  ", padx=30, pady=3, fg="white", bg="#006daf",
                            activebackground="#00497f", bd=0, state="normal", relief="groove", highlightcolor="#00497f",
                            activeforeground="white", font=("Comic Sans MS", 17), command=self.adminFunc)
        self.admin.place(x=0, y=380)

        self.withdrawl.bind("<Enter>", lambda id: self.withdrawl.place(x=980))
        self.withdrawl.bind("<Leave>", lambda id: self.withdrawl.place(x=1000))
        self.deposit.bind("<Enter>", lambda id: self.deposit.place(x=980))
        self.deposit.bind("<Leave>", lambda id: self.deposit.place(x=1000))
        self.balance.bind("<Enter>", lambda id: self.balance.place(x=980))
        self.balance.bind("<Leave>", lambda id: self.balance.place(x=1000))

        self.pin.bind("<Enter>", lambda id: self.pin.config(padx=40))
        self.pin.bind("<Leave>", lambda id: self.pin.config(padx=30))
        self.admin.bind("<Enter>", lambda id: self.admin.config(padx=40))
        self.admin.bind("<Leave>", lambda id: self.admin.config(padx=30))
        self.transfer.bind("<Enter>", lambda id: self.transfer.config(padx=40))
        self.transfer.bind("<Leave>", lambda id: self.transfer.config(padx=30))

    def withdrawlFunc(self):
        print("withdrawlFunc")
        if(self.controller.ready==False):
            messagebox.showerror("No data","Model trained without any data, Update Model")
            return

        accNo = getAccountNumberFromFace(self.controller.faceRecognizer)

        if (accNo == ""):
            return

        con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
        cur = con.cursor()
        cur.execute("select accountHolder,pin,balance from userdata where accountNo=" + accNo)
        data = cur.fetchall()

        con.commit()
        con.close()
        #if(len(data)!=1):
         #   messagebox.showerror("Wrong","Something went Wrong")
          #  return
        accountHolder = data[0][0]
        pin=data[0][1]
        balance=data[0][2]
        resp=messagebox.askyesno("Account Confirmation",
                            "Is this your Account: \nAccount Holder Name: " + accountHolder + "\nAccount Number: " + accNo)
        if not resp:
            return
        else:
            self.pinpop = Toplevel(self)
            self.pinpop.title("Password Entry")
            self.pinpop.geometry("450x250+542+307")
            self.pinpop.config(bg="black")

            self.backgroundd1 = PhotoImage(file="View/mainBack.PNG")
            self.pinpop.resizable(False, False)
            # pop.attributes('-disabled', True)
            label1 = Label(self.pinpop, image=self.backgroundd1)
            label1.place(x=0, y=0, relwidth=1, relheight=1)
            self.pinpop.overrideredirect(True)
            myFrame = Frame(self.pinpop, bg="black")
            myFrame.pack()


            pinLbl = Label(myFrame, text="Enter Your Facial ATM pin and Withdrwal Amount", font=("Comic Sans MS", 12), bg="black", fg="white",
                                pady=10)
            pinLbl.grid(row=0, column=0,columnspan=2)

            withdrawlLbl = Label(myFrame, text="Withdrawl Amount :", font=("Comic Sans MS", 12), bg="black", fg="white",
                         pady=10)
            withdrawlLbl.grid(row=1, column=0)
            withdrawlEntry = Entry(myFrame, font=("Comic Sans MS", 12), bg="white",
                             fg="black")
            withdrawlEntry.grid(row=1, column=1, padx=10, pady=15)



            pLbl = Label(myFrame, text=" Facial ATM Pin :", font=("Comic Sans MS", 12), bg="black", fg="white",
                                pady=10)
            pLbl.grid(row=2, column=0)
            pinEntry = Entry(myFrame, font=("Comic Sans MS", 12), bg="white",
                                  fg="black")
            pinEntry.grid(row=2, column=1, padx=10, pady=15)




            cancelBtn = Button(myFrame, command=lambda: self.pinpop.destroy(), text="Cancel Transaction", bd=2,
                               font=("Comic Sans MS", 12), relief=RIDGE, bg="blue", fg="white", padx=0,
                               pady=0, width=15)
            cancelBtn.grid(row=3, column=0, sticky="ew")
            checkBtn = Button(myFrame,
                                command=lambda:self.pinMatchFunc(accNo,withdrawlEntry.get().strip(),pinEntry.get().strip(),balance,pin),
                              text="Confirm", bd=2,
                              font=("Comic Sans MS", 12), relief=RIDGE, bg="blue", fg="white", padx=0,
                              pady=0, width=10)
            checkBtn.grid(row=3, column=1, sticky="ew")
            checkBtn.bind("<Enter>", lambda id: checkBtn.config(bg="darkblue"))
            checkBtn.bind("<Leave>", lambda id: checkBtn.config(bg="blue"))
            cancelBtn.bind("<Enter>", lambda id: cancelBtn.config(bg="darkblue"))
            cancelBtn.bind("<Leave>", lambda id: cancelBtn.config(bg="blue"))

        # popDetails(accNo)
        # if(Yes){
        # amount and pin entering
        # Pin verification
        # if(ok){
        # balance minus and show balance with pop up
        # }
        # else
        # {
        # transaction fails
        # }
        # }else{
        # //Scan face again or try again
        # }
    def pinMatchFunc(self,accNo,amount,pin,dbBalance,dbPin):
        if(amount==""):
            messagebox.showerror("Amount", "Amount Can not be Empty")
            return
        else:
            regex = '^[0-9]+$'
            if ((re.search(regex, amount))):
                pass
            else:
                messagebox.showerror("Error", "Invalid Amount ! Please check it")
                return
        amount=int(amount)
        dbBalance=int(dbBalance)
        if(amount==0):
            messagebox.showerror("Amount", "Amount Can not be Zero")
            return
        if(pin==""):
            messagebox.showerror("Empty Pin","Pin can not be empty")
            return
        elif( not (re.search('^[0-9]+$', pin))):
            messagebox.showerror("Error", "Invalid Pin Number ! Please check it")
            return
        elif (int(pin)!=dbPin):
            self.pinpop.destroy()
            messagebox.showerror("Pin","Wrong Pin Entered...Transaction Aborted")
            return
        else:
            self.pinpop.destroy()
            if(dbBalance-amount<0):
                messagebox.showerror("Transaction cancelled","Transaction Cancelled due to Insufficient Funds in Your account")
                return
            else:
                newBalance=dbBalance-amount
                con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
                cur = con.cursor()
                cur.execute("update userdata set balance=" + str(newBalance) + " where accountNo='"+str(accNo)+"'")
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Withdrawl of "+str(amount)+" from Account No: "+str(accNo)+" is Successfull")
                return

    def takeInputsForDeposit(self,accountNoLock, accountNo):



        self.depositpop = Toplevel(self)
        self.depositpop.title("Deposit Money")
        self.depositpop.geometry("450x250+542+307")
        self.depositpop.config(bg="black")

        self.backgroundd11 = PhotoImage(file="View/mainBack.PNG")
        self.depositpop.resizable(False, False)
        label1 = Label(self.depositpop, image=self.backgroundd11)
        label1.place(x=0, y=0, relwidth=1, relheight=1)
        self.depositpop.overrideredirect(True)
        myFrame = Frame(self.depositpop, bg="black")
        myFrame.pack()

        pinLbl = Label(myFrame, text="Enter Your Details", font=("Comic Sans MS", 12),
                       bg="black", fg="white",
                       pady=10)
        pinLbl.grid(row=0, column=0, columnspan=2)

        accountNoLbl = Label(myFrame, text="Account No :", font=("Comic Sans MS", 12), bg="black", fg="white",
                             pady=10)
        accountNoLbl.grid(row=1, column=0)
        accountNoEntry = Entry(myFrame, font=("Comic Sans MS", 12), bg="white",
                               fg="black")
        accountNoEntry.grid(row=1, column=1, padx=10, pady=15)

        depositLbl = Label(myFrame, text=" Deposit Amount :", font=("Comic Sans MS", 12), bg="black", fg="white",
                           pady=10)
        depositLbl.grid(row=2, column=0)
        depositEntry = Entry(myFrame, font=("Comic Sans MS", 12), bg="white",
                             fg="black")
        depositEntry.grid(row=2, column=1, padx=10, pady=15)

        cancelBtn = Button(myFrame, command=lambda: self.depositpop.destroy(), text="Cancel Transaction", bd=2,
                           font=("Comic Sans MS", 12), relief=RIDGE, bg="blue", fg="white", padx=0,
                           pady=0, width=15)
        cancelBtn.grid(row=3, column=0, sticky="ew")
        confirmBtn = Button(myFrame,
                            command=lambda :self.depositAmountFunc(accountNoEntry.get().strip() if accountNo=="" else accountNo,depositEntry.get().strip()),
                            text="Confirm", bd=2,
                            font=("Comic Sans MS", 12), relief=RIDGE, bg="blue", fg="white", padx=0,
                            pady=0, width=10)
        confirmBtn.grid(row=3, column=1, sticky="ew")
        confirmBtn.bind("<Enter>", lambda id: confirmBtn.config(bg="darkblue"))
        confirmBtn.bind("<Leave>", lambda id: confirmBtn.config(bg="blue"))
        cancelBtn.bind("<Enter>", lambda id: cancelBtn.config(bg="darkblue"))
        cancelBtn.bind("<Leave>", lambda id: cancelBtn.config(bg="blue"))
        if (accountNoLock):
            accountNoEntry.delete(0,END)
            accountNoEntry.insert(0,accountNo)
            accountNoEntry.bind("<Key>", lambda e: "break")
            accountNoEntry.config(fg="grey")
    def depositFunc(self):
        print("depositFunc")
        result=messagebox.askquestion("Way to Deposit","Which id do you want to use for depositing money\nFor FaceID: CLick Yes\nFor Account No: CLick No",)
        global acNo
        if(result=="yes"):
            if (self.controller.ready == False):
                messagebox.showerror("No data", "Model trained without any data, Update Model")
                return

            acNo = getAccountNumberFromFace(self.controller.faceRecognizer)
            if (acNo == ""):
                return
            con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
            cur = con.cursor()
            cur.execute("select accountHolder from userdata where accountNo=" + acNo)
            data = cur.fetchall()
            con.commit()
            con.close()
            #if (len(data) != 1):
             #   messagebox.showerror("Wrong", "Something went Wrong")
              #  return
            accountHolder = data[0][0]
            resp = messagebox.askyesno("Account Confirmation",
                                       "Is this your Account: \nAccount Holder Name: " + accountHolder + "\nAccount Number: " + acNo)
            if not resp:
                return
            else:
                self.takeInputsForDeposit(True, acNo)
        else:
            self.takeInputsForDeposit(False,"")











    def balanceEnquiryFunc(self):
        print("balanceFunc")
        result = messagebox.askquestion("Way to Balance Enquiry",
                                        "Which id do you want to use for Balance Enquiry\nFor FaceID: CLick Yes\nFor Account No: CLick No", )
        global acNo
        if (result == "yes"):
            if (self.controller.ready == False):
                messagebox.showerror("No data", "Model trained without any data, Update Model")
                return

            acNo = getAccountNumberFromFace(self.controller.faceRecognizer)
            if (acNo == ""):
                return
            con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
            cur = con.cursor()
            cur.execute("select accountHolder from userdata where accountNo=" + acNo)
            data = cur.fetchall()
            con.commit()
            con.close()
            #if (len(data) != 1):
             #   messagebox.showerror("Wrong", "Something went Wrong")
              #  return
            accountHolder = data[0][0]
            resp = messagebox.askyesno("Account Confirmation",
                                       "Is this your Account: \nAccount Holder Name: " + accountHolder + "\nAccount Number: " + acNo)
            if not resp:
                return
            else:
                self.takeInputsForBalanceEnquiry(True, acNo)
        else:
            self.takeInputsForBalanceEnquiry(False, "")

    def takeInputsForBalanceEnquiry(self, accountNoLock, accountNo):

        self.bepop = Toplevel(self)
        self.bepop.title("Balance Enquiry")
        self.bepop.geometry("450x250+542+307")
        self.bepop.config(bg="black")

        self.backgroundd111 = PhotoImage(file="View/mainBack.PNG")
        self.bepop.resizable(False, False)
        label1 = Label(self.bepop, image=self.backgroundd111)
        label1.place(x=0, y=0, relwidth=1, relheight=1)
        self.bepop.overrideredirect(True)
        myFrame = Frame(self.bepop, bg="black")
        myFrame.pack()

        pinLbl = Label(myFrame, text="Enter Your Details", font=("Comic Sans MS", 12),
                       bg="black", fg="white",
                       pady=10)
        pinLbl.grid(row=0, column=0, columnspan=2)

        accountNoLbl = Label(myFrame, text="Account No :", font=("Comic Sans MS", 12), bg="black", fg="white",
                             pady=10)
        accountNoLbl.grid(row=1, column=0)
        accountNoEntry = Entry(myFrame, font=("Comic Sans MS", 12), bg="white",
                               fg="black")
        accountNoEntry.grid(row=1, column=1, padx=10, pady=15)

        pinnLbl = Label(myFrame, text=" Pin :", font=("Comic Sans MS", 12), bg="black", fg="white",
                           pady=10)
        pinnLbl.grid(row=2, column=0)
        pinnEntry = Entry(myFrame, font=("Comic Sans MS", 12), bg="white",
                             fg="black")
        pinnEntry.grid(row=2, column=1, padx=10, pady=15)

        cancelBtn = Button(myFrame, command=lambda: self.bepop.destroy(), text="Cancel Transaction", bd=2,
                           font=("Comic Sans MS", 12), relief=RIDGE, bg="blue", fg="white", padx=0,
                           pady=0, width=15)
        cancelBtn.grid(row=3, column=0, sticky="ew")
        confirmBtn = Button(myFrame,
                            command=lambda: self.balanceEnquiryFunc1(
                                accountNoEntry.get().strip() if accountNo == "" else accountNo,
                                pinnEntry.get().strip()),
                            text="Confirm", bd=2,
                            font=("Comic Sans MS", 12), relief=RIDGE, bg="blue", fg="white", padx=0,
                            pady=0, width=10)
        confirmBtn.grid(row=3, column=1, sticky="ew")
        confirmBtn.bind("<Enter>", lambda id: confirmBtn.config(bg="darkblue"))
        confirmBtn.bind("<Leave>", lambda id: confirmBtn.config(bg="blue"))
        cancelBtn.bind("<Enter>", lambda id: cancelBtn.config(bg="darkblue"))
        cancelBtn.bind("<Leave>", lambda id: cancelBtn.config(bg="blue"))
        if (accountNoLock):
            accountNoEntry.delete(0, END)
            accountNoEntry.insert(0, accountNo)
            accountNoEntry.bind("<Key>", lambda e: "break")
            accountNoEntry.config(fg="grey")

    def balanceEnquiryFunc1(self, accountNo, pin):
        if (accountNo == ""):
            messagebox.showerror("Failure", "Account number can not be empty")
            return
        else:
            regex = '^[0-9]+$'
            if ((re.search(regex, accountNo))):
                pass
            else:
                messagebox.showerror("Error", "Invalid Account Number ! Please check it")
                return
        con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
        cur = con.cursor()
        cur.execute("select balance,pin from userdata where accountNo=" + accountNo)
        con.commit()
        con.close()
        res = cur.fetchall()
        if (len(res) == 0):
            messagebox.showerror("Failure", "No account with this account no. exist")
            return
        else:
            currentbalance = int(res[0][0])
            db_pin=int(res[0][1])
            pin=int(pin.strip())
            print(str(pin)+"--"+str(db_pin))
            if(db_pin!=pin):
                messagebox.showerror("Error","Wrong Pin Entered")
                return
            else:
                messagebox.showinfo("Success", "Balance=" + str(currentbalance) + " in your account with Account No : " + str(
                accountNo) + "")
            return


    def pinFunc(self):
        print("pinFunc")
        if (self.controller.ready == False):
            messagebox.showerror("No data", "Model trained without any data, Update Model")
            return

        accNo = getAccountNumberFromFace(self.controller.faceRecognizer)

        if (accNo == ""):
            return

        con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
        cur = con.cursor()
        cur.execute("select accountHolder,pin from userdata where accountNo=" + accNo)
        data = cur.fetchall()

        con.commit()
        con.close()
        #if (len(data) != 1):
         #   messagebox.showerror("Wrong", "Something went Wrong")
         #   return
        accountHolder = data[0][0]
        pin = data[0][1]
        resp = messagebox.askyesno("Account Confirmation",
                                   "Is this your Account: \nAccount Holder Name: " + accountHolder + "\nAccount Number: " + accNo)
        if not resp:
            return
        else:
            self.pinChangepop = Toplevel(self)
            self.pinChangepop.title("Pin Change")
            self.pinChangepop.geometry("450x250+542+307")
            self.pinChangepop.config(bg="black")

            self.backgroundd1d = PhotoImage(file="View/mainBack.PNG")
            self.pinChangepop.resizable(False, False)
            # pop.attributes('-disabled', True)
            label1 = Label(self.pinChangepop, image=self.backgroundd1d)
            label1.place(x=0, y=0, relwidth=1, relheight=1)
            self.pinChangepop.overrideredirect(True)
            myFrame = Frame(self.pinChangepop, bg="black")
            myFrame.pack()

            pinLbl = Label(myFrame, text="Enter Your Details", font=("Comic Sans MS", 12),
                           bg="black", fg="white",
                           pady=10)
            pinLbl.grid(row=0, column=0, columnspan=2)

            oldPinLbl = Label(myFrame, text="Old Pin :", font=("Comic Sans MS", 12), bg="black", fg="white",
                                 pady=10)
            oldPinLbl.grid(row=1, column=0)
            oldPinEntry = Entry(myFrame, font=("Comic Sans MS", 12), bg="white",
                                   fg="black")
            oldPinEntry.grid(row=1, column=1, padx=10, pady=15)

            newPinLbl = Label(myFrame, text="New Pin :", font=("Comic Sans MS", 12), bg="black", fg="white",
                         pady=10)
            newPinLbl.grid(row=2, column=0)
            newPinEntry = Entry(myFrame, font=("Comic Sans MS", 12), bg="white",
                             fg="black")
            newPinEntry.grid(row=2, column=1, padx=10, pady=15)

            cancelBtn = Button(myFrame, command=lambda: self.pinChangepop.destroy(), text="Cancel Transaction", bd=2,
                               font=("Comic Sans MS", 12), relief=RIDGE, bg="blue", fg="white", padx=0,
                               pady=0, width=15)
            cancelBtn.grid(row=3, column=0, sticky="ew")
            checkBtn = Button(myFrame,
                              command=lambda: self.pinChangeFunc(accNo, oldPinEntry.get().strip(),pin,
                                                                newPinEntry.get().strip()),
                              text="Confirm", bd=2,
                              font=("Comic Sans MS", 12), relief=RIDGE, bg="blue", fg="white", padx=0,
                              pady=0, width=10)
            checkBtn.grid(row=3, column=1, sticky="ew")
            checkBtn.bind("<Enter>", lambda id: checkBtn.config(bg="darkblue"))
            checkBtn.bind("<Leave>", lambda id: checkBtn.config(bg="blue"))
            cancelBtn.bind("<Enter>", lambda id: cancelBtn.config(bg="darkblue"))
            cancelBtn.bind("<Leave>", lambda id: cancelBtn.config(bg="blue"))


    def adminFunc(self):
        print("adminFunc")
        self.pop=Toplevel(self)
        self.pop.title("Password Entry")
        self.pop.geometry("450x250+542+307")
        self.pop.config(bg="black")
        # self.pop.config(bd=2)

        self.backgroundd=PhotoImage(file="View/mainBack.PNG")
        self.pop.resizable(False, False)
        # pop.attributes('-disabled', True)
        label1 = Label(self.pop, image=self.backgroundd)
        label1.place(x=0, y=0, relwidth=1, relheight=1)
        self.pop.overrideredirect(True)
        myFrame = Frame(self.pop,bg="black")
        myFrame.pack()
        usernameLbl = Label(myFrame, text="Username :", font=("Comic Sans MS", 12), bg="black", fg="white",
                             pady=10)
        usernameLbl.grid(row=0, column=0)
        usernameEntry = Entry(myFrame, font=("Comic Sans MS", 12), bg="white",
                                    fg="black")
        usernameEntry.grid(row=0, column=1, padx=10,pady=15)

        passwordLbl = Label(myFrame, text="Password :", font=("Comic Sans MS", 12), bg="black", fg="white",
                            pady=10)
        passwordLbl.grid(row=1, column=0)
        passEntry = Entry(myFrame, font=("Comic Sans MS", 12), bg="white",
                                   fg="black")
        passEntry.grid(row=1, column=1, padx=10,pady=15)

        cancelBtn = Button(myFrame,command=lambda :self.pop.destroy(), text="Cancel", bd=2,
                                          font=("Comic Sans MS", 12), relief=RIDGE, bg="blue", fg="white", padx=0,
                                          pady=0, width=10)
        cancelBtn.grid(row=2, column=0,sticky="ew")
        loginBtn = Button(myFrame, command=lambda: self.confirmLogin(usernameEntry.get().strip(),passEntry.get().strip()),text="Login", bd=2,
                               font=("Comic Sans MS", 12), relief=RIDGE, bg="blue", fg="white", padx=0,
                               pady=0, width=10)
        loginBtn.grid(row=2, column=1, sticky="ew")
        loginBtn.bind("<Enter>", lambda id: loginBtn.config(bg="darkblue"))
        loginBtn.bind("<Leave>", lambda id: loginBtn.config(bg="blue"))
        cancelBtn.bind("<Enter>", lambda id:cancelBtn.config(bg="darkblue"))
        cancelBtn.bind("<Leave>", lambda id:cancelBtn.config(bg="blue"))



    def confirmLogin(self,username,password):
        con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
        cur = con.cursor()
        cur.execute("select * from adminCred limit 1")
        result=cur.fetchall()
        db_username=result[0][0].strip()
        db_password = result[0][1].strip()
        con.commit()
        con.close()
        if(username==db_username and password==db_password):
            self.pop.destroy()
            self.controller.showFrame(AdminPanel)
        else:
            messagebox.showwarning("Stop","Unauthorised User")
            return
    def transferFunc(self):
        print("transferFunc")
        result = messagebox.askquestion("Way to Transfer",
                                        "Which id do you want to use for transfering money\nFor FaceID: CLick Yes\nFor Account No: CLick No", )
        global acNo
        if (result == "yes"):
            if (self.controller.ready == False):
                messagebox.showerror("No data", "Model trained without any data, Update Model")
                return

            acNo = getAccountNumberFromFace(self.controller.faceRecognizer)
            if (acNo == ""):
                return
            con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
            cur = con.cursor()
            cur.execute("select accountHolder from userdata where accountNo=" + acNo)
            data = cur.fetchall()
            con.commit()
            con.close()
            #if (len(data) != 1):
             #   messagebox.showerror("Wrong", "Something went Wrong")
              #  return
            accountHolder = data[0][0]
            resp = messagebox.askyesno("Account Confirmation",
                                       "Is this your Account: \nAccount Holder Name: " + accountHolder + "\nAccount Number: " + acNo)
            if not resp:
                return
            else:
                self.takeInputsForTransfer(True, acNo)
        else:
            self.takeInputsForTransfer(False, "")

    def closeFunc(self):
        self.controller.destroy()
    #
    def depositAmountFunc(self, accountNo,amount):
        if(accountNo==""):
            messagebox.showerror("Failure","Account number can not be empty")
            return
        else:
            regex = '^[0-9]+$'
            if ((re.search(regex, accountNo))):
                pass
            else:
                messagebox.showerror("Error", "Invalid Account Number ! Please check it")
                return
        con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
        cur = con.cursor()
        cur.execute("select balance from userdata where accountNo="+accountNo)
        con.commit()
        con.close()
        res = cur.fetchall()
        if(len(res)==0):
            messagebox.showerror("Failure","No account with this account no. exist")
            return
        else:
            amount = int(amount)
            if(amount==0):
                messagebox.showerror("Failure", "Amount can not be zero")
                return

            currentbalance =int(res[0][0])
            newBalance = amount+currentbalance
            con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
            cur = con.cursor()


            cur.execute("update userdata set  balance="+str(newBalance)+" where accountNo='" + accountNo+"'")
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Amount="+str(amount)+" Deposited Successfully in Account No : "+str(accountNo)+"")
            return

    def pinChangeFunc(self, accNo, oldPin,dbPin, newPin):
        if(accNo==""):
            messagebox.showerror("Wrong","Something went Wrong")
            return
        else:
            regex = '^[0-9]+$'
            if ((re.search(regex, accNo))):
                pass
            else:
                messagebox.showerror("Error", "Invalid Account Number ! Please check it")
                return
        if(oldPin==""):
            messagebox.showerror("Wrong", "Old Pin can not be empty")
            return
        else:
            regex = '^[0-9]+$'
            if ((re.search(regex, oldPin))):
                pass
            else:
                messagebox.showerror("Error", "Invalid Old Pin Number ! Please check it")
                return
        if (newPin == ""):
            messagebox.showerror("Wrong", "New Pin can not be empty")
            return
        else:
            regex = '^[0-9]+$'
            if ((re.search(regex, newPin))):
                pass
            else:
                messagebox.showerror("Error", "Invalid New Pin Number ! Please check it")
                return
        oldPin=oldPin.strip()
        #dbPin=dbPin.strip()
        newPin=newPin.strip()

        if(int(oldPin)==int(dbPin)):
            con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
            cur = con.cursor()

            cur.execute("update userdata set pin="+newPin+" where accountNo=" + accNo)
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Pin has been changed Successfully")
            return


        else:
            messagebox.showerror("Wrong", "Old Pin does not match")
            return

    def takeInputsForTransfer(self,accountNoLock, accountNo):


        self.transferpop = Toplevel(self)
        self.transferpop.title("Deposit Money")
        self.transferpop.geometry("450x360+542+252")
        self.transferpop.config(bg="black")

        self.backgroundd1122 = PhotoImage(file="View/mainBack.PNG")
        self.transferpop.resizable(False, False)
        label1 = Label(self.transferpop, image=self.backgroundd1122)
        label1.place(x=0, y=0, relwidth=1, relheight=1)
        self.transferpop.overrideredirect(True)
        myFrame = Frame(self.transferpop, bg="black")
        myFrame.pack()

        pinLbl = Label(myFrame, text="Enter Your Details", font=("Comic Sans MS", 12),
                       bg="black", fg="white",
                       pady=10)
        pinLbl.grid(row=0, column=0, columnspan=2)

        accountNoLbl = Label(myFrame, text="Your Account No :", font=("Comic Sans MS", 12), bg="black", fg="white",
                             pady=10)
        accountNoLbl.grid(row=1, column=0)
        accountNoEntry = Entry(myFrame, font=("Comic Sans MS", 12), bg="white",
                               fg="black")
        accountNoEntry.grid(row=1, column=1, padx=10, pady=15)


        beniAccountNoLbl = Label(myFrame, text="Benificiary Account No :", font=("Comic Sans MS", 12), bg="black", fg="white",
                             pady=10)
        beniAccountNoLbl.grid(row=2, column=0)
        beniaccountNoEntry = Entry(myFrame, font=("Comic Sans MS", 12), bg="white",
                               fg="black")
        beniaccountNoEntry.grid(row=2, column=1, padx=10, pady=15)

        depositLbl = Label(myFrame, text="Deposit Amount :", font=("Comic Sans MS", 12), bg="black", fg="white",
                           pady=10)
        depositLbl.grid(row=3, column=0)
        depositEntry = Entry(myFrame, font=("Comic Sans MS", 12), bg="white",
                             fg="black")
        depositEntry.grid(row=3, column=1, padx=10, pady=15)
        PinLbl = Label(myFrame, text="Your Pin :", font=("Comic Sans MS", 12), bg="black", fg="white",
                           pady=10)
        PinLbl.grid(row=4, column=0)
        PinEntry = Entry(myFrame, font=("Comic Sans MS", 12), bg="white",
                             fg="black")
        PinEntry.grid(row=4, column=1, padx=10, pady=15)

        cancelBtn = Button(myFrame, command=lambda: self.transferpop.destroy(), text="Cancel Transaction", bd=2,
                           font=("Comic Sans MS", 12), relief=RIDGE, bg="blue", fg="white", padx=0,
                           pady=0, width=15)
        cancelBtn.grid(row=5, column=0, sticky="ew")
        transferBtn = Button(myFrame,
                            command=lambda :self.transferAmountFunc(accountNoEntry.get().strip() if accountNo=="" else accountNo.strip(),beniaccountNoEntry.get().strip(),depositEntry.get().strip(),PinEntry.get().strip()),
                            text="Transfer", bd=2,
                            font=("Comic Sans MS", 12), relief=RIDGE, bg="blue", fg="white", padx=0,
                            pady=0, width=10)
        transferBtn.grid(row=5, column=1, sticky="ew")
        transferBtn.bind("<Enter>", lambda id: transferBtn.config(bg="darkblue"))
        transferBtn.bind("<Leave>", lambda id: transferBtn.config(bg="blue"))
        cancelBtn.bind("<Enter>", lambda id: cancelBtn.config(bg="darkblue"))
        cancelBtn.bind("<Leave>", lambda id: cancelBtn.config(bg="blue"))
        if (accountNoLock):
            accountNoEntry.delete(0,END)
            accountNoEntry.insert(0,accountNo)
            accountNoEntry.bind("<Key>", lambda e: "break")
            accountNoEntry.config(fg="grey")

    def transferAmountFunc(self, senderAccNo, recieverAccNo, amount, pin):

        if(senderAccNo=="" or recieverAccNo==""):
            messagebox.showerror("Failure","Account no. can't ne empty")
            return
        else:
            regex = '^[0-9]+$'
            if ((re.search(regex, senderAccNo) and (re.search(regex,recieverAccNo)))):
                pass
            else:
                messagebox.showerror("Error", "Invalid Account Number ! Please check it")
                return

        if (amount==""):
            messagebox.showerror("Failure", "Amount can't be empty")
            return
        else:
            regex = '^[0-9]+$'
            if ((re.search(regex, amount))):
                pass
            else:
                messagebox.showerror("Error", "Invalid Amount ! Please check it")
                return

        amount = int(amount)

        if (amount == 0):
            messagebox.showerror("Amount", "Amount Can not be Zero")
            return

        con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
        cur = con.cursor()
        cur.execute("select pin,balance from userdata where accountNo='" + str(senderAccNo) + "'")
        res=cur.fetchall()
        con.commit()
        con.close()
        if len(res)==0:
            messagebox.showerror("Fail","Invalid Sender account no.")

        dbPin=res[0][0]
        dbBalance=res[0][1]

        if (pin == ""):
            messagebox.showerror("Empty Pin", "Pin can not be empty")
            return
        elif (not (re.search('^[0-9]+$', pin) )):
                messagebox.showerror("Error", "Invalid Pin Number ! Please check it")
                return
        elif (pin != dbPin):
            self.pinpop.destroy()
            messagebox.showerror("Pin", "Wrong Pin Entered...Transaction Aborted")
            return
        else:
            if (senderAccNo == recieverAccNo):
                messagebox.showerror("Failure", "Can not transfer to same account")
                return

            if (dbBalance - amount < 0):
                messagebox.showerror("Transaction cancelled",
                                     "Transaction Cancelled due to Insufficient Funds in Your account")
                return
            else:
                newBalance = dbBalance - amount
                con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
                cur = con.cursor()
                cur.execute("update userdata set balance=" + str(newBalance) + " where accountNo='" + str(senderAccNo) + "'")
                con.commit()
                con.close()

                # deposit Process
                con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
                cur = con.cursor()
                cur.execute("select balance from userdata where accountNo='" + str(recieverAccNo) + "'")
                reset=cur.fetchall()
                con.commit()
                con.close()
                if(len(reset)==1):
                    oldbal=reset[0][0]

                    con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
                    cur = con.cursor()
                    cur.execute("update userdata set balance=" + str(oldbal+amount) + " where accountNo='" + str(
                        recieverAccNo) + "'")
                    con.commit()
                    con.close()

                    messagebox.showinfo("Success", "Transer of " + str(amount) + " from Account No: " + str(
                    senderAccNo) + "to Account No: "+recieverAccNo+"  is Successfull")
                else:
                    messagebox.showerror("Fail","No reciever account number exist")
                    return


class AdminPanel(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        #  Background Image

        self.bg = PhotoImage(file="View/mainBack.PNG")

        label1 = Label(self, image=self.bg)
        label1.place(x=0, y=0, relwidth=1, relheight=1)

        title = Label(self, text="Facial ATM Admin Panel", bd=5, relief=GROOVE, font=("Comic Sans MS", 20), fg="white",
                      bg="#006daf")
        title.place(x=50, y=0, width=1440, height=50)
        self.closeImg = PhotoImage(file="View/close.png")
        self.close = Button(self, image=self.closeImg, command=self.closeFunc, bd=0)
        self.close.place(x=1500, y=10, width=30, height=30)
        self.backImg = PhotoImage(file="View/back.png")
        self.back = Button(self, image=self.backImg, bd=0, command=self.backFunc)
        self.back.place(x=10, y=10, width=30, height=30)

        self.trainBtn = Button(self, command=lambda :model.trainOurModel(self), text="Train Model", bd=4, font=("Comic Sans MS", 14),
                               relief=RIDGE, bg="blue", fg="white", padx=0, pady=0, width=11)
        self.trainBtn.place(x=10, y=60)
        self.changeAdminPassBtn = Button(self, text="Change Admin Password", bd=4, font=("Comic Sans MS", 14),
                               relief=RIDGE, bg="blue", fg="white", padx=0, pady=0, width=19,command=self.changeAdminPassFunc)
        self.changeAdminPassBtn.place(x=150, y=60)
        Manage_Frame = Frame(self, bd=4, relief=RIDGE, bg="Black", padx=0, pady=0)
        Manage_Frame.place(x=10, y=120, width=364.5, height=660)

        managaeTitle = Label(Manage_Frame, text="Account Management", font=("Comic Sans MS", 20), fg="white",
                             bg="#006daf", padx=0, pady=0)
        managaeTitle.grid(row=0, column=0, columnspan=2, sticky="we")
        #
        # # Account holder  name
        accHolderLbl = Label(Manage_Frame, text="Account Holder :", font=("Comic Sans MS", 12), bg="black", fg="white",
                             pady=10)
        accHolderLbl.grid(row=1, column=0)
        self.accHolderEntry = Entry(Manage_Frame, text="Account Holder", font=("Comic Sans MS", 12), bg="white",
                                    fg="black")
        self.accHolderEntry.grid(row=1, column=1, padx=10)

        # email
        emailLbl = Label(Manage_Frame, text="Email :", font=("Comic Sans MS", 12), bg="black",
                         fg="white", pady=15)
        emailLbl.grid(row=2, column=0)
        self.emailEntry = Entry(Manage_Frame, font=("Comic Sans MS", 12), bg="white",
                                fg="black")
        self.emailEntry.grid(row=2, column=1, padx=10)

        # # gender
        genderLbl = Label(Manage_Frame, text="Gender :", font=("Comic Sans MS", 12), bg="black",
                          fg="white", pady=10)
        genderLbl.grid(row=3, column=0)
        self.genderEntry = Entry(Manage_Frame, text="Male", font=("Comic Sans MS", 12), bg="white", fg="black")
        self.genderEntry.grid(row=3, column=1)

        self.genderEntry.insert(0, "Male/Female")
        self.genderEntry.bind("<Enter>",
                              lambda id: self.genderEntry.delete(0,
                                                                 END) if self.genderEntry.get() == "Male/Female" else "")

        self.genderEntry.bind("<Leave>", lambda id: self.genderEntry.insert(0,
                                                                            "Male/Female" if self.genderEntry.get() == "" else ""))
        #
        # # dob
        dobLbl = Label(Manage_Frame, text="Date of Birth :", font=("Comic Sans MS", 12), bg="black",
                       fg="white", pady=10)
        dobLbl.grid(row=4, column=0)
        self.dobEntry = Entry(Manage_Frame, font=("Comic Sans MS", 12), bg="white", fg="black", width=20)
        self.dobEntry.insert(0, "In form of 25/01/2022")
        self.dobEntry.bind("<Enter>", lambda id: self.dobEntry.delete(0,
                                                                      END) if self.dobEntry.get() == "In form of 25/01/2022" else "")

        self.dobEntry.bind("<Leave>", lambda id: self.dobEntry.insert(0,
                                                                      "In form of 25/01/2022" if self.dobEntry.get() == "" else ""))
        self.dobEntry.grid(row=4, column=1, padx=10)
        # # address
        addressLbl = Label(Manage_Frame, text="Address :", font=("Comic Sans MS", 12), bg="black",
                           fg="white", pady=10)
        addressLbl.grid(row=5, column=0)
        self.addressEntry = Text(Manage_Frame, font=("Comic Sans MS", 12), bg="white", fg="black", width=20, height=2)
        self.addressEntry.grid(row=5, column=1, padx=10)
        # # contact
        contactLbl = Label(Manage_Frame, text="Contact :", font=("Comic Sans MS", 12), bg="black",
                           fg="white", pady=10)
        contactLbl.grid(row=6, column=0)
        self.contactEntry = Entry(Manage_Frame, font=("Comic Sans MS", 12), bg="white", fg="black")
        self.contactEntry.grid(row=6, column=1, padx=10)

        

        # # account number generation
        accountNoLbl = Label(Manage_Frame, text="A/C No :", font=("Comic Sans MS", 12), bg="black",
                             fg="white", pady=10)
        accountNoLbl.grid(row=9, column=0)
        self.accountNoEntry = Entry(Manage_Frame, font=("Comic Sans MS", 12), bg="white", fg="black")
        self.accountNoEntry.grid(row=9, column=1, padx=10)
        self.accountNoEntry.bind("<Key>", lambda e: "break")
        self.generateAccoutNoBtn = Button(Manage_Frame, command=self.generateAccNoFunc, text="Generate A/C No.", bd=2,
                                          font=("Comic Sans MS", 12), relief=RIDGE, bg="blue", fg="white", padx=0,
                                          pady=0, width=16)
        self.generateAccoutNoBtn.grid(row=8, column=0, columnspan=2)
        #
        # # Face added - add new ,update
        faceLbl = Label(Manage_Frame, text="Face added :", font=("Comic Sans MS", 12), bg="black",
                        fg="white")
        faceLbl.grid(row=10, column=0)

        self.faceEntry = Entry(Manage_Frame, font=("Comic Sans MS", 12), bg="red", fg="white", width=10,
                               justify="center")

        self.faceEntry.insert(0, "Not Added")
        self.faceEntry.bind("<Key>", lambda e: "break")
        self.faceEntry.grid(row=10, column=1)
        #
        #
        self.addFaceBtn = Button(Manage_Frame, command=self.addOrUpdateFace, text="Add or Update Face", bd=2,
                                 font=("Comic Sans MS", 12), relief=RIDGE, bg="blue", fg="white", padx=0, pady=0)
        self.addFaceBtn.grid(row=11, column=0, pady=5, padx=0, columnspan=2)
        pinLbl = Label(Manage_Frame, text="4 digit Pin No :", font=("Comic Sans MS", 12), bg="black",
                       fg="white", pady=10)
        pinLbl.grid(row=12, column=0)
        self.pinNoEntry = Entry(Manage_Frame, font=("Comic Sans MS", 12), bg="white", fg="black")
        self.pinNoEntry.grid(row=12, column=1, padx=10)
        #
        #
        #
        ButtonFrame=Frame(Manage_Frame,bg="black")
        ButtonFrame.place(x=10, y=593,width=330)
        self.saveBtn = Button(ButtonFrame, text="Save All", bd=2, font=("Comic Sans MS", 15), relief=RIDGE, bg="Green",
                              fg="white", pady=0, width=7, command=self.saveAllFunc)
        self.saveBtn.grid(row=0,column=0,padx=5)
        self.deleteBtn = Button(ButtonFrame, text="Delete A/C", bd=2, font=("Comic Sans MS", 15), relief=RIDGE, bg="red",
                              fg="white", pady=0, width=9,command=self.deleteAccountFunc)
        self.deleteBtn.grid(row=0,column=1,padx=5)
        self.deleteBtn['state']=DISABLED
        self.clearBtn = Button(ButtonFrame, text="Clear", bd=2, font=("Comic Sans MS", 15), relief=RIDGE,
                                bg="blue",
                                fg="white", pady=0, width=7,command=self.clearToDefault)
        self.clearBtn.grid(row=0,column=2,padx=5)

        #

        # =================================================================================================
        Detail_Frame = Frame(self, bd=4, relief=RIDGE, bg="Black")
        Detail_Frame.place(x=381, y=60, width=1145, height=720)

        searchLbl = Label(Detail_Frame, text="Search By :", font=("Comic Sans MS", 12), bg="black",
                          fg="white", pady=10)
        searchLbl.grid(row=0, column=0, padx=20, pady=10)
        self.comboSearch = ttk.Combobox(Detail_Frame, width=10, font=('times', 13), state='readonly')
        self.comboSearch['values'] = ('A/c Number', 'Name', 'Contact', 'Date of Birth', 'Email')
        self.comboSearch.grid(row=0, column=1, padx=20, pady=10)
        self.searchEntry = Entry(Detail_Frame, font=("Comic Sans MS", 12), bg="white", fg="black", width=20,
                                 justify="center")
        self.searchEntry.grid(row=0, column=2)

        self.searchBtn = Button(Detail_Frame, text="Search", bd=2, font=("Comic Sans MS", 13), relief=RIDGE, bg="blue",
                                fg="white", pady=0, width=12,command=lambda :self.fetchDataWithCondition(self.comboSearch.get().strip(),self.searchEntry.get().strip()))
        self.searchBtn.grid(row=0, column=3, padx=20, pady=10)
        self.showAllBtn = Button(Detail_Frame, text="Show All", bd=2, font=("Comic Sans MS", 13), relief=RIDGE,
                                 bg="blue",
                                 fg="white", pady=0, width=12,command=self.fetchData)
        self.showAllBtn.grid(row=0, column=4, padx=20, pady=10)
        self.searchBtn.bind("<Enter>", lambda id: self.searchBtn.config(bg="darkblue"))
        self.searchBtn.bind("<Leave>", lambda id: self.searchBtn.config(bg="blue"))
        self.showAllBtn.bind("<Enter>", lambda id: self.showAllBtn.config(bg="darkblue"))
        self.showAllBtn.bind("<Leave>", lambda id: self.showAllBtn.config(bg="blue"))
        self.trainBtn.bind("<Enter>", lambda id: self.trainBtn.config(bg="darkblue"))
        self.trainBtn.bind("<Leave>", lambda id: self.trainBtn.config(bg="blue"))
        self.changeAdminPassBtn.bind("<Enter>", lambda id: self.changeAdminPassBtn.config(bg="darkblue"))
        self.changeAdminPassBtn.bind("<Leave>", lambda id: self.changeAdminPassBtn.config(bg="blue"))


        self.addFaceBtn.bind("<Enter>", lambda id: self.addFaceBtn.config(bg="darkblue"))
        self.addFaceBtn.bind("<Leave>", lambda id: self.addFaceBtn.config(bg="blue"))
        self.saveBtn.bind("<Enter>", lambda id: self.saveBtn.config(bg="darkgreen"))
        self.saveBtn.bind("<Leave>", lambda id: self.saveBtn.config(bg="green"))
        self.generateAccoutNoBtn.bind("<Enter>", lambda id: self.generateAccoutNoBtn.config(bg="darkblue"))
        self.generateAccoutNoBtn.bind("<Leave>", lambda id: self.generateAccoutNoBtn.config(bg="blue"))
        self.deleteBtn.bind("<Enter>", lambda id: self.deleteBtn.config(bg="darkred"))
        self.deleteBtn.bind("<Leave>", lambda id: self.deleteBtn.config(bg="red"))
        self.clearBtn.bind("<Enter>", lambda id: self.clearBtn.config(bg="darkblue"))
        self.clearBtn.bind("<Leave>", lambda id: self.clearBtn.config(bg="blue"))

        # Table Frame

        Table_Frame = Frame(Detail_Frame, bd=2, relief=RIDGE, bg="Black")
        Table_Frame.place(x=10, y=60, width=1115, height=645)
        scrollX = Scrollbar(Table_Frame, orient=HORIZONTAL)
        scrollY = Scrollbar(Table_Frame, orient=VERTICAL)
        self.dataTable = ttk.Treeview(Table_Frame, height=30, columns=(
        'Account Number', 'Account Holder', 'Email', 'Gender', 'Date of Birth', 'Address', 'Contact',
        'Face Id','Pin','Balance'), xscrollcommand=scrollX.set, yscrollcommand=scrollY.set)
        scrollX.pack(fill=X, side=BOTTOM)
        scrollY.pack(fill=Y, side=RIGHT)
        scrollX.config(command=self.dataTable.xview)
        scrollY.config(command=self.dataTable.yview)
        self.dataTable.heading('Account Number', text="Account Number")
        self.dataTable.heading('Account Holder', text="Account Holder")
        self.dataTable.heading('Email', text="Email")
        self.dataTable.heading('Gender', text="Gender")
        self.dataTable.heading('Date of Birth', text="Date of Birth")
        self.dataTable.heading('Address', text="Address")
        self.dataTable.heading('Contact', text="Contact")
        self.dataTable.heading('Face Id', text="Face Id")
        self.dataTable.heading('Pin', text="Pin")
        self.dataTable.heading('Balance', text="Balance")

        self.dataTable['show'] = 'headings'
        self.dataTable.column('Account Number', width=150,anchor=CENTER)
        self.dataTable.column('Account Holder', width=200,anchor=CENTER)
        self.dataTable.column('Email', width=350,anchor=CENTER)
        self.dataTable.column('Gender', width=100,anchor=CENTER)
        self.dataTable.column('Date of Birth', width=150,anchor=CENTER)
        self.dataTable.column('Address', width=400,anchor=CENTER)
        self.dataTable.column('Contact', width=100,anchor=CENTER)
        self.dataTable.column('Face Id', width=80,anchor=CENTER)
        self.dataTable.column('Pin', width=80, anchor=CENTER)
        self.dataTable.column('Balance', width=100, anchor=CENTER)
        self.dataTable.pack()
        self.dataTable.bind("<ButtonRelease-1>",self.selectRow)

        self.fetchData()

    def changeAdminPassFunc(self):
        self.adminpop = Toplevel(self)
        self.adminpop.title("Admin Password Change")
        self.adminpop.geometry("400x220+542+307")
        self.adminpop.config(bg="black")

        self.backgroundd12 = PhotoImage(file="View/mainBack.PNG")
        self.adminpop.resizable(False, False)
        # pop.attributes('-disabled', True)
        label1 = Label(self.adminpop, image=self.backgroundd12)
        label1.place(x=0, y=0, relwidth=1, relheight=1)
        self.adminpop.overrideredirect(True)
        myFrame = Frame(self.adminpop, bg="black")
        myFrame.pack()

        changeLbl = Label(myFrame, text="Change Admin Password ", font=("Comic Sans MS", 12),
                       bg="black", fg="white",
                       pady=10)
        changeLbl.grid(row=0, column=0, columnspan=2)

        oldPasslLbl = Label(myFrame, text="Old Password :", font=("Comic Sans MS", 12), bg="black", fg="white",
                             pady=10)
        oldPasslLbl.grid(row=1, column=0)
        oldPassEntry = Entry(myFrame, font=("Comic Sans MS", 12), bg="white",
                               fg="black")
        oldPassEntry.grid(row=1, column=1, padx=10, pady=15)

        newPassLbl = Label(myFrame, text=" New Password :", font=("Comic Sans MS", 12), bg="black", fg="white",
                     pady=10)
        newPassLbl.grid(row=2, column=0)
        newPassEntry = Entry(myFrame, font=("Comic Sans MS", 12), bg="white",
                         fg="black")
        newPassEntry.grid(row=2, column=1, padx=10, pady=15)

        cancelBtn = Button(myFrame, command=lambda: self.adminpop.destroy(), text="Cancel", bd=2,
                           font=("Comic Sans MS", 12), relief=RIDGE, bg="blue", fg="white", padx=0,
                           pady=0, width=10)
        cancelBtn.grid(row=3, column=0, sticky="ew",padx=10)
        changeBtn = Button(myFrame,
                          command=lambda: self.changeAdminPass(oldPassEntry.get().strip(),
                                                            newPassEntry.get().strip()),
                          text="Change Password", bd=2,
                          font=("Comic Sans MS", 12), relief=RIDGE, bg="blue", fg="white", padx=0,
                          pady=0, width=15)
        changeBtn.grid(row=3, column=1, sticky="ew",padx=10)
        cancelBtn.bind("<Enter>", lambda id: cancelBtn.config(bg="darkblue"))
        cancelBtn.bind("<Leave>", lambda id: cancelBtn.config(bg="blue"))
        changeBtn.bind("<Enter>", lambda id: changeBtn.config(bg="darkblue"))
        changeBtn.bind("<Leave>", lambda id: changeBtn.config(bg="blue"))

    def deleteAccountFunc(self):
        try:

            if (os.path.exists("data/" + self.accountNoEntry.get().strip())):
                for path,subdir,filenames in os.walk("data/" + self.accountNoEntry.get().strip()):
                    for filename in filenames:
                        os.remove(os.path.join(path,filename))
                os.rmdir("data/" + self.accountNoEntry.get().strip())
            con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
            cur = con.cursor()
            cur.execute("delete from userdata where accountNo=" + self.accountNoEntry.get().strip())
            con.commit()
            con.close()
            self.clearToDefault()
            self.fetchData()
            messagebox.showinfo("Success", "Account Deleted Successfully")
        except:
            messagebox.showinfo("Wrong", "Somthing Went Wrong")
            return


    def clearToDefault(self):
        self.clear()
        self.faceEntry.insert(0,"Not Added")
        self.dobEntry.insert(0, "In form of 25/01/2022")
        self.genderEntry.insert(0, "Male/Female")
        self.deleteBtn['state']=DISABLED
        self.faceEntry.config(bg="red")
    def fetchData(self):
        print("Fetching data")
        con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
        cur = con.cursor()

        cur.execute("select accountNo,accountHolder,email,gender,dateOfBirth,address,contact,faceAdded,pin,balance from userdata")
        rows=cur.fetchall()
        self.dataTable.delete(*self.dataTable.get_children())
        if len(rows)!=0:
            for row in rows:
                self.dataTable.insert("",END,values=row)
        con.commit()
        con.close()

    def fetchDataWithCondition(self,column,value):
        if(column==""):
            messagebox.showerror("Unsuccessfull Search","Please select valid Column for search")
            return
        if (value==""):
            messagebox.showerror("Unsuccessfull Search", "Please enter search paramater")
            return
        global query

        if(column=="A/c Number"):
            column="accountNo"
            query= "select accountNo,accountHolder,email,gender,dateOfBirth,address,contact,faceAdded,pin,balance from userdata where " + column.lower() + " = " + value + ""

        elif(column=="Date of Birth"):
            column="dateOfBirth"
            query = "select accountNo,accountHolder,email,gender,dateOfBirth,address,contact,faceAdded,pin,balance from userdata where " + column.lower() + " like '%" + value + "%'"

        elif(column=="Name"):
            column="accountHolder"
            query = "select accountNo,accountHolder,email,gender,dateOfBirth,address,contact,faceAdded,pin,balance from userdata where " + column.lower() + " like '%" + value + "%'"
        elif(column=="Email"):
            query = "select accountNo,accountHolder,email,gender,dateOfBirth,address,contact,faceAdded,pin,balance from userdata where " + column.lower() + " like '%" + value + "%'"
        elif(column=="Contact"):
            query = "select accountNo,accountHolder,email,gender,dateOfBirth,address,contact,faceAdded,pin,balance from userdata where " + column.lower() + " like '%" + value + "%'"

        print("Fetching data")
        con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
        cur = con.cursor()


        cur.execute(query)

        rows=cur.fetchall()
        if len(rows)>=0:
            self.dataTable.delete(*self.dataTable.get_children())
            if(len(rows)>0):
                for row in rows:
                    self.dataTable.insert("",END,values=row)
        con.commit()
        con.close()


    def closeFunc(self):
        # if any account not saved in Database and it has face id added then remove the facce id folder
        self.controller.destroy()

    def backFunc(self):
        # if any account not saved in Database and it has face id added then remove the facce id folder
        self.controller.showFrame(MainPanel)
    def selectRow(self,ev):
        cursorRow=self.dataTable.focus()
        contents=self.dataTable.item(cursorRow)
        row=contents['values']
        if(len(row)==0):
            return
        self.clear()
        self.deleteBtn['state'] = NORMAL
        self.setValues(row)
        self.faceEntry.config(bg="green")
        return
    def generateAccNoFunc(self):
        self.accountNo = self.accountNoEntry.get().strip()
        if(self.accountNo!="" and self.deleteBtn['state']==NORMAL):
            messagebox.showerror("Failed","You can not change your account number")
            return
        self.accountHolder = self.accHolderEntry.get().strip()
        self.gender = self.genderEntry.get().strip().capitalize()
        self.email = self.emailEntry.get().strip()
        self.dateOfBirth = self.dobEntry.get().strip()
        self.address = self.addressEntry.get("1.0", "end").strip()
        self.contact = self.contactEntry.get().strip()
        self.faceId = self.faceEntry.get().strip()


        if (self.accountHolder == ""):
            messagebox.showerror("Error", "Empty Account Holder Name! Please fill it first")
            return
        if (self.email == ""):
            messagebox.showerror("Error", "Empty Email! Please fill it first")
            return
        else:
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if ((re.search(regex, self.email))):
                pass
            else:
                messagebox.showerror("Error", "Invalid Email ! Please check it")
                return

        if (self.gender == "" or self.gender == "Male/Female"):
            messagebox.showerror("Error", "Empty Gender ! Please fill it first")
            return
        else:
            if (self.gender == "Male"):
                pass
            elif (self.gender == "Female"):
                pass
            else:
                messagebox.showerror("Error", "Invalid Gender! Please Check it")
                return

        if (self.dateOfBirth == "" or self.dateOfBirth == "In form of 25/01/2022"):
            messagebox.showerror("Error", "Empty Date of Birth! Please fill it first")
            return
        else:
            regex = '^[0-9]{2}[/][0-9]{2}[/][0-9]{4}$'
            if ((re.search(regex, self.dateOfBirth))):
                pass
            else:
                messagebox.showerror("Error", "Invalid Date Of Birth ! Please check it")
                return

        if (self.address == ""):
            messagebox.showerror("Error", "Empty Address! Please fill it first")
            return
        if (self.contact == ""):
            messagebox.showerror("Error", "Empty Contact No! Please fill it first")
            return
        else:
            regex = '^[0-9]{10}$'
            if ((re.search(regex, self.contact))):
                pass
            else:
                messagebox.showerror("Error", "Invalid Contact Number ! Please check it")
                return

        con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
        cur = con.cursor()

        cur.execute("select accountNo from userdata ORDER BY accountNo DESC LIMIT 1")
        res=cur.fetchall()
        noOfRows=100000
        if(len(res)!=0):
            noOfRows-=100000
            noOfRows+=res[0][0]
            noOfRows+=1

        if (self.accountNo == ""):
            self.accountNoEntry.insert(0, str(noOfRows))
        else:
            self.accountNoEntry.delete(0, END)
            self.accountNoEntry.insert(0, str(noOfRows))

        con.commit()
        con.close()

    def addOrUpdateFace(self):
        self.accountNo = self.accountNoEntry.get().strip()
        if (self.accountNo == ""):
            messagebox.showerror("Error", "Empty Account No! Generate Account Number First")
            return
        model.addFace(self.accountNo)
        self.faceEntry.config(bg="green")
        self.faceEntry.delete(0, END)
        self.faceEntry.insert(0, "Added")
    def clear(self):
        self.accountNoEntry.delete(0, END)
        self.accHolderEntry.delete(0, END)
        self.genderEntry.delete(0, END)
        self.emailEntry.delete(0, END)
        self.dobEntry.delete(0, END)
        self.addressEntry.delete(1.0, END)
        self.contactEntry.delete(0, END)
        self.faceEntry.delete(0, END)
        self.pinNoEntry.delete(0, END)

    def setValues(self,row):
        self.accountNoEntry.insert(0,row[0])
        self.accHolderEntry.insert(0, row[1])
        self.emailEntry.insert(0, row[2])
        self.genderEntry.insert(0, row[3])
        self.dobEntry.insert(0, row[4])
        self.addressEntry.insert(1.0, row[5])
        self.contactEntry.insert(0, row[6])
        self.faceEntry.insert(0, row[7])
        self.pinNoEntry.insert(0,row[8])

    def saveAllFunc(self):
        self.accountNo = self.accountNoEntry.get().strip()
        self.accountHolder = self.accHolderEntry.get().strip()
        self.gender = self.genderEntry.get().strip().capitalize()
        self.email = self.emailEntry.get().strip()
        self.dateOfBirth = self.dobEntry.get().strip()
        self.address = self.addressEntry.get("1.0", "end").strip()
        self.contact = self.contactEntry.get().strip()
        self.faceId = self.faceEntry.get().strip()
        self.pinNo = self.pinNoEntry.get().strip()

        if (self.accountHolder == ""):
            messagebox.showerror("Error", "Empty Account Holder Name! Please fill it first")
            return


        if (self.email == ""):
            messagebox.showerror("Error", "Empty Email! Please fill it first")
            return
        else:
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if ((re.search(regex, self.email))):
                pass
            else:
                messagebox.showerror("Error", "Invalid Email ! Please check it")
                return

        if (self.gender == "" or self.gender == "Male/Female"):
            messagebox.showerror("Error", "Empty Gender ! Please fill it first")
            return
        else:
            if (self.gender == "Male"):
                pass
            elif (self.gender == "Female"):
                pass
            else:
                messagebox.showerror("Error", "Invalid Gender! Please Check it")
                return

        if (self.dateOfBirth == "" or self.dateOfBirth == "In form of 25/01/2022"):
            messagebox.showerror("Error", "Empty Date of Birth! Please fill it first")
            return
        else:
            regex = '^[0-9]{2}[/][0-9]{2}[/][0-9]{4}$'
            if ((re.search(regex, self.dateOfBirth))):
                pass
            else:
                messagebox.showerror("Error", "Invalid Date Of Birth ! Please check it")
                return

        if (self.address == ""):
            messagebox.showerror("Error", "Empty Address! Please fill it first")
            return
        if (self.contact == ""):
            messagebox.showerror("Error", "Empty Contact No! Please fill it first")
            return
        else:
            regex = '^[0-9]{10}$'
            if ((re.search(regex, self.contact))):
                pass
            else:
                messagebox.showerror("Error", "Invalid Contact Number ! Please check it")
                return

        if (self.accountNo == ""):
            messagebox.showerror("Error", "Empty Account No! Generate Account Number First")
            return
        if (self.faceId == "Not Added"):
            messagebox.showerror("Error", "No Face Id added! Please add it first")
            return
        if (self.pinNo == ""):
            messagebox.showerror("Error", "Pin can't be empty! Please fill it first")
            return
        elif (len(self.pinNo) != 4):
            messagebox.showerror("Error", "Pin length must be 4 digit! Please write 4 digit pin")
            return
        regex = '^[0-9]{4}$'
        if ((re.search(regex, self.pinNo))):
            pass
        else:
            messagebox.showerror("Error", "Invalid Pin Entered! It should be numeric only")
            return

        con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
        cur = con.cursor()
        cur.execute("select * from userdata where accountNo="+self.accountNo)
        noOfRows=len(cur.fetchall())

        if(noOfRows==1):
            cur.execute("delete from userdata where accountNo=" + self.accountNoEntry.get().strip())
            con.commit()
        result=cur.execute("insert into Userdata values("+self.accountNo+",%s,%s,%s,%s,%s,%s,%s,%s,0)",(
        self.accountHolder,
        self.email,
        self.gender,
        self.dateOfBirth,
        self.address,
        self.contact,
        
        self.faceId,
        self.pinNo,
        ))

        con.commit()
        con.close()
        if(result==1):
            self.clearToDefault()
            self.fetchData()
            messagebox.showinfo("Success","Data Saved")


            return
        else:
            messagebox.showerror("Something Went Wrong", "Not able to Save Data ! PLease Try Again")
            self.clearToDefault()
            self.fetchData()
            return

    def changeAdminPass(self, oldpass,newpass):
        if(oldpass==""):
            messagebox.showerror("Wrong Credentials","Old password can not be empty")
            return
        if (newpass == ""):
            messagebox.showerror("Wrong Credentials", "New password can not be empty")
            return
        try:
            con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
            cur = con.cursor()
            cur.execute("select password from adminCred limit 1")
            result = cur.fetchall()
            db_password = result[0][0].strip()
            con.commit()
            con.close()
            if(db_password!=oldpass):
                messagebox.showerror("Password","Old Password does not Match")
                return
            con = pymysql.connect(host="localhost", user="root", password="", database="fatm")
            cur = con.cursor()
            cur.execute("update adminCred set password='"+newpass+"'")
            con.commit()
            con.close()
            messagebox.showinfo("Admin Password","Password Successfully changed")
            return
        except:
            messagebox.showerror("Admin Password", "Something Went Wrong")
            return



app = FATM()
app.mainloop()
