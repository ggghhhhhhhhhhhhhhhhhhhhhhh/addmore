import streamlit as st
from pathlib import Path

# Placeholder for a simple user database
users = {"admin": {"password": "admin123", "is_admin": True}, "user": {"password": "user123", "is_admin": False}}
lost_items = []
found_items = []

# Load HTML files
def load_html(file_name):
    file_path = Path("templates") / file_name
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Main function to handle navigation and pages
def main():
    st.set_page_config(page_title="RecoverEase", page_icon="🔍")
    menu = ["Home", "Login", "Register", "Report Lost", "Report Found", "Admin"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Home":
        st.write(load_html("index.html"), unsafe_allow_html=True)
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

def login_page():
    st.write(load_html("login.html"), unsafe_allow_html=True)

def register_page():
    st.write(load_html("register.html"), unsafe_allow_html=True)

def report_lost_page():
    st.write(load_html("report_lost.html"), unsafe_allow_html=True)

def report_found_page():
    st.write(load_html("report_found.html"), unsafe_allow_html=True)

def admin_page():
    st.write(load_html("admin.html"), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
