#main page file

#importing all of the necessary libraries aswell as the classes from other files 
from tkinter import *
from datetime import *
from calendar import *
import tkinter as tk
from PIL import Image,ImageTk
from auth import Login, Signup
from upload import UploadPage
from view import WardrobePage
from database import init_db
from outfit import DesignerPage
from calendarp import CalendarPage

#other pages will be imported later

#calling function in database.py that contain all of the tables created
init_db()

#creating the window for my app
root = Tk()
root.title("Virtual Wardrobe App")
root.geometry("500x500") 
root.configure(bg="#E3A869") #bgc for window
root.state("zoomed")

#initilaising all of the pages, usernames and ids to none so that every time app is reopen it resets
root.current_page = None
root.current_username = None
root.current_user_id = None

#header / menu bar creation
menu_bar_colour = "#8B1A1A"
menu_bar_frame = tk.Frame(root, bg=menu_bar_colour)
menu_bar_frame.pack(side="top", fill="x")
menu_bar_frame.pack_propagate(flag=False)
menu_bar_frame.configure(height=60)

#wardrobe image
wardrobe_img = Image.open("images/wardrobe_img.png")#load image
wardrobe_img = wardrobe_img.resize((60,50))
wardrobe_icon=ImageTk.PhotoImage(wardrobe_img)#converting image in tk
wardrobe_label = tk.Label(menu_bar_frame, image=wardrobe_icon, bg=menu_bar_colour, bd=0, activebackground=menu_bar_colour)
wardrobe_label.pack(side="left", padx=10, pady=5)

#virtual wardrobe title
root.vw_title_label = tk.Label(menu_bar_frame,bg=menu_bar_colour, text="Virtual Wardrobe", font=("Brush Script MT", 40, "bold"), fg="white")
root.vw_title_label.pack(side="left", padx=10)

#create icon for app
app_icon =PhotoImage(file="C:\\Users\\Isoken\\Desktop\\Virtual Wardrobe NEA\\images\\window_icon.png")
root.iconphoto(False, app_icon)


#function to change the header bar from saying 'virtual wardrobe' to the current users' username
def update_header():
    if root.current_username:
        root.vw_title_label.config(text=f"{root.current_username}'s Wardrobe")
    else:
        root.vw_title_label.config(text="Virtual Wardrobe")

root.update_header = update_header        

#tab buttons
tab_font = ("Brush Script MT", 15, "bold")
tab_buttons = {}
active_tab_colour = "#B4824C"
inactive_tab_colour = "#8B1A1A"

#function to show which page is currently in use by highlighting it as well as for when the user clicks on the tab for that page
def highlighted_tab(self):
    for text, btn in tab_buttons.items():
        if text == root.current_page:
            btn.config(bg=active_tab_colour, fg="black")
        else:
            btn.config(bg=inactive_tab_colour, fg="white")

root.highlighted_tab = highlighted_tab        

def create_tab_btn(text, page_class):
    #function that allows user to switch page to tab that they clicked on
    def switch_page():
        if page_class is not None:
            frame = frames[page_class]
            if hasattr(frame, "load_items"):
                frame.load_items()
            show_frame(page_class)
        root.current_page = text
        highlighted_tab()

    #design for all of the tabs
    btn = tk.Button(menu_bar_frame, text= text, font=tab_font, bg=inactive_tab_colour, fg="white",
                    activebackground=active_tab_colour, activeforeground="black", relief="sunken",padx=20, pady=5, command=switch_page)
    btn.pack(side="left", padx=25)

    tab_buttons[text]=btn
    return btn

#creating actual buttons
upload_btn = create_tab_btn("Upload", UploadPage)
wardrobe_btn = create_tab_btn("Wardrobe", WardrobePage)
calendar_btn = create_tab_btn("Calendar", CalendarPage)
designer_btn = create_tab_btn("Designer", DesignerPage)

#initially forgetting them becauyse they only appear once a user has logged in
upload_btn.pack_forget()
wardrobe_btn.pack_forget()
calendar_btn.pack_forget()
designer_btn.pack_forget()

#function to show tab buttons once user has logged in
def show_tab_btn():
    logout_btn.pack(side="left", padx=25)
    designer_btn.pack(side="right", padx=25)
    calendar_btn.pack(side="right", padx=25)
    wardrobe_btn.pack(side="right", padx=25)
    upload_btn.pack(side="right", padx=25)

root.show_tab_btn = show_tab_btn

#function that allows user to log out of their account by clicking on logout button
def logout():

    #clears curreent user info
    root.current_user_id = None
    root.current_username = None
    root.current_page = None

    #restes the header
    root.update_header()

    #hides the header tabs
    upload_btn.pack_forget()
    wardrobe_btn.pack_forget()
    calendar_btn.pack_forget()
    designer_btn.pack_forget()
    logout_btn.pack_forget()

    #returns back to login page
    show_frame(Login)

#creating frame for logout button
logout_frame = tk.Frame(root, bg="#E3A869")
logout_frame.pack(side="bottom", fill="x", padx=10, pady=10)

#creating the logout button
logout_btn = tk.Button(logout_frame, text="Logout", font=("Open Sans", 12, "bold"), bg=inactive_tab_colour, fg="white", activebackground=active_tab_colour, command=logout)
logout_btn.pack(side="left", padx=10)
logout_btn.pack_forget()


#create container to hold all frames
container = tk.Frame(root)
container.pack(side="top", fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

#create dictionary for frames 
frames = {}

#function that shows each page when it hs been called
def show_frame(frame_class):
    frame = frames[frame_class]
    frame.tkraise()

    if hasattr(frame, "called"):
        frame.called()

#creating frames
for F in (Login, Signup, UploadPage, WardrobePage, DesignerPage, CalendarPage):
    frame = F(container, show_frame)
    frames[F] = frame
    frame.grid(row=0, column=0, sticky=NSEW)

#first page to load when users open the app
show_frame(Login)    


#running the program
root.mainloop()


