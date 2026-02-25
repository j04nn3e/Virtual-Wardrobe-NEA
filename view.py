import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
from database import delete_item_db
from constants import CATEGORIES, COLOURS,SEASONS

main_bg= "#E3A869"
canvas_bg= "#8B1A1A"
item_bg="#FCF5E5"

try:
    from constants import CATEGORIES, COLOURS, SEASONS #attempts to import the 3 variables from constant.py file
except ImportError: # if not then use the default values
    CATEGORIES = ["Accessory","Blazer", "Blouse", "Button shirt", "Cardigan", "Coat", 
                     "Dress","Hat", "Hoodie", "Jacket","Jeans", "Joggers", "Leggings", 
                     "Polo shirt", "Scarf", "Shoe", "Shorts", "Skirts", "Sweater", "Tops", 
                     "Trousers","T-shirt", "Others"]

    COLOURS=["Beige", "Black", "Blue", "Brown", "Cream", "Gold", "Green", "Grey", 
                 "Orange", "Pink", "Purple", "Red", "Silver", "White", "Yellow", "Others"]

    SEASONS=["Autumn", "Winter", "Spring", "Summer"]




class WardrobePage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg=main_bg)
        self.controller = controller

        #delete button
        delete_img = Image.open("images/delete_icon.png").resize((40,40))
        self.delete_icon = ImageTk.PhotoImage(delete_img)

        #centre box
        self.centre_frame = tk.Frame(self, bg=canvas_bg, relief="sunken", bd=4)
        self.centre_frame.place(relx=0.40, rely=0.5, anchor="center", width=1150, height=750)

        #scrollable canvas
        self.canvas = tk.Canvas(self.centre_frame, bg=canvas_bg, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas_frame = tk.Frame(self.canvas, bg=canvas_bg)
        self.canvas.create_window((0,0), window=self.canvas_frame, anchor="nw")
        self.canvas_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        #filter drop down panel

        #creating the icons needed
        menu_img = Image.open("images/menu_icon.png").resize((40,40))
        self.menu_icon = ImageTk.PhotoImage(menu_img)
        close_img = Image.open("images/close_icon.png").resize((40,40))
        self.close_icon = ImageTk.PhotoImage(close_img)
        search_img = Image.open("images/search_icon.png").resize((30,30))
        self.search_icon = ImageTk.PhotoImage(search_img)

        #toggle button/ switch between menu and close icon
        self.menu_button = tk.Button(self, image=self.menu_icon, bd=0, bg=canvas_bg, activebackground=canvas_bg, command=self.toggle_panel)
        self.menu_button.place(relx=0.94, rely=0.03)

        #creating the filter panel
        self.filter_panel = tk.Frame(self, bg=canvas_bg, width=250, height=750)
        self.filter_panel.place(x=1600, y=72)

        #search bar creation/  outside frame for now
        search_frame = tk.Frame(self.filter_panel, bg=canvas_bg, bd=1, relief="sunken")
        search_frame.pack(pady=5, padx=10, fill="x")

        self.search_entry = tk.Entry(search_frame, font=("Open Sans", 12), bd=0) #creates a entry box inside the search frame
        self.search_entry.insert(0, "Search for item...")#placeholder text so user knows what entry box is for
        self.search_entry.config(fg="grey") #set placeholder colour to grey
        self.search_entry.bind("<FocusIn>", lambda e: self.clear_placeholder()) #binds events for placeholder
        self.search_entry.bind("<FocusOut>", lambda e: self.add_placeholder())
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(5,0), pady=2)#pack the entry into a frame, places the box on the left side of the search frame

        self.search_button = tk.Button(search_frame, image=self.search_icon, bd=0, bg=canvas_bg, command=self.search_items) #creates a clickavle button insude the search frame
        self.search_button.pack(side="right", padx=5) #position of the button
        self.search_button.bind("<Button-1>", lambda e: self.search_items()) #binds the event to trigger a search

        #sorting options for category
        tk.Label(self.filter_panel, text="Category:", bg=canvas_bg, fg="white", font=("Open Sans", 12)).pack(pady=(20,5)) #create a label for the dropdown
        self.category_var = tk.StringVar() #create a varibale to store the selected value
        self.category_dropdown = ttk.Combobox(self.filter_panel, textvariable=self.category_var) #creating the dropdown menu using ttk combobox
        self.category_dropdown['values'] = ['All'] + CATEGORIES # set the dropdown options to be the list of category name but with all as the first option
        self.category_dropdown.current(0) #sets the first option to be all by defualt
        self.category_dropdown.pack(pady=5, padx=10, fill="x") #places the dropdown in the panel
        self.category_dropdown.bind("<<ComboboxSelected>>", lambda e: self.load_items())#binds the event to reload the items to only show the option

        #sorting options for colour(same code as the category but adjusted for colour)
        tk.Label(self.filter_panel, text="Colour:", bg=canvas_bg, fg="white", font=("Open Sans", 12)).pack(pady=(20,5))
        self.colour_var = tk.StringVar()
        self.colour_dropdown = ttk.Combobox(self.filter_panel, textvariable=self.colour_var)
        self.colour_dropdown['values'] = ['All'] + COLOURS  
        self.colour_dropdown.current(0)
        self.colour_dropdown.pack(pady=5, padx=10, fill="x")
        self.colour_dropdown.bind("<<ComboboxSelected>>", lambda e: self.load_items())

        #sorting options for season(same code as the category but adjusted for season)
        tk.Label(self.filter_panel, text="Season:", bg=canvas_bg, fg="white", font=("Open Sans", 12)).pack(pady=(20,5))
        self.season_var = tk.StringVar()
        self.season_dropdown = ttk.Combobox(self.filter_panel, textvariable=self.season_var)
        self.season_dropdown['values'] = ['All'] + SEASONS
        self.season_dropdown.current(0)
        self.season_dropdown.pack(pady=5, padx=10, fill="x")
        self.season_dropdown.bind("<<ComboboxSelected>>", lambda e: self.load_items())
        
        #panel open status stes to false by default
        self.panel_open = False

        self.load_items()#calls the load items function so that the canvas is displaying the images of the items saved onto database

    #function for toggling the panel
    def toggle_panel(self):
        if self.panel_open:
            self.filter_panel.place(x=1600, y=72) #off screen
            self.menu_button.config(image=self.menu_icon)
        else:
            self.filter_panel.place(x=1210, y=72) #on screen
            self.menu_button.config(image=self.close_icon)
        self.panel_open = not self.panel_open    


    #functions for placeholders
    def clear_placeholder(self): #removes the placeholder text when the user clicks into the search box
        if self.search_entry.get() == "Search for item...":
            self.search_entry.delete(0, tk.END) #clears the entry box
            self.search_entry.config(fg="black") #changes the text colour to black so the user input looks normal

    def add_placeholder(self):  #restores the placeholder text when the search box is empty
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search for item...") #adds placeholder text back
            self.search_entry.config(fg="grey")  #changes colour to grey to indicate that it is a placeholder


    #function to search for item with search icon
    def search_items(self):
        self.load_items(search=self.search_entry.get())


    #showing items on canvas
    def load_items(self, search=""):
        for widget in self.canvas_frame.winfo_children(): #loops through all widgets inside the canvas frame
            widget.destroy() #removes the widget from the canvas

        conn = sqlite3.connect("data.db")    
        cur = conn.cursor()
        user_id = self.master.master.current_user_id

        #selects item details from the item table only for the currently logged in user
        query= "SELECT id, item_name, image_path, category, colour, season FROM Items WHERE user_id=?" 
        params=[user_id] # list of search /query parameters

        #applying the filters for search and dropdown
        if self.category_var.get() != 'All':
            query += " AND category=?"
            params.append(self.category_var.get())

        if self.colour_var.get() != 'All':
            query += " AND colour=?"
            params.append(self.colour_var.get())

        if self.season_var.get() != 'All':
            query += " AND season=?"   
            params.append(self.season_var.get())

        if search:
            query += " AND item_name LIKE ?"
            params.append(f"%{search}%")      

        #runs the query with all filters applied, fetches all matching rows into items and closes the database connection
        cur.execute(query, tuple(params))   
        items = cur.fetchall()
        conn.close()

        #if no items match the filters, display a 'no items uploaded' message and stops           
        if not items:
            tk.Label(self.canvas_frame, text="No items uploaded.", bg=canvas_bg, fg=canvas_bg, font=("Open Sans", 15)).pack(pady=20)
            return
        
        row = 0
        col = 0
        
        #create a box for each item and places it in a grid layout
        for item_id, item_name, image_path, category, colour, season in items:
            box = tk.Frame(self.canvas_frame, bg=canvas_bg , padx=10, pady=10)
            box.grid(row=row, column=col, padx=20, pady=20)

            try: #opens the image from image path and resizes it to 180x180 pixles
                img = Image.open(image_path).resize((180,180))
                tk_img = ImageTk.PhotoImage(img)
            except: #if loaidng fails set the img to none
                tk_img = None

            #create a label to display the image and pack it into the box frame
            label_img = tk.Label(box, image=tk_img, bg=canvas_bg)
            label_img.image = tk_img
            label_img.pack()

            row_frame = tk.Frame(box, bg=canvas_bg)
            row_frame.pack(fill="x", pady=(5,0))

            #adds a lable showing the item name in bold
            name_label = tk.Label(row_frame, text=item_name, font=("Open Sans",16,"bold"), bg="white", fg=canvas_bg)
            name_label.pack(side="left")

            #creating the delete icon button
            delete_btn = tk.Button(row_frame, image=self.delete_icon, bg=canvas_bg, activebackground=canvas_bg, bd=0, highlightthickness=0,
                                   command=lambda iid=item_id: self.delete_item(iid))
            delete_btn.pack(side="right")

            col +=1
            if col == 4:
                col = 0
                row +=1

          

    def delete_item(self, item_id):
        confirm = messagebox.askyesno("Confim Delete", 
        "Are you sure you want to delete this item?") #opens a yes/no confirmation popup that returns true = yes and false= no
        if confirm:
            delete_item_db(item_id) #calls function that removes the item with the itemid from the database
            self.load_items() #reloads the canvas so that the deleted ietm is no longer shown
            
       
 
    
        

    
       
    