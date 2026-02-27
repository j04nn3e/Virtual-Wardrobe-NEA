#main page file

#importing all of the necessary libraries aswell as the classes and functions from other files 
from tkinter import * #importing everything from tkinter library
from datetime import * #importing everything from python built-in datetime module
from calendar import * #importing everything from python built-in calendar module
import tkinter as tk #imports tkinter giving it the alias of tk for simplicity when coding
from PIL import Image,ImageTk #imports image, for opening,reszizing,manipulating images and imagetk,for converting images into a format that tkinter can display
from auth import Login, Signup #imports the login and signup class from auth.py file
from upload import UploadPage #imports the uploadpage class from auth.py
from view import WardrobePage #imports the wardrobepage class from view.py
from database import init_db #imports initilaiser function from database.py file
from outfit import DesignerPage #imports designerpage class from outfit.py file
from calendarp import CalendarPage #imports calenderpage class from calendarp.py file 


#calling function in database.py that contain all of the tables created
init_db()

#creating the window for my app
root = Tk()
root.title("Virtual Wardrobe App")#name of the app
root.geometry("500x500") 
root.configure(bg="#E3A869") #background colour for window
root.state("zoomed")#as soon as users run the app they are on fully screen

#initilaising all of the pages, usernames and ids to none so that every time app is reopen it resets
root.current_page = None
root.current_username = None
root.current_user_id = None

#header / menu bar creation
menu_bar_colour = "#8B1A1A" #colour for the menu/header bar
menu_bar_frame = tk.Frame(root, bg=menu_bar_colour) #creating the menubar frame
menu_bar_frame.pack(side="top", fill="x") # positioning the menu bar
menu_bar_frame.pack_propagate(flag=False) #prevents the frame from resizing to fit its conents so frame size can be controlled manually
menu_bar_frame.configure(height=60) #setting the height of the menu bar

#wardrobe image
wardrobe_img = Image.open("images/wardrobe_img.png")#load image
wardrobe_img = wardrobe_img.resize((60,50))
wardrobe_icon=ImageTk.PhotoImage(wardrobe_img)#converting image in tk
wardrobe_label = tk.Label(menu_bar_frame, image=wardrobe_icon, bg=menu_bar_colour, bd=0, activebackground=menu_bar_colour) #creating the wardrobe label
wardrobe_label.pack(side="left", padx=10, pady=5) #positioning the wardrobe label

#virtual wardrobe title
root.vw_title_label = tk.Label(menu_bar_frame,bg=menu_bar_colour, text="Virtual Wardrobe", font=("Brush Script MT", 40, "bold"), fg="white") #creating wardrobe title label
root.vw_title_label.pack(side="left", padx=10) #positioning title on screen

#create icon for app
app_icon =PhotoImage(file="C:\\Users\\Isoken\\Desktop\\Virtual Wardrobe NEA\\images\\window_icon.png")#loads the image icon from given path
root.iconphoto(False, app_icon) #sets the window icon using iconphoto() which changes the icon to show in the taskbar and title bar of computers


#function to change the header bar from saying 'virtual wardrobe' to the current users' username
def update_header():
    if root.current_username: #stores current logged in username
        root.vw_title_label.config(text=f"{root.current_username}'s Wardrobe") #once user has logged in it will update the label of the header to show the usernames + wardrobe
    else:     
        root.vw_title_label.config(text="Virtual Wardrobe") #if there is no currnetly logged in user it will set the  label to the default text of 'virtual wardrobe'

root.update_header = update_header #running the function to actually updates the header name        

#tab buttons creation
tab_font = ("Brush Script MT", 15, "bold") #font for each of the tab buttons
tab_buttons = {} #dictonary to store the names of all of the tab buttons
active_tab_colour = "#B4824C" #colour of the tab button when no interactions is being made with it
inactive_tab_colour = "#8B1A1A" #tab button when users click on it

#function to show which page is currently in use by highlighting it as well as for when the user clicks on the tab for that page
def highlighted_tab(self): #
    for text, btn in tab_buttons.items(): #loops through eavh tab name its it correspodning button
        if text == root.current_page: #checks if this tab is the current page that the user is on
            btn.config(bg=active_tab_colour, fg="black") #if so it changes the colour of the tab so that is the active colour and then changes the text colour to black to match it
        else:
            btn.config(bg=inactive_tab_colour, fg="white") #if the user isnt on that page then the tab colour is set to default 

root.highlighted_tab = highlighted_tab #running the function above     


def create_tab_btn(text, page_class):
    #function that allows user to switch page to tab that they clicked on
    def switch_page(): #inner function that actuallly handles what happens when user clicks on tab to switch pages
        if page_class is not None: #check that there is a valid page to switch to
            frame = frames[page_class] #gets the frame from the frames dictionary
            if hasattr(frame, "load_items"): # checks if the frame has the method load items 
                frame.load_items() #loads the method if it exists
            show_frame(page_class) # function that displayed the selected page on screen
        root.current_page = text # stores the name of the currently active page
        highlighted_tab() #updates the tab so that the colour is the active colour

    #design for all of the tabs
    btn = tk.Button(menu_bar_frame, text= text, font=tab_font, bg=inactive_tab_colour, fg="white",
                    activebackground=active_tab_colour, activeforeground="black", relief="sunken",padx=20, pady=5, command=switch_page)
    btn.pack(side="left", padx=25) #position of the button

    #stores value of the button in tab button dictionary
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

#function to show tab buttons once user has logged in and positioning all of them in the right position
def show_tab_btn():
    logout_btn.pack(side="left", padx=25)
    designer_btn.pack(side="right", padx=25)
    calendar_btn.pack(side="right", padx=25)
    wardrobe_btn.pack(side="right", padx=25)
    upload_btn.pack(side="right", padx=25)

root.show_tab_btn = show_tab_btn #running the function to show the tab buttons

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
logout_frame.pack(side="bottom", fill="x", padx=10, pady=10) #position of the logout button

#creating the logout button
logout_btn = tk.Button(logout_frame, text="Logout", font=("Open Sans", 12, "bold"), bg=inactive_tab_colour, fg="white", activebackground=active_tab_colour, command=logout)
logout_btn.pack(side="left", padx=10) #position of the logout button
logout_btn.pack_forget() #hides logout button temporarliy so that it is only shown once user has logged into account


#container to hold all frames
container = tk.Frame(root) #creates a frame widget 
container.pack(side="top", fill="both", expand=True) # position of the frame widget and allows frame to take extra space with the expand attribute when window is resized
container.grid_rowconfigure(0, weight=1) # grid layout
container.grid_columnconfigure(0, weight=1) #column layout

#create dictionary for frames which are esentially the different pages
frames = {}

#function that shows each page when it hs been called
def show_frame(frame_class): #frameclass is an parameter
    frame = frames[frame_class] #retrives the frame object from the frame dictionary
    frame.tkraise() #brings the frame to the front so that it is displayed to the user

    if hasattr(frame, "called"): #checks if the frame object has a method named 'called'
        frame.called() #executes if the frame has that method

#creating frames
for F in (Login, Signup, UploadPage, WardrobePage, DesignerPage, CalendarPage): # loops through the page classes
    frame = F(container, show_frame) #creating an instance of the page class
    frames[F] = frame # stores the frame instance inside the frames dictionary so that it can be retrieved later
    frame.grid(row=0, column=0, sticky=NSEW) #places the frame in the container, makes the frame expand to fill entire cell in all direction

#first page to load when users open the app
show_frame(Login)    


#running the program
root.mainloop()


