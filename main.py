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
window.config(padx=10,pady=80)
window.minsize(500,600)
window.config(bg='white')


#image
img = Image.open("topsecretlogo.png")
resized=img.resize((150,150),Image.Resampling.LANCZOS)
itk=ImageTk.PhotoImage(resized)
lbl=Label(window,image=itk)
lbl.image=itk
lbl.pack()

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
    user_key =enter_key.get()

    if len(message_encrypted) == 0 or len(user_key)==0:
        messagebox.showinfo(title='Error',message='Please enter all info.')

    else:
        try:
            decrypted_message = decode(user_key, message_encrypted)
            text.delete('1.0', END)
            text.insert('1.0', decrypted_message)
        except:
            messagebox.showinfo(title='Error',message='Please encrypted text')

#title
title=Label(text='Enter Your File Name',font=("Arial",10,'bold'))
title.pack()

#enter title
enter_title=Entry(width=35)
enter_title.pack()

#text title
text_title=Label(text='Enter Your Secret Notes',font=("Arial",10,'bold'))
text_title.pack()

#enter text
text=Text(width=43,height=15)
text.config(font=("Arial",10,'italic'))
text.pack()

#title key
key_title=Label(text="Enter Master Key",font=("Arial",10,'bold'))
key_title.pack()

#enter key
enter_key=Entry(width=35)
enter_key.pack()

#save & encrypt
save_encrypt=Button(text="Save & Encrypt",font=("Arial",10,'bold'),command=save_and_encypt)

save_encrypt.pack()

#decrypt
decrypt=Button(text="Decrypt",font=("Arial",10,'bold'),command=decrypted_note)
decrypt.pack()


#mainloop
window.mainloop()