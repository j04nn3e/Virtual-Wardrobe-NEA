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
    from constants import CATEGORIES, COLOURS, SEASONS
except ImportError:
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

        #toggle button/ switch between menu and close icon, REMEBER TO ADD COMMAND
        self.menu_button = tk.Button(self, image=self.menu_icon, bd=0, bg=canvas_bg, activebackground=canvas_bg, command=self.toggle_panel)
        self.menu_button.place(relx=0.94, rely=0.03)

        #creating the filter panel
        self.filter_panel = tk.Frame(self, bg=canvas_bg, width=250, height=750)
        self.filter_panel.place(x=1600, y=72)

        #search bar creation/  outside frame for now
        search_frame = tk.Frame(self.filter_panel, bg=canvas_bg, bd=1, relief="sunken")
        search_frame.pack(pady=5, padx=10, fill="x")

        self.search_entry = tk.Entry(search_frame, font=("Open Sans", 12), bd=0)
        self.search_entry.insert(0, "Search for item...")#placeholder text so user knows what entry box is for
        self.search_entry.config(fg="grey")
        self.search_entry.bind("<FocusIn>", lambda e: self.clear_placeholder())
        self.search_entry.bind("<FocusOut>", lambda e: self.add_placeholder())
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(5,0), pady=2)

        self.search_button = tk.Button(search_frame, image=self.search_icon, bd=0, bg=canvas_bg, command=self.search_items)
        self.search_button.pack(side="right", padx=5)
        self.search_button.bind("<Button-1>", lambda e: self.search_items())

        #sorting options
        tk.Label(self.filter_panel, text="Category:", bg=canvas_bg, fg="white", font=("Open Sans", 12)).pack(pady=(20,5))
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.filter_panel, textvariable=self.category_var)
        self.category_dropdown['values'] = ['All'] + CATEGORIES
        self.category_dropdown.current(0)
        self.category_dropdown.pack(pady=5, padx=10, fill="x")
        self.category_dropdown.bind("<<ComboboxSelected>>", lambda e: self.load_items())

        #sorting options
        tk.Label(self.filter_panel, text="Colour:", bg=canvas_bg, fg="white", font=("Open Sans", 12)).pack(pady=(20,5))
        self.colour_var = tk.StringVar()
        self.colour_dropdown = ttk.Combobox(self.filter_panel, textvariable=self.colour_var)
        self.colour_dropdown['values'] = ['All'] + COLOURS  
        self.colour_dropdown.current(0)
        self.colour_dropdown.pack(pady=5, padx=10, fill="x")
        self.colour_dropdown.bind("<<ComboboxSelected>>", lambda e: self.load_items())

        #sorting options
        tk.Label(self.filter_panel, text="Season:", bg=canvas_bg, fg="white", font=("Open Sans", 12)).pack(pady=(20,5))
        self.season_var = tk.StringVar()
        self.season_dropdown = ttk.Combobox(self.filter_panel, textvariable=self.season_var)
        self.season_dropdown['values'] = ['All'] + SEASONS
        self.season_dropdown.current(0)
        self.season_dropdown.pack(pady=5, padx=10, fill="x")
        self.season_dropdown.bind("<<ComboboxSelected>>", lambda e: self.load_items())
        
        #panel open status stes to false by default
        self.panel_open = False

        self.load_items()

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
    def clear_placeholder(self):
        if self.search_entry.get() == "Search for item...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="black")

    def add_placeholder(self):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search for item...")
            self.search_entry.config(fg="grey")  


    #function to search for item with search icon
    def search_items(self):
        self.load_items(search=self.search_entry.get())


    #showing items on canvas
    def load_items(self, search=""):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("data.db")    
        cur = conn.cursor()
        user_id = self.master.master.current_user_id

        query= "SELECT id, item_name, image_path, category, colour, season FROM Items WHERE user_id=?"
        params=[user_id]

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

        cur.execute(query, tuple(params))   
        items = cur.fetchall()
        conn.close()

        if not items:
            tk.Label(self.canvas_frame, text="No items uploaded.", bg=canvas_bg, fg=canvas_bg, font=("Open Sans", 15)).pack(pady=20)
            return
        
        row = 0
        col = 0
        
        for item_id, item_name, image_path, category, colour, season in items:
            box = tk.Frame(self.canvas_frame, bg=canvas_bg , padx=10, pady=10)
            box.grid(row=row, column=col, padx=20, pady=20)

            try:
                img = Image.open(image_path).resize((180,180))
                tk_img = ImageTk.PhotoImage(img)
            except:
                tk_img = None

            label_img = tk.Label(box, image=tk_img, bg=canvas_bg)
            label_img.image = tk_img
            label_img.pack()

            row_frame = tk.Frame(box, bg=canvas_bg)
            row_frame.pack(fill="x", pady=(5,0))

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
        confirm = messagebox.askyesno(
        "Confim Delete", 
        "Are you sure you want to delete this item?")
        if confirm:
            delete_item_db(item_id)
            self.load_items()
            
       
 
    
        

    
       
    