import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from database import save_item
from constants import CATEGORIES, COLOURS, SEASONS
from PIL import Image, ImageTk
import os
main_bg= "#E3A869"

class UploadPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=main_bg)

        #title label
        label = tk.Label(self, 
                         text="Upload Item", 
                         font=("Brush Script MT", 70, "bold"),
                         bg =main_bg
                         )
        label.pack(pady=40) 

        main_font = ("Open Sans",25)

        #upolad image section
        add_image_frame = tk.Frame(self, bg=main_bg)
        add_image_frame.pack(pady=2)

        #image icon
        image_icon = Image.open("images/image_icon.png").resize((50,55))
        self.image_icon_img = ImageTk.PhotoImage(image_icon)

        #label+icon
        image_icon_label = tk.Label(add_image_frame, image=self.image_icon_img, bg=main_bg)
        image_icon_label.pack(side=tk.LEFT, padx=10)
        image_text_label = tk.Label(add_image_frame, text="Add Image File / URL:", font=main_font, bg=main_bg)
        image_text_label.pack(side=tk.LEFT)

        #upload frame
        self.upload_frame = tk.Frame(self, bg=main_bg)
        self.upload_frame.pack(pady=20)

        #upload image button(remeber command)
        self.upload_btn = tk.Button(self.upload_frame, text="Choose Image", font=("Open Sans", 15, "bold"), width=15, bd=3, bg="white", anchor="center", overrelief="sunken",command=self.choose_image)
        self.upload_btn.pack(side="left", padx=(0,10))

        #filename label
        self.filename_label = tk.Label(self.upload_frame, text="", font=("Open Sans", 14), bg=main_bg)
        self.filename_label.pack(side="left", padx=(0,5))

        #remove button
        self.remove_button = None    

        #path of chosen image
        self.chosen_image_path = None

        #top section frame
        top_frame = tk.Frame(self, bg=main_bg)
        top_frame.pack(pady=10, fill="x")

        #bottom section frame
        bottom_frame = tk.Frame(self, bg=main_bg)
        bottom_frame.pack(pady=50, fill="x")

        #item name sectionn(frame)
        itemname_frame = tk.Frame(top_frame, bg=main_bg)
        itemname_frame.pack(side="left", padx=150, anchor="w")
        #label
        itemname_label = tk.Label(itemname_frame,
                                  text="Item name: ",
                                  font=main_font,
                                  bg=main_bg)
        itemname_label.pack(side="top", anchor="c")

        #entrybox for item name
        self.itemname_entry = tk.Text(itemname_frame,
                                       font=("Open Sans", 16),
                                       width=30,
                                       height=2,
                                       highlightthickness=2)
        self.itemname_entry.pack(side="bottom",pady=5)

        #frame for category dropdown
        category_frame = tk.Frame(top_frame, bg=main_bg)
        category_frame.pack(side="right",padx=150, anchor="e")

        category_label = tk.Label(category_frame,
                                  text="Select category: ",
                                  font=main_font, 
                                  bg=main_bg)
        category_label.pack(side="top", anchor="c")

        #category options
      
        
        self.category_var = tk.StringVar(value="Select...")

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Custom.TCombobox",
            fieldbackground="#DEE2E6",
            background="white",
            selectbackground="#DEE2E6",
            selectforeground="black",
            arrowsize=20,
            padding=8
        )
    
        self.category_box = ttk.Combobox(
            category_frame,
            textvariable=self.category_var,
            values=CATEGORIES,
            state="readonly",
            font=("Open Sans", 15),
            width=30,
            style="Custom.TCombobox")
        self.category_box.set("Select...")
        self.category_box.pack(side="top", pady=5)

        self.category_box.set("Select...")
        self.category_box.pack(side="top", pady=5, ipady=8)


        #colour drop down
        colour_frame = tk.Frame(bottom_frame, bg=main_bg) #using same frame as item name as i want it to be below it vertically
        colour_frame.pack(side="left", padx=150, anchor="w")

        colour_label = tk.Label(colour_frame, text="Select colour: ", 
                                font=main_font, bg=main_bg)
        colour_label.pack(side="top", anchor="c")

        #colour options
        
        self.colour_var = tk.StringVar(value="Select...")
        
        self.colour_box = ttk.Combobox(
            colour_frame,
            textvariable=self.colour_var,
            values=COLOURS,
            state="readonly",
            font=("Open Sans", 15),
            width=30,
            style="Custom.TCombobox"
        )

        self.colour_box.set("Select...")
        self.colour_box.pack(side="top", pady=5, ipady=8)

        #season drop down
        season_frame = tk.Frame(bottom_frame, bg=main_bg)
        season_frame.pack(side="right",padx=150, anchor="e")

        season_label = tk.Label(season_frame, text="Select season: ",
                                font=main_font, bg=main_bg)
        season_label.pack(side="top", anchor="c")

        #season options


        self.season_var=tk.StringVar(value="Select...")

        self.season_box = ttk.Combobox(
            season_frame,
            textvariable=self.season_var,
            values=SEASONS,
            state="readonly",
            font=("Open Sans", 15),
            width=30,
            style="Custom.TCombobox"
        )

        self.season_box.set("Select...")
        self.season_box.pack(side="top", pady=5, ipady=8)

        #save item button(remeber to add command)
        saveitem_btn = tk.Button(self, text="Save Item", width=18, anchor="c", bg="#8B1A1A", font=("Open Sans", 18,"bold"), overrelief="sunken", command=self.save_item)
        saveitem_btn.pack(side="top", padx=100,pady=10)


    def choose_image(self):  
        file_path= filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[("Image file", "*.jpg *.jpeg *.png *.gif")]
        ) 

        #if user doesnt select any file or file is empty
        if not file_path: 
            return
        
        self.chosen_image_path = file_path
        self.update_preview()

    def update_preview(self):
        if self.chosen_image_path:
            #show filename and button 'x'
             filename = os.path.basename(self.chosen_image_path)
             self.filename_label.config(text=filename)

             
             if not self.remove_button:
                 self.remove_button = tk.Button(self.upload_frame, text="❌", font =("Open Sans", 14), bg="#E3A869", bd=0, command=self.clear_choice, cursor="hand2")
                 self.remove_button.pack(side="left")
        else:
            self.filename_label.config(text="")

            if self.remove_button:
                self.remove_button.destroy()
                self.remove_button = None
                 
    def clear_choice(self):
        self.chosen_image_path = None 
        self.update_preview()

    def save_item(self):
        #getting all inputted values
        item_name = self.itemname_entry.get("1.0", "end").strip()
        category = self.category_var.get()
        colour = self.colour_var.get()
        season = self.season_var.get()
        image_path = self.chosen_image_path

        #validating that nothinbg is empty
        if not item_name:
            messagebox.showerror("Error","Please enter an item name.") 
            return
        if category in ("Select...",""):
            messagebox.showerror("Error","Please choose a category.")   
            return
        if colour in ("Select...",""):
            messagebox.showerror("Error","Please choose a colour.")
            return
        if season in ("Select...",""):
            messagebox.showerror("Error","Please choose a season.")
            return
        if not image_path:
            messagebox.showerror("Error","Please choose an image for the item.")
            return
        
        #getting logged in user id
        root=self.master.master
        user_id = getattr(root, "current_user_id", None)
        if user_id is None:
            messagebox.showerror("Error", "No user found, please log in again")
            return
        
        #saving into database
        successful = save_item(user_id, item_name, image_path, category, colour, season)
        if successful:
            messagebox.showinfo("Saved","Item saved successfully!")
            #restarting all options
            self.itemname_entry.delete("1.0","end")
            self.chosen_image_path = None
            self.update_preview()
            self.colour_box.set("Select...")
            self.category_box.set("Select...")
            self.season_box.set("Select...")
        else:
            messagebox.showerror("Error","Failed to save item successfully.")
            

