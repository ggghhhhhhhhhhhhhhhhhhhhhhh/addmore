import streamlit as st
import sqlite3

# Connect to the SQLite Database
def get_conn():
    return sqlite3.connect('recoverease.db')

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

# Delete a lost item by ID
def delete_lost_item(item_id):
    conn = get_conn()
    conn.execute('DELETE FROM lost_items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

# Delete a found item by ID
def delete_found_item(item_id):
    conn = get_conn()
    conn.execute('DELETE FROM found_items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

# Display Lost Items with the option to delete (admin only)
def show_lost_items():
    items = fetch_lost_items()
    if items:
        st.write("### Lost Items")
        st.write("""
        <table style="width:100%">
        <tr>
            <th>Owner Name</th>
            <th>Description</th>
            <th>Last Seen Location</th>
            <th>Status</th>
            <th>Action</th>
        </tr>
        """, unsafe_allow_html=True)
        
        for item in items:
            delete_button = ""
            if st.session_state.get("is_admin"):
                # Add a delete button for admin users
                delete_button = st.button(f"Delete {item[0]}", key=f"delete_lost_{item[0]}")
                if delete_button:
                    delete_lost_item(item[0])
                    st.success(f"Lost item {item[1]} deleted successfully.")
                    st.experimental_rerun()
                    
            st.write(f"""
            <tr>
                <td>{item[1]}</td>
                <td>{item[2]}</td>
                <td>{item[3]}</td>
                <td>{item[4]}</td>
                <td>{delete_button}</td>
            </tr>
            """, unsafe_allow_html=True)
        st.write("</table>", unsafe_allow_html=True)
    else:
        st.write("No lost items reported yet.")

# Display Found Items with the option to delete (admin only)
def show_found_items():
    items = fetch_found_items()
    if items:
        st.write("### Found Items")
        st.write("""
        <table style="width:100%">
        <tr>
            <th>Finder Name</th>
            <th>Description</th>
            <th>Found Location</th>
            <th>Action</th>
        </tr>
        """, unsafe_allow_html=True)

        for item in items:
            delete_button = ""
            if st.session_state.get("is_admin"):
                # Add a delete button for admin users
                delete_button = st.button(f"Delete {item[0]}", key=f"delete_found_{item[0]}")
                if delete_button:
                    delete_found_item(item[0])
                    st.success(f"Found item {item[1]} deleted successfully.")
                    st.experimental_rerun()

            st.write(f"""
            <tr>
                <td>{item[1]}</td>
                <td>{item[2]}</td>
                <td>{item[3]}</td>
                <td>{delete_button}</td>
            </tr>
            """, unsafe_allow_html=True)
        st.write("</table>", unsafe_allow_html=True)
    else:
        st.write("No found items reported yet.")

# Main function to handle navigation and pages
def main():
    st.set_page_config(page_title="RecoverEase", page_icon="🔍")
    
    # Navigation menu (only show other options after login)
    if st.session_state.get("logged_in"):
        menu = ["Home", "Report Lost", "Report Found", "Logout"]
    else:
        menu = ["Login", "Register"]

    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Home":
        home_page()
    elif choice == "Login":
        login_page()
    elif choice == "Register":
        register_page()
    elif choice == "Report Lost":
        report_lost_page()
    elif choice == "Report Found":
        report_found_page()
    elif choice == "Logout":
        st.session_state.clear()
        st.experimental_rerun()

# Example Home Page
def home_page():
    st.title("Home - Lost and Found Items")
    if st.session_state.get("is_admin"):
        st.success("Welcome, admin!")
        show_lost_items()
        show_found_items()
    else:
        st.success(f"Welcome, {st.session_state['username']}!")
        show_lost_items()

# Example Login Page
def login_page():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Example login logic (for now we'll assume username "admin" is the only admin)
        if username == "admin" and password == "admin":
            st.session_state["logged_in"] = True
            st.session_state["is_admin"] = True
            st.session_state["username"] = username
            st.success("Logged in as admin.")
            st.experimental_rerun()
        else:
            st.session_state["logged_in"] = True
            st.session_state["is_admin"] = False
            st.session_state["username"] = username
            st.success(f"Logged in as {username}.")
            st.experimental_rerun()

# Main entry point
if __name__ == "__main__":
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["is_admin"] = False

    main()

