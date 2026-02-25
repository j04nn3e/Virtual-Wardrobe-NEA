import sqlite3

#CREATING DATABASE

def init_db():
     conn= sqlite3.connect("data.db")
     cur = conn.cursor()

     #creating table to store user data
     table_create_query = '''CREATE TABLE IF NOT EXISTS User_Data 
                         (user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         username TEXT UNIQUE NOT NULL, 
                         password TEXT NOT NULL)'''
     
     cur.execute(table_create_query)

     #creating table to store items uploaded
     item_table = '''CREATE TABLE IF NOT EXISTS Items 
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         user_id INTEGER NOT NULL,
                         item_name TEXT NOT NULL,
                         image_path TEXT NOT NULL,
                         category TEXT NOT NULL,
                         colour TEXT NOT NULL,
                         season TEXT NOT NULL,
                         FOREIGN KEY(user_id) REFERENCES User_Data(user_id))'''

     cur.execute(item_table)

     #creating the table to store outfit
     outfit_table = '''CREATE TABLE IF NOT EXISTS Outfits
                         (outfit_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         user_id INTEGER NOT NULL,
                         FOREIGN KEY(user_id) REFERENCES User_Data(user_id))'''
     cur.execute(outfit_table)

     #creating table to store items linked ot each outfit
     outfit_items_table = '''CREATE TABLE IF NOT EXISTS Outfit_Items 
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              outfit_id INTEGER NOT NULL,
                              image_path TEXT NOT NULL,
                              FOREIGN KEY(outfit_id) REFERENCES Outfits(outfit_id))'''
     cur.execute(outfit_items_table)

     #creating table for calendar outfits
     calendar_table = '''CREATE TABLE IF NOT EXISTS Calendar_Outfits 
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         user_id INTEGER NOT NULL,
                         date TEXT NOT NULL,
                         outfit_id INTEGER NOT NULL,
                         FOREIGN KEY(user_id) REFERENCES User_Data(user_id),
                         FOREIGN KEY(outfit_id) REFERENCES Outfits(outfit_id))'''
     cur.execute(calendar_table)

     conn.commit()
     conn.close()

#function to add user to the database
def add_user(username, password):
    conn=sqlite3.connect("data.db")
    cur = conn.cursor()
    try: 
        cur.execute('INSERT INTO User_Data (username, password) VALUES (?, ?)', (username, password)) #adds the username and password inputted by the user into the correct field in the database
        conn.commit()
        conn.close()
        return True
    #if username already exists then return false
    except sqlite3.IntegrityError:
        conn.close()
        return False
    

# validating the users entry
def validate_user(username, password):
         conn = sqlite3.connect("data.db")
         cursor = conn.cursor()

         cursor.execute("SELECT * FROM User_Data WHERE username=? AND password=?", (username, password)) #searches the database to see if the username and password enetred by the user exists in the database
         result = cursor.fetchone()             
         conn.close() # closing this specific validation connection
         return result is not None

#saving uploaded item linking it to specific user account
def save_item(user_id, item_name, image_path, category, colour, season):
     try:
          conn = sqlite3.connect("data.db")
          cursor = conn.cursor()
          
          cursor.execute('INSERT INTO Items(user_id, item_name, image_path, category, colour, season) VALUES (?, ?, ?, ?, ?, ?)', 
                                (user_id, item_name, image_path, category, colour, season)) #inserts the inputted values by the user from the upload page into the database
          conn.commit()
          return True
     except Exception as e: #if something goes wrong such as not every input fieldn not having a value
          print("Error saving item.", e)
          return False
     
#getting the user_id
def get_user_id(username, password):
     conn_local = sqlite3.connect("data.db")
     cur = conn_local.cursor()
     cur.execute("SELECT user_id FROM User_Data WHERE username=? AND password=?", (username, password)) #retrieveing the userid with teh matching username and password
     row = cur.fetchone()
     conn_local.close()
     return row[0] if row else None

#deleting item from database
def delete_item_db(item_id):
     conn = sqlite3.connect("data.db")
     cur = conn.cursor()
     cur.execute("DELETE FROM Items WHERE id=?", (item_id,))
     conn.commit()
     conn.close()


#saving outfit and its items
def save_outfit(user_id, image_paths):
     try:
          conn = sqlite3.connect("data.db")
          cur = conn.cursor()

          #create outfit
          cur.execute("INSERT INTO Outfits (user_id) VALUES (?)", (user_id,)) #inserts the user id to the respective outfit
          outfit_id = cur.lastrowid 

          for path in image_paths:
               cur.execute("INSERT INTO Outfit_Items (outfit_id, image_path) VALUES (?, ?)", (outfit_id, path))

          conn.commit()
          conn.close()
          return True
     except Exception as e:
          print("Error saving outfit", e)
          return False

#saving outfit to date
def save_outfit_date(user_id, outfit_id, date):
     try:
          conn=sqlite3.connect("data.db")
          cur=conn.cursor()
          cur.execute("INSERT INTO Calendar_Outfits (user_id, outfit_id, date) VALUES (?,?,?)",
                      (user_id, outfit_id, date))
          conn.commit()
          conn.close()
          return True
     except Exception as e:
          print("Error savibg outfit to date", e)
          return False










  