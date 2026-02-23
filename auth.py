import tkinter as tk
from tkinter import *
import sqlite3
from PIL import Image,ImageTk
from tkinter import messagebox
from database import add_user, validate_user, get_user_id
from upload import UploadPage  



class Login(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E3A869")

        #title label
        label = tk.Label(self, 
                         text="Login Page", 
                         font=("Brush Script MT", 100, "bold"),
                         bg ="#E3A869"
                         )
        label.pack(pady=90) 

        entry_font = ("Open sans", 25, "bold")
        entry_width = 40
        label_width = 20

        #username entry
        username_frame = tk.Frame(self, bg="#E3A869")
        username_frame.pack(pady=10, padx=100, fill="x")

        username_label = tk.Label(username_frame, text="Username:", bg="#E3A869", font=entry_font, width=label_width, anchor="w")
        username_label.grid(row=0, column=0, sticky="w")

        self.username_entry = tk.Entry(username_frame, width=entry_width, font=entry_font, highlightthickness=2.4)
        self.username_entry.grid(row=0, column=1)
        
        #password entry
        password_frame = tk.Frame(self, bg="#E3A869")
        password_frame.pack(pady=26, padx=100, fill="x")

        password_label = tk.Label(password_frame, text="Password:", bg="#E3A869", font=entry_font, width=label_width, anchor="w")
        password_label.grid(row=0, column=0, sticky="w")

        self.password_entry = tk.Entry(password_frame, width=entry_width, font=entry_font, show="*", highlightthickness=2.4)
        self.password_entry.grid(row=0, column=1)

        #creating show and hiding toggles
        showpw_img = Image.open("images/showpw_icon.png").resize((40,40))
        hidepw_img = Image.open("images/hidepw_icon.png").resize((40,40))
        self.show_icon = ImageTk.PhotoImage(showpw_img)
        self.hide_icon = ImageTk.PhotoImage(hidepw_img)

        self.showing = False # password is set to be hidden
        self.toggle_button = tk.Button(password_frame, image=self.show_icon, relief=FLAT, bd=0, command=self.toggle_pw)
        self.toggle_button.grid(row=0,column=2,padx=30)

        #login button () make sure to add command
        login_button = tk.Button(self, text="Log in", width=18, anchor="center", bg="#8B1A1A",font=entry_font, overrelief=SUNKEN, command=lambda: self.handle_login(controller)) 
        login_button.pack(side="right",pady=13, padx=200)

        #signup button
        signup_link = tk.Label(self, text="Don't have an account? Sign up here.", fg="#8B3A3A", cursor="hand2", bg="#E3A869", font=("Arial", 20, "underline"))
        signup_link.pack(pady=130)
        signup_link.bind("<Button-1>", lambda e: controller(Signup))  


    def toggle_pw(self): #code for the toggle button interactivity
            if self.showing:
                self.password_entry.config(show="*")
                self.toggle_button.config(image=self.show_icon)
                self.showing=False

            else:
                self.password_entry.config(show="")
                self.toggle_button.config(image=self.hide_icon)
                self.showing = True   

    def handle_login(self, controller):
         username = self.username_entry.get()
         password = self.password_entry.get()

         #empty field validation
         if username == "" or password =="":
              messagebox.showerror("Error", "Please enter valid inputs.")
              return

         if validate_user(username, password):
              #gets the user id and stores it so other frames can access it
              user_id = get_user_id(username, password)
              self.master.master.current_user_id=user_id
              self.master.master.current_username = username
              self.master.master.update_header()
              self.master.master.show_tab_btn()
              controller(UploadPage)
              self.master.master.current_page = "Upload"
              self.master.master.highlighted_tab()
         else:
              messagebox.showerror("Error", "Invalid username or password.")
   

class Signup(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E3A869") #bgc

        # Wrapper frame to hold everything below the menu bar
        content_frame = tk.Frame(self, bg="#E3A869")
        content_frame.pack(expand=True)   # page is filled correctly with dynamic spacing

        #title label
        label = tk.Label(self, 
                         text="Signup Page", 
                         font=("Brush Script MT", 100, "bold"),
                         bg ="#E3A869"
                         )
        label.pack(pady=40) 

        entry_font = ("Open sans", 25, "bold")
        entry_width = 40
        label_width = 20

        #username entry
        username_frame = tk.Frame(self, bg="#E3A869")
        username_frame.pack(pady=4, padx=100, fill="x")

        username_label = tk.Label(username_frame, text="Username:", bg="#E3A869", font=entry_font, width=label_width, anchor="w")
        username_label.grid(row=0, column=0, sticky="w")

        self.username_entry = tk.Entry(username_frame, width=entry_width, font=entry_font, highlightthickness=2.4)
        self.username_entry.grid(row=0, column=1)
        
        #password entry
        password_frame = tk.Frame(self, bg="#E3A869")
        password_frame.pack(pady=13, padx=100, fill="x")

        password_label = tk.Label(password_frame, text="Password:", bg="#E3A869", font=entry_font, width=label_width, anchor="w")
        password_label.grid(row=0, column=0, sticky="w")

        self.password_entry = tk.Entry(password_frame, width=entry_width, font=entry_font, show="*", highlightthickness=2.4)
        self.password_entry.grid(row=0, column=1)

        #creating show and hiding toggles
        showpw_img = Image.open("images/showpw_icon.png").resize((40,40))
        hidepw_img = Image.open("images/hidepw_icon.png").resize((40,40))
        self.show_icon = ImageTk.PhotoImage(showpw_img)
        self.hide_icon = ImageTk.PhotoImage(hidepw_img)

        self.showing = False # password is set to be hidden
        self.toggle_button = tk.Button(password_frame, image=self.show_icon, relief=FLAT, bd=0, command=self.toggle_pw)
        self.toggle_button.grid(row=0,column=2,padx=30)
 
        #confim password entry
        confirmp_frame = tk.Frame(self, bg="#E3A869")
        confirmp_frame.pack(pady=9, padx=100, fill="x")

        confirmp_label = tk.Label(confirmp_frame, text="Confirm password:", bg="#E3A869", font=entry_font, width=label_width, anchor="w")
        confirmp_label.grid(row=0, column=0, sticky="w")

        self.confirmp_entry = tk.Entry(confirmp_frame, width=entry_width, font=entry_font, highlightthickness=2.4, show="*")
        self.confirmp_entry.grid(row=0, column=1)

        #signup button () 
        signup_button = tk.Button(self, text="Sign up", width=18, anchor="center", bg="#8B1A1A",font=entry_font, overrelief=SUNKEN, command=self.handle_signup) 
        signup_button.pack(side="right",pady=15, padx=200)

        #log in button
        login_link = tk.Label(self, text="Already have an account? Log in", fg="#8B3A3A", cursor="hand2", bg="#E3A869", font=("Arial", 20, "underline"))
        login_link.pack(pady=100, padx=150)
        login_link.bind("<Button-1>", lambda e: controller(Login))   

    def toggle_pw(self):
            if self.showing:
                self.password_entry.config(show="*")
                self.toggle_button.config(image=self.show_icon)
                self.showing=False

            else:
                self.password_entry.config(show="")
                self.toggle_button.config(image=self.hide_icon)
                self.showing = True         

#storing the details into the database
    def handle_signup(self):
         username = self.username_entry.get()
         password = self.password_entry.get()
         confirm_p = self.confirmp_entry.get()   

        #empty input validation 
         if username == "" or password =="" or confirm_p =="":
              messagebox.showerror("Error", "Please enter valid inputs.")

         success = add_user(username, password)
    
         if success:
              messagebox.showinfo("Account created successfully","Now go to log in page")
         else:
              messagebox.showerror("Error", "Username already exists") 

        # checking if the pw matches eachother
         if password != confirm_p:
              messagebox.showerror("Error!", "Password do not match.")    
              return
    
                

        




       
    
