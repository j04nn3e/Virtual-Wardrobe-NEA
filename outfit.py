import tkinter as tk
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk
from constants import CATEGORIES, COLOURS, SEASONS
from database import save_outfit
from tkinter import messagebox

main_bg = "#E3A869"
canvas_bg ="#F5F5DC"
wardrobe_panel_bg = "#8B1A1A"

class DesignerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=main_bg)

        #creating the outfit designer canvas
        self.outfit_frame = tk.Frame(self, bg=canvas_bg, relief="sunken", bd=3)
        self.outfit_frame.place(
            relx=0.32,
            rely=0.5,
            anchor="center",
            width=910,
            height=750
            )
        
        #text to tell user to create outfits
        self.outfit_label = tk.Label(self.outfit_frame,
                                     text="Create Your Outfit",
                                     bg=canvas_bg,
                                     fg=wardrobe_panel_bg,
                                     font=("Brush Script MT", 25, "bold")
                                     )
        self.outfit_label.pack(pady=10)

        #creating a frame for the outfits created 
        self.outfit_canvas = tk.Canvas(self.outfit_frame, bg=canvas_bg, highlightthickness=0)
        self.outfit_canvas.pack(side="left", fill="both", expand=True)

        outfit_scrollbar = ttk.Scrollbar(self.outfit_frame, orient="vertical", command=self.outfit_canvas.yview)
        outfit_scrollbar.pack(side="right", fill="y")

        self.outfit_canvas.configure(yscrollcommand=outfit_scrollbar.set)
    
        self.creation_frame = tk.Frame(self.outfit_canvas, bg=canvas_bg)
        self.creation_frame.config(width=910)
        self.outfit_canvas.create_window((455,0), window=self.creation_frame, anchor="center")

        self.creation_frame.bind("<Configure>", lambda e: self.outfit_canvas.configure(scrollregion=self.outfit_canvas.bbox("all")))
      
        #stack to track items
        self.outfit_items = []
        #tracking paths for items
        self.outfit_image_paths = []

        #ICON BUTTONS
        control_frame = tk.Frame(self.outfit_frame, bg=canvas_bg)
        control_frame.place(relx=0.95,rely=0.97, anchor="se")

        undo_img = Image.open("images/undo_icon.png").resize((30,30))
        self.undo_icon = ImageTk.PhotoImage(undo_img)

        clear_img = Image.open("images/bin_icon.png").resize((30,30))
        self.clear_icon = ImageTk.PhotoImage(clear_img)

        #BUTTONS IMAGE BASED
        undo_btn = tk.Button(control_frame, image=self.undo_icon, bg=canvas_bg, bd=0, command=self.undo_last_item)
        undo_btn.pack(side="right", padx=15)

        clear_btn = tk.Button(control_frame, image=self.clear_icon, bg=canvas_bg, bd=0, command=self.clear_outfit)
        clear_btn.pack(side="right", padx=15)

        #SAVE OUTFIT BUTTON
        save_btn = ttk.Button(control_frame, text="Save Outfit", command=self.save_outfit_function)
        save_btn.pack(side="right", padx=15)

        #wardrobe outfit panel
        self.panel_frame = tk.Frame(self, bg=wardrobe_panel_bg, relief="sunken", bd=3)
        self.panel_frame.place(
            relx=0.83,
            rely=0.5,
            anchor="center",
            width=460,
            height=750
        )

        #wardrobe panel label
        self.panel_label = tk.Label(
            self.panel_frame, text="Your Wardrobe",
            bg=wardrobe_panel_bg, fg=canvas_bg, font=("Brush Script MT", 25, "bold")
        )
        self.panel_label.pack(pady=10)


        #RECOMMENDATION BUTTON 
        ttk.Button(self.panel_frame, text="Recommend Items?",command=self.recommend_popup).pack(pady=10)

        #SHOW WARDOBE BUTTON
        ttk.Button(self.panel_frame, text="Show full Wardrobe", command=self.load_items).pack(pady=5)

        #scrollable canvas
        self.panel_canvas = tk.Canvas(self.panel_frame, bg=wardrobe_panel_bg, highlightthickness=0)
        self.panel_canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.panel_frame, orient="vertical", command=self.panel_canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.panel_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.item_frame = tk.Frame(self.panel_canvas, bg=wardrobe_panel_bg)
        self.panel_canvas.create_window((0,0), window=self.item_frame, anchor="nw")
        self.item_frame.bind("<Configure>", lambda e: self.panel_canvas.configure(scrollregion=self.panel_canvas.bbox("all")))

        self.image_refs = []
        self.load_items()
    
    #LOAD ITEM FUNCTION:
    def load_items(self):
        for widget in self.item_frame.winfo_children(): #returns list of all the child widgets inside the item frame
            widget.destroy()
        self.image_refs.clear()  #removes all stored images from the canvas
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        user_id = self.master.master.current_user_id
        cur.execute("SELECT image_path FROM Items WHERE user_id=?", (user_id,)) #retrives all the image paths values from the item table where the user id matches the currently logged in user
        paths = [row[0] for row in cur.fetchall()] 
        conn.close()

        self.show_items_from_query(recommended=False, recommended_paths=paths) #displays the fetched items to the canvas


    #RECOMMEND POPUP
    def recommend_popup(self):
        popup = tk.Toplevel(self, background=main_bg) #creates a neew popup
        popup.title("Recommend Items") #window title
        popup.geometry("400x400") #window size
        popup.grab_set() #means that user must close it before returning back to the main window

        #defaults value is all for each filter
        cat = tk.StringVar(value="All") 
        col = tk.StringVar(value="All") 
        sea = tk.StringVar(value="All") 

        ttk.Label(popup, text="Category", background=wardrobe_panel_bg, foreground="white").pack(pady=5) #create label category
        ttk.Combobox(popup, values=["All"] + CATEGORIES, textvariable=cat, state="readonly").pack()

        ttk.Label(popup, text="Colour", background=wardrobe_panel_bg, foreground="white").pack(pady=5)#create colour label
        ttk.Combobox(popup, values=["All"] + COLOURS, textvariable=col, state="readonly").pack()

        ttk.Label(popup, text="Season", background=wardrobe_panel_bg, foreground="white").pack(pady=5)#create season label
        ttk.Combobox(popup, values=["All"] + SEASONS, textvariable=sea, state="readonly").pack()

        #done button
        ttk.Button(popup, text="Done", command= lambda: self.recommend_items(cat.get(), col.get(), sea.get(), popup)).pack(pady=15)#gets current categoyr,colour and season selection and the popup window closes itself 

    #RECOMMEND FUNCTION

    def recommend_items(self, category, colour, season, popup):
        popup.destroy()#closes the popup window

        conn= sqlite3.connect("data.db")
        cur = conn.cursor()
        user_id = self.master.master.current_user_id #retrieves current logged in user id

        cur.execute("""SELECT image_path, category, colour, season FROM Items WHERE user_id=?""", (user_id,)) #select imagepath, colour, category, season for all items belonging to the current user

        scored = [] #initilaises scoring

        
        for path, cat, col, sea in cur.fetchall(): #loops though all fetched items
            score = 0 #starts with score of 0
            if category != "All" and cat == category: #add 1 point for each filter that matches and if the user didnt choose all and the item matches the selected category then add 1. same is done for colour and season
                score+= 1
            if colour != "All" and col == colour:
                score += 1
            if season != "All" and sea == season:
                score+= 1
            if score > 0: #if score greater than 0 then store trhe score and that image path in the scored list
                scored.append((score,path))

        conn.close()
        scored.sort(reverse=True) # sorts the list in dedescending order so that the best matches come firts
        top_items = [p for _, p in scored[:3]] #only takes the first 3 items from the sorted list and extracts their image paths values

        self.show_items_from_query(recommended=True, recommended_paths=top_items) #calls another method to displayt the top 3 recommended items

    def show_items_from_query(self, recommended=False, recommended_paths=None):
        #removes previous items
        for widget in self.item_frame.winfo_children():
            widget.destroy()
        self.image_refs.clear()

        paths = recommended_paths or [] # if recommended paths is not empty then paths will be that list else it will be an empty list

        row=0 #initilaises row to 0 to start at first row
        col=0 #initilaises column to 0 to start at first column

        if recommended: #if recommendd = true
            found_label = tk.Label(self.item_frame, text="Items that best match:", bg=wardrobe_panel_bg, fg=canvas_bg, font=("Open Sans", 15, "bold")) # display label message at top of the frame
            found_label.grid(row=row, column=0, columnspan=3, pady=(0,10)) # label spans across the 3 columns
            row=1 # row is increases by 1 so that the images are placed below the label

        for image_path in paths: #iterates through the file path in paths
            try: 
                img = Image.open(image_path).resize((120,120)) #opens the image file from image paths and resizes it to 120x120 pixels
                tk_img = ImageTk.PhotoImage(img) #converts it ti a tkinter compatible image
                self.image_refs.append(tk_img) #stores it in image references so that there are no erroneous collections
            except: #if loading fails it will skip to the next image
                continue

            tk.Button(self.item_frame, image=tk_img, bg=wardrobe_panel_bg, bd=0, command=lambda p=image_path: self.add_to_outfit(p)).grid(row=row, column=col, padx=10, pady=10) #creates button with image in its contents, when clicked calls the addtooutfit function that passes the image file path

            col +=1 #moves to the next column
            if col == 3: # if 3 images have been placed then reset col to 0 and move onto next row
                col = 0
                row+=1    
    
                
    #OUTFIT FUNCTION
    def add_to_outfit(self, image_path):
        try:
            img = Image.open(image_path).resize((180,180)) #set image size to 180 width and height
            tk_img = ImageTk.PhotoImage(img) #display the image
        except:
            return

        wrapper = tk.Frame(self.creation_frame, bg=canvas_bg) #where the image will be placed between
        wrapper.pack(pady=10)

        label = tk.Label(wrapper, image=tk_img, bg=canvas_bg)
        label.image=tk_img
        label.pack(anchor="center")

        self.outfit_items.append(wrapper)
        self.outfit_image_paths.append(image_path)

    #FUNCTIONS FOR THE UNOD AND CLEAR ICON
    def undo_last_item(self):
        if self.outfit_items: #checks if there are any items in the outfititems list
            last_item = self.outfit_items.pop() #removes and returns that last widget in the list as in the way a stack is implemeneted
            last_item.destroy() #removes that widget from the canavs

    def clear_outfit(self):
        for item in self.outfit_items: #loops through all widgets in the outfit
            item.destroy() # removes each widget from the canvas
        self.outfit_items.clear()  #empties tge list that tracks the outfit widgets added to the canvas
        self.outfit_image_paths.clear() #empties the list of the image file paths for the outfits

    #FUNCTION OT SAVE ITEM TO DB
    def save_outfit_function(self): 
        if not self.outfit_image_paths: #if list of outfitimagepaths is empty then show a error popup
            messagebox.showerror("Error", "No items in outfit canvas to save.") 
            return #stop function so that it doesnt try to save an empty outfit

        user_id = self.master.master.current_user_id
        success=save_outfit(user_id, self.outfit_image_paths)  #calls seperate function to store outfit in       

        if success:
            messagebox.showinfo("Successful", "Outfit saved successfully!") #shows a syccess popup

            #clearing canvas
            self.clear_outfit() #removes all outfit items from the canvas
            self.outfit_image_paths.clear() #outfit is empty
        else:
            messagebox.showerror("Error", "Error saving outfit. Please try again.") #handles any failure or error that may occur
        


    


            
    

   
