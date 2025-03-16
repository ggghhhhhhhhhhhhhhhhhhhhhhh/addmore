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

# Connect to the SQLite Database
def get_conn():
    return sqlite3.connect('recoverease.db')

# Insert user into the database
def register_user(username, password, is_admin=0):
    conn = get_conn()
    conn.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)', (username, password, is_admin))
    conn.commit()
    conn.close()

# Check user credentials for login
def check_user(username, password):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cur.fetchone()
    conn.close()
    return user

# Insert lost item into the database
def report_lost_item(owner_name, item_desc, last_seen_location):
    conn = get_conn()
    conn.execute('INSERT INTO lost_items (owner_name, item_desc, last_seen_location, status) VALUES (?, ?, ?, ?)', 
                 (owner_name, item_desc, last_seen_location, "Lost"))
    conn.commit()
    conn.close()

# Insert found item into the database
def report_found_item(finder_name, item_desc, found_location):
    conn = get_conn()
    conn.execute('INSERT INTO found_items (finder_name, item_desc, found_location) VALUES (?, ?, ?)', 
                 (finder_name, item_desc, found_location))
    conn.commit()
    conn.close()

# Update lost item status to found
def update_lost_item_status(item_id):
    conn = get_conn()
    conn.execute('UPDATE lost_items SET status = "Found" WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

# Fetch lost items from the database
def fetch_lost_items():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM lost_items')
    items = cur.fetchall()
    conn.close()
    return items

# Fetch found items from the database
def fetch_found_items():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM found_items')
    items = cur.fetchall()
    conn.close()
    return items

# Main function to handle navigation and pages
def main():
    st.set_page_config(page_title="RecoverEase", page_icon="🔍")
    
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["is_admin"] = False
        st.session_state["username"] = ""

    # Show all sidebar options regardless of login state
    menu = ["Login", "Register", "Home", "Report Lost", "Report Found", "Admin", "Logout"]

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
            st.warning("Please login to access this page.")
    elif choice == "Report Found":
        if st.session_state["logged_in"]:
            report_found_page()
        else:
            st.warning("Please login to access this page.")
    elif choice == "Admin":
        if st.session_state["is_admin"]:
            admin_page()
        else:
            st.warning("Admin access required.")
    elif choice == "Logout":
        if st.session_state["logged_in"]:
            st.session_state["logged_in"] = False
            st.session_state["is_admin"] = False
            st.session_state["username"] = ""
            st.success("You have been logged out.")

# Home Page
def home_page():
    st.title("Home - Lost and Found Items")

    if st.session_state["logged_in"]:
        st.success(f"Welcome, {st.session_state['username']}!")

        # Show lost and found items based on user role
        if st.session_state["username"] == "admin":
            st.subheader("Lost Items")
            show_lost_items()

            st.subheader("Found Items")
            show_found_items()
        else:
            st.subheader("Lost Items")
            show_lost_items()
    else:
        st.markdown("Please login to see the items.")

# Login Page
def login_page():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = check_user(username, password)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["is_admin"] = user[2]
            st.session_state["username"] = username
            st.success(f"Welcome {username}! You can now access other options from the sidebar.")
        else:
            st.error("Invalid username or password.")

# Register Page
def register_page():
    st.title("Register")

    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if password == confirm_password and st.button("Register"):
        register_user(username, password)
        st.success(f"User {username} registered successfully.")
    elif st.button("Register"):
        st.error("Passwords do not match!")

# Report Lost Page
def report_lost_page():
    st.title("Report Lost Item")
    
    owner_name = st.text_input("Owner Name")
    item_desc = st.text_input("Item Description")
    last_seen_location = st.text_input("Last Seen Location")
    status = "Lost"  # Default status for lost items

    if st.button("Submit"):
        report_lost_item(owner_name, item_desc, last_seen_location)
        st.success("Lost item reported successfully!")

    show_lost_items()

# Report Found Page
def report_found_page():
    st.title("Report Found Item")
    
    finder_name = st.text_input("Finder Name")
    item_desc = st.text_input("Item Description")
    found_location = st.text_input("Found Location")

    if st.button("Submit"):
        report_found_item(finder_name, item_desc, found_location)
        st.success("Found item reported successfully!")

    show_found_items()

# Admin Page
def admin_page():
    st.title("Admin Dashboard")
    
    st.subheader("Lost Items")
    show_lost_items()

    st.subheader("Found Items")
    show_found_items()

# Display Lost Items
def show_lost_items():
    items = fetch_lost_items()
    if items:
        st.write("""<table><tr><th>Owner Name</th><th>Description</th><th>Last Seen Location</th><th>Status</th><th>Action</th></tr>""", unsafe_allow_html=True)
        
        for item in items:
            status = item[4]
            action_button = ""
            if status == "Lost":
                # Add a button with a unique key to mark as found
                if st.button(f"Mark as Found", key=f"mark_found_{item[0]}"):
                    update_lost_item_status(item[0])
                    st.success(f"Marked item ID {item[0]} as found!")

            st.write(f"""<tr><td>{item[1]}</td><td>{item[2]}</td><td>{item[3]}</td><td>{status}</td><td>{action_button}</td></tr>""", unsafe_allow_html=True)
            
        st.write("</table>", unsafe_allow_html=True)
    else:
        st.write("No lost items reported yet.")

# Display Found Items
def show_found_items():
    items = fetch_found_items()
    if items:
        st.write("""
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            th, td {
                padding: 8px 12px;
                border: 1px solid #ddd;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
        <table>
            <tr>
                <th>Finder Name</th>
                <th>Description</th>
                <th>Found Location</th>
            </tr>
        """, unsafe_allow_html=True)

        for item in items:
            st.write(f"""
            <tr>
                <td>{item[1]}</td>
                <td>{item[2]}</td>
                <td>{item[3]}</td>
            </tr>
            """, unsafe_allow_html=True)
        
        st.write("</table>", unsafe_allow_html=True)
    else:
        st.write("No found items reported yet.")
