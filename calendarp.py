import tkinter as tk
from tkcalendar import Calendar
from database import save_outfit_date
import sqlite3
from tkinter import messagebox
from datetime import datetime, date

main_bg = "#E3A869"
class CalendarPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=main_bg)

        #calendar page title
        title = tk.Label(self, text="Calendar", font=("Brush Script MT", 50, "bold"), bg=main_bg)
        title.pack(pady=20)

        #calendar widget
        self.calendar = Calendar(self, selectmode="day", date_pattern="yyyy-mm-dd", font=("Open Sans", 18),
                                 background= "white", foreground="black", headersbackground="#8B1A1A", headersforeground="white", bordercolor="#8B1A1A", 
                                 othermonthweforeground="gray", weekendbackground="#F5E1C1")
        self.calendar.pack(pady=20, ipadx=40, ipady=40)

        self.calendar.tag_config("saved", background = "#8B0000", foreground="black")

        self.add_outfit_btn = tk.Button(self, text="Add Outfit to Date", font=("Open Sans", 18,"bold"), bg="#8B1A1A", fg="white", command=self.add_outfit_date)
        self.add_outfit_btn.pack(pady=20)

        #todays outfit/no outfit label
        self.today_outfit = tk.Label(self, text="No outfit saved for today.", font=("Open sans", "20","bold"), bg=main_bg, fg="#8B1A1A")
        self.today_outfit.pack(pady=20) 

        self.highlighted_date()
        self.todays_outfit

    #function for highlighted saved dates by user
    def highlighted_date(self):
        user_id = self.master.master.current_user_id
        if user_id is None:
            return

        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute("SELECT date FROM Calendar_Outfits WHERE user_id=?",(user_id,))
        dates = [row[0] for row in cur.fetchall()]
        conn.close()

        #removing the current colour 
        self.calendar.calevent_remove("all") 

        #new highlights
        for d in dates:
            year,month,day=map(int, d.split('-'))
            date_obj = date(year,month,day)
            self.calendar.calevent_create(date_obj, f"Outfit Saved", "saved") 

        #styling
        self.calendar.tag_config("saved", background="#7C4848", foreground="white")     



    #function for the messsageb label when an outfit has been saved to the current date
    def todays_outfit(self):
        user_id = self.master.master.current_user_id
        today = date.today().strftime("%Y-%m-%d")

        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute("SELECT outfit_id FROM Calendar_Outfits WHERE user_id=? AND date=?", (user_id, today))
        result=cur.fetchone()
        conn.close()

        if result:
            self.today_outfit.config(text=f"Today outfit is Outfit ID: {result[0]}.")
        else:
            self.today_outfit.config(text="No outfit saved for today.")  

    #calling the message label function sepeartely
    def called(self):
        self.todays_outfit()     
        self.highlighted_date()   

    def add_outfit_date(self):
        selected_date = self.calendar.get_date()
        user_id = self.master.master.current_user_id    

        #gets users outfits
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute("SELECT outfit_id FROM Outfits WHERE user_id=?", (user_id,))
        outfits = [row[0] for row in cur.fetchall()]
        conn.close()

        if not outfits:
            messagebox.showinfo("No outfits.", "You have no saved outfits to add.")
            return 
        
        #popup to select an outfit
        popup = tk.Toplevel(self, background=main_bg)
        popup.title(f"Select Outfit for {selected_date}")
        popup.geometry("400x500")
        popup.grab_set()

        tk.Label(popup, text="Select an Outfit ID:", font=("Arial", 14)).pack(pady=10)

        outfit_var = tk.IntVar(value=outfits[0])
        for oid in outfits:
            tk.Radiobutton(popup, text=f"Outfit ID: {oid}", variable=outfit_var, value=oid, font=("Arial", 12)).pack(anchor="w", padx=20, pady=5)

        def save_selected():
            outfit_id = outfit_var.get()
            success = save_outfit_date(user_id, outfit_id, selected_date)
            if success:
                messagebox.showinfo("Saved", f"Outfit {outfit_id} saved for {selected_date}")
                self.highlighted_date()
                self.todays_outfit()
            else:
                messagebox.showerror("Error", "Could not save outfit.")    
            popup.destroy()

        tk.Button(popup, text="Save", font=("Open sans", 13, "bold"), bg="#8B1A1A", fg="white", command=save_selected).pack(pady=20)    
    



                