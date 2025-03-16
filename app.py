import streamlit as st
import sqlite3
from sqlite3 import Connection

# Database Setup
def init_db(conn: Connection):
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        is_admin INTEGER NOT NULL DEFAULT 0
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS lost_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_name TEXT,
        item_desc TEXT,
        last_seen_location TEXT,
        status TEXT
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS found_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        finder_name TEXT,
        item_desc TEXT,
        found_location TEXT
    )''')
    conn.commit()

# Connect to SQLite Database
def get_conn():
    return sqlite3.connect('recoverease.db')

# User Functions
def register_user(username, password, is_admin=0):
    conn = get_conn()
    conn.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)', (username, password, is_admin))
    conn.commit()
    conn.close()

def check_user(username, password):
    conn = get_conn()
    user = conn.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password)).fetchone()
    conn.close()
    return user

# Lost & Found Item Functions
def report_lost_item(owner_name, item_desc, last_seen_location):
    conn = get_conn()
    conn.execute('INSERT INTO lost_items (owner_name, item_desc, last_seen_location, status) VALUES (?, ?, ?, ?)',
                 (owner_name, item_desc, last_seen_location, "Lost"))
    conn.commit()
    conn.close()

def report_found_item(finder_name, item_desc, found_location):
    conn = get_conn()
    conn.execute('INSERT INTO found_items (finder_name, item_desc, found_location) VALUES (?, ?, ?)',
                 (finder_name, item_desc, found_location))
    conn.commit()
    conn.close()

def fetch_lost_items():
    conn = get_conn()
    items = conn.execute('SELECT * FROM lost_items').fetchall()
    conn.close()
    return items

def fetch_found_items():
    conn = get_conn()
    items = conn.execute('SELECT * FROM found_items').fetchall()
    conn.close()
    return items

# Delete Items from Database
def delete_lost_item(item_id):
    conn = get_conn()
    conn.execute('DELETE FROM lost_items WHERE id=?', (item_id,))
    conn.commit()
    conn.close()

def delete_found_item(item_id):
    conn = get_conn()
    conn.execute('DELETE FROM found_items WHERE id=?', (item_id,))
    conn.commit()
    conn.close()

# Streamlit App Pages
def main():
    st.set_page_config(page_title="RecoverEase", page_icon="🔍")
    
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["is_admin"] = False
        st.session_state["username"] = ""

    menu = ["Home", "Login", "Register", "Report Lost", "Report Found", "Admin", "Logout"]
    
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        home_page()
        
    elif choice == "Login":
        login_page()

    elif choice == "Register":
        register_page()

    elif choice == "Report Lost":
        if st.session_state["logged_in"]:
            report_lost_page()
        else:
            st.warning("Please login first.")

    elif choice == "Report Found":
        if st.session_state["logged_in"]:
            report_found_page()
        else:
            st.warning("Please login first.")

    elif choice == "Admin":
        if st.session_state["is_admin"]:
            admin_page()
        else:
            st.warning("Admin access required.")

    elif choice == "Logout":
        st.session_state["logged_in"] = False
        st.session_state["is_admin"] = False
        st.session_state["username"] = ""
        st.success("Logged out successfully.")

# Individual Page Definitions

def home_page():
    st.title("RecoverEase - Home")
    
    if st.session_state["logged_in"]:
        st.success(f"Welcome {st.session_state['username']}!")
        
        st.subheader("Lost Items")
        show_lost_items(admin_view=False)
        
        st.subheader("Found Items")
        show_found_items(admin_view=False)
        
    else:
        st.info("Please login to view items.")

def login_page():
    st.title("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = check_user(username, password)
        
        if user:
            st.session_state["logged_in"] = True
            st.session_state["is_admin"] = bool(user[2])
            st.session_state["username"] = username
            st.success(f"Welcome back {username}!")
            
        else:
            st.error("Invalid credentials.")

def register_page():
    st.title("Register")
    
    username = st.text_input("New Username")
    
    password1 = st.text_input("Password", type="password")
    
    password2 = st.text_input("Confirm Password", type="password")

    if password1 == password2 and st.button("Register"):
        
        register_user(username, password1)
        
        st.success(f"User {username} registered successfully.")
        
def report_lost_page():
    
    st.title("Report Lost Item")

    
    owner_name = st.text_input("Owner Name")
    
   
  
item_desc=st.text_input("Item Description")

last_seen=st.text_input("Last Seen Location")

if(st.button("Submit")):
  report_lost_item(owner_name,item_desc,last_seen)
  st.success("Lost item reported successfully!")

def report_found_page():

  st.title("Report Found Item")

  finder_name=st.text_input("Finder Name")

  item_desc=st.text_input("Item Description")

  found_loc=st.text_input("Found Location")

  if(st.button("Submit")):
      report_found_item(finder_name,item_desc,found_loc)
      st.success("Found item reported successfully!")

# Admin Page with Delete Buttons

def admin_page():
  st.title("Admin Dashboard")

  # Lost Items Table with Delete Option
  show_lost_items(admin_view=True)

  # Found Items Table with Delete Option
  show_found_items(admin_view=True)

# Display Lost Items with Optional Delete Button

def show_lost_items(admin_view=False):
  items=fetch_lost_items()

  for item in items:
      cols=st.columns([2,2,2,1])
      cols[0].write(item[1])
      cols[1].write(item[2])
      cols[2].write(item[3])
      cols[3].write(item[4])

      if admin_view and cols[3].button(f"Delete Lost #{item[0]}"):
          delete_lost_item(item[0])
          st.experimental_rerun()

# Display Found Items with Optional Delete Button

def show_found_items(admin_view=False):
  items=fetch_found_items()

  for item in items:
      cols=st.columns([2,2,2])
      cols[0].write(item[1])
      cols[1].write(item[2])
      cols[2].write(item[3])

      if admin_view and cols[2].button(f"Delete Found #{item[0]}"):
          delete_found_item(item[0])
          st.experimental_rerun()

if __name__=="__main__":
   init_db(get_conn())
   main()

