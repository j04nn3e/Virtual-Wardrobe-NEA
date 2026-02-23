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
        for widget in self.item_frame.winfo_children():
            widget.destroy()
        self.image_refs.clear()    
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        user_id = self.master.master.current_user_id
        cur.execute("SELECT image_path FROM Items WHERE user_id=?", (user_id,))
        paths = [row[0] for row in cur.fetchall()]
        conn.close()

        self.show_items_from_query(recommended=False, recommended_paths=paths)


    #RECOMMEND POPUP
    def recommend_popup(self):
        popup = tk.Toplevel(self, background=main_bg)
        popup.title("Recommend Items")
        popup.geometry("400x400")
        popup.grab_set()   

        cat = tk.StringVar(value="All") 
        col = tk.StringVar(value="All") 
        sea = tk.StringVar(value="All") 

        ttk.Label(popup, text="Category", background=wardrobe_panel_bg, foreground="white").pack(pady=5)
        ttk.Combobox(popup, values=["All"] + CATEGORIES, textvariable=cat, state="readonly").pack()

        ttk.Label(popup, text="Colour", background=wardrobe_panel_bg, foreground="white").pack(pady=5)
        ttk.Combobox(popup, values=["All"] + COLOURS, textvariable=col, state="readonly").pack()

        ttk.Label(popup, text="Season", background=wardrobe_panel_bg, foreground="white").pack(pady=5)
        ttk.Combobox(popup, values=["All"] + SEASONS, textvariable=sea, state="readonly").pack()

        #done button
        ttk.Button(popup, text="Done", command= lambda: self.recommend_items(cat.get(), col.get(), sea.get(), popup)).pack(pady=15)

    #RECOMMEND FUNCTION
    def recommend_items(self, category, colour, season, popup):
        popup.destroy()

        conn= sqlite3.connect("data.db")
        cur = conn.cursor()
        user_id = self.master.master.current_user_id

        cur.execute("""SELECT image_path, category, colour, season FROM Items WHERE user_id=?""", (user_id,))

        scored = []

        for path, cat, col, sea in cur.fetchall():
            score = 0
            if category != "All" and cat == category:
                score+= 1
            if colour != "All" and col == colour:
                score += 1
            if season != "All" and sea == season:
                score+= 1
            if score > 0:
                scored.append((score,path))

        conn.close()
        scored.sort(reverse=True)
        top_items = [p for _, p in scored[:3]]

        self.show_items_from_query(recommended=True, recommended_paths=top_items)     

    def show_items_from_query(self, recommended=False, recommended_paths=None):
        #removes previous items
        for widget in self.item_frame.winfo_children():
            widget.destroy()
        self.image_refs.clear()

        paths = recommended_paths or []

        row=0
        col=0

        if recommended:
            found_label = tk.Label(self.item_frame, text="Items that best match:", bg=wardrobe_panel_bg, fg=canvas_bg, font=("Open Sans", 15, "bold"))
            found_label.grid(row=row, column=0, columnspan=3, pady=(0,10))
            row=1

        for image_path in paths:
            try: 
                img = Image.open(image_path).resize((120,120))
                tk_img = ImageTk.PhotoImage(img)
                self.image_refs.append(tk_img)
            except:
                continue

            tk.Button(self.item_frame, image=tk_img, bg=wardrobe_panel_bg, bd=0, command=lambda p=image_path: self.add_to_outfit(p)).grid(row=row, column=col, padx=10, pady=10)

            col +=1
            if col == 3:
                col = 0
                row+=1    
    
                
    #OUTFIT FUNCTION
    def add_to_outfit(self, image_path):
        try:
            img = Image.open(image_path).resize((180,180))
            tk_img = ImageTk.PhotoImage(img)
        except:
            return

        wrapper = tk.Frame(self.creation_frame, bg=canvas_bg)
        wrapper.pack(pady=10)

        label = tk.Label(wrapper, image=tk_img, bg=canvas_bg)
        label.image=tk_img
        label.pack(anchor="center")

        self.outfit_items.append(wrapper)
        self.outfit_image_paths.append(image_path)

    #FUNCTIONS FOR THE UNOD AND CLEAR ICON
    def undo_last_item(self):
        if self.outfit_items:
            last_item = self.outfit_items.pop()
            last_item.destroy()

    def clear_outfit(self):
        for item in self.outfit_items:
            item.destroy()
        self.outfit_items.clear() 
        self.outfit_image_paths.clear()

    #FUNCTION OT SAVE ITEM TO DB
    def save_outfit_function(self):
        if not self.outfit_image_paths:
            messagebox.showerror("Error", "No items in outfit canvas to save.") 
            return

        user_id = self.master.master.current_user_id
        success=save_outfit(user_id, self.outfit_image_paths)         

        if success:
            messagebox.showinfo("Successful", "Outfit saved successfully!")    

            #clearing canvas
            self.clear_outfit()
            self.outfit_image_paths.clear()
        else:
            messagebox.showerror("Error", "Error saving outfit. Please try again.")      
        


    


            
    

   
