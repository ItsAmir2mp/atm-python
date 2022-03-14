from tkinter import *
from tkinter import messagebox
import json
from tkinter import ttk
from PIL import Image , ImageTk
#backend=================================
def login_function():
    global information ,file_name , id_sabt_shode , entry_id_card, img
    id_sabt_shode = entry_id_card.get()
    file_name = entry_id_card.get()
    file_name_for_photo = entry_id_card.get()
    file_name += '.json'
    # لود تصویر
    findimage =  file_name_for_photo + ".jpg"
    myimage = Image.open(findimage)
    myimage = myimage.resize((150,125), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(myimage)
    try:
        file = open(file_name, 'r')
        information = json.load(file)
        Label(tap_profile , text="Name :", bg="#F95700", fg="#FFFFFF" ,font=("bold" , 10)).place(x=30 , y=10)
        Label(tap_profile , text="Family :", bg="#F95700", fg="#FFFFFF" ,font=("bold" , 10)).place(x=26 , y=40)
        Label(tap_profile , text="Id :", bg="#F95700", fg="#FFFFFF" ,font=("bold" , 10)).place(x=55  , y=75)
        Label(tap_profile , text="Date :", bg="#F95700", fg="#FFFFFF" ,font=("bold" , 10)).place(x=40 , y = 105)
        Label(tap_profile , text=information["name"], bg="#F95700", fg="#FFFFFF" ,font=("bold" , 10)).place(x=80 , y=10)
        Label(tap_profile , text=information["family"], bg="#F95700", fg="#FFFFFF" ,font=("bold" , 10)).place(x=76 , y=40)
        Label(tap_profile , text=information["id"], bg="#F95700", fg="#FFFFFF" ,font=("bold" , 10)).place(x=80  , y=75)
        Label(tap_profile , text=information["date"], bg="#F95700", fg="#FFFFFF" ,font=("bold" , 10)).place(x=80 , y = 105)
        # استفاده تصویر
        Label(tap_profile , image=img).place(x=350, y=10)
        file.close()
        date = entry_date_y.get() + '/' + entry_date_m.get()
        if information['pin']==entry_pin.get() and information['date']==date:
            root.deiconify()
            login.destroy()
        else:
            messagebox.showerror('Wrong information', 'The data you entered is wrong!!!')
    except:
            messagebox.showerror('Card Error', 'This account does not exist!!!')
def cancel():
    a = messagebox.askyesno("EXIT" , "Are you sure?")
    if a == True:
        login.destroy()
    else:
        None
def balance():
    global information
    Label(tab_balance , text=information["amount"] , font=("bold" , 15), bg="#F95700", fg="#FFFFFF").place(x=260) 
def withdraw():
    global information, file_name ,combo_amount
    current_money = information['amount']
    if current_money-int(combo_amount.get()) >= 0:
        information['amount'] = current_money-int(combo_amount.get())
        file = open(file_name, 'w', encoding='utf-8')
        json.dump(information, file, indent=4, ensure_ascii=False)
        messagebox.showinfo('successful',
            f'Successfull withdraw\nNew Balance: {information["amount"]}')
        file.close()
    else:
        messagebox.showwarning("ERROR",'Not enough money!')
        
def transfer():
    global information, file_name , entry_amount , entry_id_card
    current_money = information['amount']
    x = entry_amount.get()
    if x.isdigit():

        if entry_destination.get() != id_sabt_shode:
            if current_money-int(entry_amount.get()) >= 0 and int(entry_amount.get()) > 0:
                try:
                    file_name2 = entry_destination.get()
                    file_name2 += '.json'
                    file2 = open(file_name2, 'r')
                    information2 = json.load(file2)
                    file2.close()
                    information['amount'] = current_money-int(entry_amount.get())
                    file = open(file_name, 'w', encoding='utf-8')
                    json.dump(information, file, indent=4, ensure_ascii=False)
                    file.close()
                    temp = information2['amount'] + int(entry_amount.get())
                    file2 = open(file_name2, 'w', encoding='utf-8')
                    information2['amount'] = temp
                    json.dump(information2, file2, indent=4, ensure_ascii=False)
                    file2.close()
                    m = f'Transfer from {information["id"]} to {information2["name"]} {information2["family"]} Succesful.\nBalance {information["amount"]}'
                    messagebox.showinfo('successful', m)
                    entry_amount.delete(0 , END)
                    entry_destination.delete(0 ,END)
                except:
                    messagebox.showerror('CARD ERROR', 'Destination does not exist!!!')
            else:
                messagebox.showwarning('ERROR','Not enough money or wrong amount')
        else:
            messagebox.showwarning('ERROR','Destination is not valid!!!')
    else:
            messagebox.showwarning('ERROR','only use numbers!')
def change_pin():
    global information, file_name
    if old_pin.get() == information['pin']:
        my_new_pin = new_pin.get()
        if my_new_pin.isdigit():
            if new_pin.get() == repeat_new_pin.get():
                information['pin'] = new_pin.get()
                file = open(file_name, 'w', encoding='utf-8')
                json.dump(information, file, indent=4, ensure_ascii=False)
                messagebox.showinfo('Pin change', 'Pin Successfully changed!!!')
                file.close()           
                ent_oldpin.delete(0 , END)
                ent_newpi.delete(0 , END)
                ent_rep.delete(0 , END)
            else:
                messagebox.showerror('Conflict',
                        'New pin and repetetion does not match!')
        else:
            messagebox.showwarning('PIN ERROR','only use numbers!')
    else:
        messagebox.showerror('PIN ERROR', 'Old pin is wrong!!!')
#page========================================
root = Tk()
root.resizable(0,0)
root.title("Main Page")
login = Toplevel(root)
login.geometry('200x200')
login.resizable(0,0)
root.geometry("550x200")
login.title("login")
login.configure(bg="#F95700")
root.withdraw()
my_notebook = ttk.Notebook(root)
tab_transfer = Frame(my_notebook , bg="#F95700")
tab_balance = Frame(my_notebook, bg="#F95700")
tab_changepin = Frame(my_notebook, bg="#F95700")
tab_withdraw = Frame(my_notebook, bg="#F95700")
tap_profile =  Frame(my_notebook, bg="#F95700")
entry_amount = Entry(tab_transfer)
my_notebook.add(tab_transfer ,text="Transfer")
my_notebook.add(tab_balance,text="Balance")
my_notebook.add(tab_changepin,text="Change Pin")
my_notebook.add(tab_withdraw,text="Withdraw")
my_notebook.add(tap_profile,text="Profile")
my_notebook.pack(fill="both" , expand=1)
vals = [20000, 50000, 80000, 100000, 150000, 200000]    
combo_amount = ttk.Combobox(tab_withdraw, values=vals, state='readonly')
combo_amount.place(x=170 , y=50)
Label(tab_changepin, text='Old pin: ' , bg="#F95700", fg="#FFFFFF").place(x=120 , y=10)
Label(tab_changepin, text='New pin: ', bg="#F95700", fg="#FFFFFF").place(x=116 , y=40)
Label(tab_changepin, text='Repeat new pin: ', bg="#F95700", fg="#FFFFFF").place(x=80 , y=70)
old_pin = StringVar()
new_pin = StringVar()
repeat_new_pin = StringVar()
ent_oldpin = Entry(tab_changepin, textvariable=old_pin)
ent_oldpin.place(x=170 , y=10)
ent_newpi = Entry(tab_changepin, textvariable=new_pin)
ent_newpi.place(x=170 , y=40)
ent_rep = Entry(tab_changepin, textvariable=repeat_new_pin)
ent_rep.place(x=170 , y=70)
Button(tab_changepin, text='Change Pin', command=change_pin, fg="#F95700" , bg="#FFFFFF",bd=1).place(x=195 , y=100)
Label(tab_withdraw, text='Amount : ', bg="#F95700", fg="#FFFFFF").place(x=110 , y=50)
Button(tab_withdraw, text='Withdraw', command=withdraw ,fg="#F95700", bg="#FFFFFF").place(x=210 , y=100)
Label(tab_balance , text="Your Balance Is :" , font=("bold" , 15), bg="#F95700", fg="#FFFFFF").place(x=100)
Label(tab_transfer, text='Amount : ',bg="#F95700", fg="#FFFFFF").place(x=110 , y=10)
Label(tab_transfer, text='To : ',bg="#F95700", fg="#FFFFFF").place(x=140 , y=40)
entry_destination = Entry(tab_transfer)
entry_amount.place(x=175 , y=10)
entry_destination.place(x=175 , y=40)
#label========================================
lbl_id_card = Label(login, text='ID CARD :' , bg="#F95700" , fg="#FFFFFF")
lbl_pin = Label(login, text='PIN :' ,bg="#F95700", fg="#FFFFFF")
lbl_date_y = Label(login , text="Y :" ,bg="#F95700", fg="#FFFFFF")
lbl_date_m = Label(login , text="M :" ,bg="#F95700", fg="#FFFFFF")
#Entry========================================
entry_pin = Entry(login, show="*")
entry_id_card = Entry(login , show="*")
entry_date_y = Entry(login, show="*")
entry_date_m = Entry(login, show="*")
#Button========================================
btn_ok = Button(login, text='OK', command=login_function,bg="#FFFFFF", fg="#F95700" , activeforeground="#F95700" ,border=0.1 ,bd=1)
btn_cancel = Button(login, text='Cancel', command=cancel,bg="#FFFFFF", fg="#F95700", activeforeground="#F95700",border=1)
btn_balance = Button(tab_balance, text='Balance', command=balance,bg="#FFFFFF", bd=1,fg="#F95700").place(x=175, y=60)
btn_transfer = Button(tab_transfer, text='Transfer', command=transfer,fg="#F95700", bg="#FFFFFF").place(x=210 , y=80)
#grid=========================================== 
entry_pin.place(x=60, y=50)
entry_date_y.place(x=60, y=80 , width=25)
entry_date_m.place(x=125, y=80 , width=25)
entry_id_card.place(x=60, y=20)
lbl_id_card.place(x=0 , y=20)
lbl_pin.place(x=25 , y=50)
lbl_date_y.place(x=35 , y=80)
lbl_date_m.place(x=100 , y=80)
btn_cancel.place(x=40 , y=130 , width=45)
btn_ok.place(x=125 , y=130, width=45)

mainloop()