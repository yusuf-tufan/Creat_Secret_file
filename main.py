from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import base64

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

#window
window=Tk()
window.title("The Scret Notes App")
window.state("zoomed")
window.config(bg='silver')

#image
img = Image.open("topsecretlogo.png")
resized=img.resize((150,150),Image.Resampling.LANCZOS)
itk=ImageTk.PhotoImage(resized)
lbl=Label(window,image=itk)
lbl.image=itk
lbl.pack(pady=(0,5))

#information
lbl_guide=Label(text='If you want to retrieve your secret notes:\n1) Just enter the file name,\n2) press GET,\n3) Enter the KEY and click Decrypt.',font=("Arial",10,'bold'),bg='brown',fg='white')
lbl_guide.pack(pady=(10,10))

#create file
def save_and_encypt():
    user_input_title=enter_title.get()
    user_input_text=text.get('1.0',END)
    user_key=enter_key.get()


    if len(user_input_title)==0 or len(user_input_text)==0 or len(user_key) == 0:
        messagebox.showinfo(title='Error',message='Please enter all info.')

    else:
        #encrypt
        message_encrypted = encode(user_key,user_input_text)

        try:
            with open(f'{user_input_title}.txt','a') as data_file:
                data_file.write(f'{message_encrypted}')
        except FileNotFoundError:
            with open(f'{user_input_title}.txt','w') as data_file:
                data_file.write(f'{message_encrypted}')
        finally:
            enter_title.delete(0,END)
            enter_key.delete(0,END)
            text.delete('1.0',END)

def decrypted_note():
    message_encrypted = text.get('1.0',END)

    password=passw_var.get()
    passw_var.set("")
    
    if len(message_encrypted) == 0 or len(password)==0:
        messagebox.showinfo(title='Error',message='Please enter all info.')

    else:
        try:
            decrypted_message = decode(password, message_encrypted)
            text.delete('1.0', END)
            text.insert('1.0', decrypted_message)
            
        except:
            messagebox.showinfo(title='Error',message='Please encrypted text')
        enter_key.delete(0,END)

def get_file():
    try:
        a=enter_title.get()
        text_file=open(f'{a}.txt','r')
        content=text_file.read()
        text.insert(END,content)
        text_file.close()
        btn_get.config(state='disabled')
    except:
        messagebox.showinfo(title='Error',message='Get True File!')
#show and hide password
def toggle_passsword():
    if enter_key.cget('show')=='*':
        enter_key.config(show='')
        btn_show_hide.config(text='Hide Password')
    else:
        enter_key.config(show='*')
        btn_show_hide.config(text='Show Password')  


def clear_all():
    text.delete(1.0,END)
    enter_key.delete(0,END)
    enter_title.delete(0,END)
    btn_get.config(state='active')
 
#title
title=Label(text='Enter Your File Name',font=("Arial",10,'bold'))
title.pack()

#enter title
enter_title=Entry(width=35)
enter_title.pack(pady=(0,10))

#text title
text_title=Label(text='Enter Your Secret Notes',font=("Arial",10,'bold'))
text_title.pack()

#enter text
text=Text(width=43,height=10)
text.config(font=("Arial",10,'italic'))
text.pack(pady=(0,20))

#title key
key_title=Label(text="Enter Master Key",font=("Arial",10,'bold'))
key_title.pack()
passw_var=StringVar()

#enter key
enter_key=Entry(width=15,textvariable=passw_var,show='*')
enter_key.pack()

#button of show/hide password
btn_show_hide=Button(text='Show Password',command=toggle_passsword)
btn_show_hide.pack(pady=(0,5))

#save & encrypt
save_encrypt=Button(text="Save & Encrypt",font=("Arial",10,'bold'),bg='light green',command=save_and_encypt)
save_encrypt.pack(pady=(5))

#clear the window
clear_button = Button(text="Clear ALL",bg='firebrick',fg='white',command=clear_all)
clear_button.pack()

#Get file
btn_get=Button(text='GET',command=get_file,font=("Arial",10,'bold'),bg='light green')
btn_get.pack(pady=5)

#decrypt
decrypt=Button(text="Decrypt",font=("Arial",10,'bold'),bg='light green',command=decrypted_note)
decrypt.pack(pady=(5))

#mainloop
window.mainloop()