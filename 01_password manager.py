from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
FONT_NAME = "Courier"
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_entry.delete(0, END)
    
    password_letters = [choice(letters) for i in range(randint(6, 8))]
    password_numbers = [choice(numbers) for i in range(randint(2, 4))]
    password_symbols = [choice(symbols) for i in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(text=password)
    password_copied_label.config(text="New password copied to clipboard!")
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = mail_userid_entry.get()
    password = password_entry.get()
    new_data = {website : {"email" : email, "password" : password,}}

    if len(website) < 4 or len(password) < 4 or len(email) < 4:
        messagebox.showerror(title="Incorrect Entries detected", message="You have entered some details incorrectly. Please try again.")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:       
            data.update(new_data)
            with open("data.json", "w") as data_file: 
                json.dump(data, data_file, indent=4)
        finally:    
            website_entry.delete(0, END)
            password_entry.delete(0, END)

def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found.")
    else:
        searched = {}
        for i in data:
            if i == website:
                searched = data[website]
            
        if len(searched) > 0:        
            messagebox.showinfo(title="Serach Results", message=f"Email : {searched['email']}\nPassword : {searched['password']}")
        else:
            messagebox.showerror(title="Search Results", message=f"No details of the {website} exists.")



# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=55, pady=55)

canvas = Canvas(height=200, width=200)
lock_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_image)
canvas.grid(row=0, column=1)

#labels
website_label = Label(text="Website :")
website_label.grid(row=1, column=0)

mail_userid_label = Label(text="Email/Username :")
mail_userid_label.grid(row=2, column=0)

password_label = Label(text="Password :")
password_label.grid(row=3, column=0)

password_copied_label = Label(text="")
password_copied_label.grid(row=5, column=1)

#info input
mail_userid_entry = Entry(width=52)
mail_userid_entry.insert(0, "abc123@gmail.com")
mail_userid_entry.grid(row=2, column=1, columnspan=2)

website_entry = Entry(width=33)
website_entry.grid(row=1, column=1)
website_entry.focus()

password_entry = Entry(width=33)
password_entry.grid(row=3, column=1)

#buttons
search_button = Button(text="Search Saved Info!", command=find_password)
search_button.grid(row=1, column=2)

gen_pass_button = Button(text="Generate Password", command=generate_password)
gen_pass_button.grid(row=3, column=2)

add_button = Button(text="Add", width=44, command=save)
add_button.grid(row=4, column=1, columnspan=2)


window.mainloop()