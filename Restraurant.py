import streamlit as st
import sqlite3
from datetime import date

# --- DATABASE SETUP ---
conn = sqlite3.connect("restaurant.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    people INTEGER,
    booking_date TEXT
)
""")
conn.commit()

# --- FUNCTIONS ---
def add_reservation(name, people, booking_date):
    c.execute("INSERT INTO reservations (name, people, booking_date) VALUES (?, ?, ?)",
              (name, people, booking_date))
    conn.commit()

def get_reservations():
    c.execute("SELECT * FROM reservations")
    return c.fetchall()

# --- UI ---
st.set_page_config(page_title="Restaurant Website", layout="wide")

st.title("🍽️ Spice Delight Restaurant")

menu = ["Home", "Menu", "Gallery", "Book Table", "Admin"]
choice = st.sidebar.selectbox("Navigation", menu)

# --- HOME ---
if choice == "Home":
    st.header("Welcome!")
    st.write("Enjoy delicious food and great service.")

# --- MENU ---
elif choice == "Menu":
    st.header("📜 Our Menu")
    st.write("Paneer Tikka - ₹250")
    st.write("Veg Biryani - ₹220")
    st.write("Gulab Jamun - ₹120")

# --- GALLERY ---
elif choice == "Gallery":
    st.header("📸 Gallery")
    st.image("https://images.unsplash.com/photo-1555396273-367ea4eb4db5")

# --- BOOK TABLE ---
elif choice == "Book Table":
    st.header("📅 Reserve Your Table")

    name = st.text_input("Your Name")
    people = st.number_input("Number of People", min_value=1, max_value=20)
    booking_date = st.date_input("Select Date", min_value=date.today())

    if st.button("Reserve"):
        if name:
            add_reservation(name, people, str(booking_date))
            st.success("✅ Table booked successfully!")
        else:
            st.error("Please enter your name")

# --- ADMIN PANEL ---
elif choice == "Admin":
    st.header("🔐 Admin Panel")

    password = st.text_input("Enter Admin Password", type="password")

    if password == "admin123":   # change this later
        st.success("Access Granted")

        data = get_reservations()

        if data:
            st.subheader("📋 All Reservations")
            for row in data:
                st.write(f"ID: {row[0]} | Name: {row[1]} | People: {row[2]} | Date: {row[3]}")
        else:
            st.info("No reservations yet")

    elif password:
        st.error("Wrong Password")
