#importing all necessary libraries and functions or classes from other files
import tkinter as tk #imports tkinter library as tk alias for simplicity
from tkinter import * #importing everything from tkinter library
import sqlite3 #importuing the sqlite database
from PIL import Image,ImageTk #imports image, for opening,reszizing,manipulating images and imagetk,for converting images into a format that tkinter can display
from tkinter import messagebox #imports submodule for ready-made pop-up dialog boxes
from database import add_user, validate_user, get_user_id #imports these functions from the databsse.py file
from upload import UploadPage #imports uploadpage class from upload.py file  


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

        #making these as local variables so I dont have to keep rewriting them again as they are used a lot in this file
        entry_font = ("Open sans", 25, "bold")
        entry_width = 40
        label_width = 20

        #username entry creation
        username_frame = tk.Frame(self, bg="#E3A869") #creates a frame
        username_frame.pack(pady=10, padx=100, fill="x") #places the frame in the parent widget and changes it sizing
        username_label = tk.Label(username_frame, text="Username:", bg="#E3A869", font=entry_font, width=label_width, anchor="w") #creates a label widget for username
        username_label.grid(row=0, column=0, sticky="w") #position of the username label
        self.username_entry = tk.Entry(username_frame, width=entry_width, font=entry_font, highlightthickness=2.4) #creates the entry box widget for username
        self.username_entry.grid(row=0, column=1) #position of the entry widget for username
        
        #password entry creation
        password_frame = tk.Frame(self, bg="#E3A869") #creates a frame
        password_frame.pack(pady=26, padx=100, fill="x") #places the frame in the parent widget and changes it sizing
        password_label = tk.Label(password_frame, text="Password:", bg="#E3A869", font=entry_font, width=label_width, anchor="w") #creates a label for password
        password_label.grid(row=0, column=0, sticky="w") #position of the password label
        self.password_entry = tk.Entry(password_frame, width=entry_width, font=entry_font, show="*", highlightthickness=2.4) #creates entry box widget for password
        self.password_entry.grid(row=0, column=1) #position of the entry box widget for password

        #creating show and hiding toggles
        showpw_img = Image.open("images/showpw_icon.png").resize((40,40)) #use pillow library to open image file and resizes it
        hidepw_img = Image.open("images/hidepw_icon.png").resize((40,40)) #use pillow library to open image file and resize it 
        self.show_icon = ImageTk.PhotoImage(showpw_img) #coverts the pillow image into a tkinter compatiable image object so that it can be displayed in a tkinter widget
        self.hide_icon = ImageTk.PhotoImage(hidepw_img) #converts image into tkinter compatiable image object so that it can be displayed in a tkinter widget

        self.showing = False # password is set to be hidden
        self.toggle_button = tk.Button(password_frame, image=self.show_icon, relief=FLAT, bd=0, command=self.toggle_pw) #creates button inside the password frame
        self.toggle_button.grid(row=0,column=2,padx=30) #position of the toggle button icon

        #login button and commnad to link the button to its respective funtion
        login_button = tk.Button(self, text="Log in", width=18, anchor="center", bg="#8B1A1A",font=entry_font, overrelief=SUNKEN, command=lambda: self.handle_login(controller)) #creates button for login that calls the handlelogin method when clciked
        login_button.pack(side="right",pady=13, padx=200) #position of the login button 

        #signup button and command to link the button to its respective function
        signup_link = tk.Label(self, text="Don't have an account? Sign up here.", fg="#8B3A3A", cursor="hand2", bg="#E3A869", font=("Arial", 20, "underline")) #creates button for signup
        signup_link.pack(pady=130) #position of the signup link align with its parent container
        signup_link.bind("<Button-1>", lambda e: controller(Signup)) #connects the button to the signup function so that when click it is called


    def toggle_pw(self): #code for the toggle button interactivity
            if self.showing: #showing password by replacing toggle icon with open eye
                self.password_entry.config(show="*") #changes password so that it is masked with * characters
                self.toggle_button.config(image=self.show_icon) #changes button icon to open eye image indicating that clicking it will show the password
                self.showing=False #updates state flage to indicate password is now hidden
            else: # hiding password by replacing toggle button with the closed eye
                self.password_entry.config(show="") #removes masking so password text is fully visible
                self.toggle_button.config(image=self.hide_icon) # changes button icon to closed eye indicating that clicking it will hide password
                self.showing = True #updates state flag to indicate the passowrd is now visible

    #function for the login button that compares username and password inputted to values in database 
    def handle_login(self, controller): 
         username = self.username_entry.get() # retrieves the enetered username
         password = self.password_entry.get() #retrieves the enetered password

         #empty field validation
         if username == "" or password =="": #checks if either userrname or password field is empty
              messagebox.showerror("Error", "Please enter valid inputs.") #display an error dialog pop up
              return

    
         if validate_user(username, password):
              #gets the user id and stores it so other pages can access it
              user_id = get_user_id(username, password)
              self.master.master.current_user_id=user_id #sets userid to the the parent of logged in user id
              self.master.master.current_username = username #sets username to parent of logged in username
              self.master.master.update_header()#updates the header bar to the users' username
              self.master.master.show_tab_btn()#shows the tab buttons once the user has logged in
              controller(UploadPage)
              self.master.master.current_page = "Upload" #automatically transfers user to upload page once they have successfully logged in
              self.master.master.highlighted_tab() #highlight the tab for the page that the user is currently on
         else:
              messagebox.showerror("Error", "Invalid username or password.")#if password or username doesnt match values in database
   

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

        #username entry creation
        username_frame = tk.Frame(self, bg="#E3A869") #creates frame
        username_frame.pack(pady=4, padx=100, fill="x") #sizing of frame
        username_label = tk.Label(username_frame, text="Username:", bg="#E3A869", font=entry_font, width=label_width, anchor="w") #creates username label
        username_label.grid(row=0, column=0, sticky="w") #position of username label
        self.username_entry = tk.Entry(username_frame, width=entry_width, font=entry_font, highlightthickness=2.4) #creates an entry box for username
        self.username_entry.grid(row=0, column=1) #position of username entry box
        
        #password entry creation
        password_frame = tk.Frame(self, bg="#E3A869") #create frame
        password_frame.pack(pady=13, padx=100, fill="x") #sizing of frame
        password_label = tk.Label(password_frame, text="Password:", bg="#E3A869", font=entry_font, width=label_width, anchor="w") #password label
        password_label.grid(row=0, column=0, sticky="w") #position of password label
        self.password_entry = tk.Entry(password_frame, width=entry_width, font=entry_font, show="*", highlightthickness=2.4) #create entry box for password 
        self.password_entry.grid(row=0, column=1) #position for password entry box

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

    #function that hides/shows the toggle icon image 
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
         username = self.username_entry.get() #retrieves inputted username
         password = self.password_entry.get() #retrieves inputted password
         confirm_p = self.confirmp_entry.get() #retrieves inputted confirm password   

        #empty input validation 
         if username == "" or password =="" or confirm_p =="": #checks if username, password or confirm pw entry box is empty
              messagebox.showerror("Error", "Please enter valid inputs.") #if so outputs error pop up message

         success = add_user(username, password) #if it isnt then it sends it as parameters to success function
    
         if success: #if the success value from the function in database returns true
              messagebox.showinfo("Account created successfully","Now go to log in page") #success message
         else:
              messagebox.showerror("Error", "Username already exists") 

        # checking if the pw matches eachother
         if password != confirm_p:
              messagebox.showerror("Error!", "Password do not match.")    
              return
    
                

        




       
    
