import streamlit as st

# Sample user database
users = {"admin": {"password": "admin123", "is_admin": True}, "user": {"password": "user123", "is_admin": False}}

# Sample data for lost and found items
lost_items = [
    {"owner_name": "John Doe", "item_desc": "Red backpack", "last_seen_location": "Central Park", "status": "Lost"},
    {"owner_name": "Jane Smith", "item_desc": "Blue jacket", "last_seen_location": "Bus Station", "status": "Resolved"}
]

found_items = [
    {"finder_name": "Sam", "item_desc": "Wallet", "found_location": "Coffee Shop"},
    {"finder_name": "Alice", "item_desc": "Umbrella", "found_location": "Library"}
]

# Main function to handle navigation and pages
def main():
    st.set_page_config(page_title="RecoverEase", page_icon="🔍")
    menu = ["Home", "Login", "Register", "Report Lost", "Report Found", "Admin"]
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
    elif choice == "Admin" and st.session_state.get("is_admin"):
        admin_page()
    else:
        st.warning("Please login as an admin to access the admin panel.")

# Home Page
def home_page():
    st.title("Welcome to RecoverEase")
    st.markdown("""
        RecoverEase is a platform to report lost and found items. Use the menu to navigate through the platform.
        """)
    
# Login Page
def login_page():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.success(f"Welcome {username}!")
            st.session_state["is_admin"] = users[username]["is_admin"]
        else:
            st.error("Invalid username or password.")

# Register Page
def register_page():
    st.title("Register")

    st.write("""
    Register a new account to access additional features of RecoverEase.
    """)

    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if password == confirm_password and st.button("Register"):
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
        lost_items.append({"owner_name": owner_name, "item_desc": item_desc, "last_seen_location": last_seen_location, "status": status})
        st.success("Lost item reported successfully!")

    show_lost_items()

# Report Found Page
def report_found_page():
    st.title("Report Found Item")
    
    finder_name = st.text_input("Finder Name")
    item_desc = st.text_input("Item Description")
    found_location = st.text_input("Found Location")

    if st.button("Submit"):
        found_items.append({"finder_name": finder_name, "item_desc": item_desc, "found_location": found_location})
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
    if lost_items:
        st.write("""
        <table>
        <tr>
            <th>Owner Name</th>
            <th>Description</th>
            <th>Last Seen Location</th>
            <th>Status</th>
            <th>Action</th>
        </tr>
        """, unsafe_allow_html=True)
        
        for item in lost_items:
            st.write(f"""
            <tr>
                <td>{item['owner_name']}</td>
                <td>{item['item_desc']}</td>
                <td>{item['last_seen_location']}</td>
                <td>{item['status']}</td>
                <td>
                    {"<a href='#' class='btn'>Mark as Found</a>" if item['status'] == 'Lost' else 'Resolved'}
                </td>
            </tr>
            """, unsafe_allow_html=True)
            
        st.write("</table>", unsafe_allow_html=True)
    else:
        st.write("No lost items reported yet.")

# Display Found Items
def show_found_items():
    if found_items:
        st.write("""
        <table>
        <tr>
            <th>Finder Name</th>
            <th>Description</th>
            <th>Found Location</th>
        </tr>
        """, unsafe_allow_html=True)

        for item in found_items:
            st.write(f"""
            <tr>
                <td>{item['finder_name']}</td>
                <td>{item['item_desc']}</td>
                <td>{item['found_location']}</td>
            </tr>
            """, unsafe_allow_html=True)
        
        st.write("</table>", unsafe_allow_html=True)
    else:
        st.write("No found items reported yet.")

if __name__ == "__main__":
    main()
