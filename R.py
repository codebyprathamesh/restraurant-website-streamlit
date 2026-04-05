import streamlit as st
import sqlite3
from datetime import date
import smtplib
from email.message import EmailMessage
import bcrypt
import random
import pandas as pd
import matplotlib.pyplot as plt

# --- DATABASE ---
conn = sqlite3.connect("restaurant_final11.db", check_same_thread=False)
c = conn.cursor()

# --- TABLES ---
c.execute("""
CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    people INTEGER,
    booking_date TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS admin (
    email TEXT PRIMARY KEY,
    password BLOB
)
""")

conn.commit()

# --- INIT ADMIN (SAFE) ---
def create_admin():
    password = "admin123".encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    c.execute("SELECT * FROM admin WHERE email=?", ("admin@gmail.com",))
    result = c.fetchone()

    if not result:
        c.execute(
            "INSERT INTO admin (email, password) VALUES (?, ?)",
            ("admin@gmail.com", hashed)
        )
        conn.commit()
create_admin()

# --- FUNCTIONS ---

def add_reservation(name, email, people, booking_date):
    c.execute(
        "INSERT INTO reservations (name, email, people, booking_date) VALUES (?, ?, ?, ?)",
        (name, email, people, booking_date)
    )
    conn.commit()

def get_reservations():
    c.execute("SELECT * FROM reservations")
    return c.fetchall()

def send_email(to_email, subject, body):
    sender_email = "meprathamesh21@gmail.com"
    app_password = "hrmk pksc ddwn ukmd"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)

# --- AUTH FUNCTIONS ---

def check_login(email, password):
    c.execute("SELECT password FROM admin WHERE email=?", (email,))
    result = c.fetchone()
    if result:
        return bcrypt.checkpw(password.encode(), result[0])
    return False

def update_password(email, new_password):
    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    c.execute("UPDATE admin SET password=? WHERE email=?", (hashed, email))
    conn.commit()

# --- UI ---
st.set_page_config(page_title="Restaurant System", layout="wide")

menu = ["Home", "Book Table", "Admin"]
choice = st.sidebar.selectbox("Menu", menu)

# --- HOME ---
if choice == "Home":
    st.title("🍽️ Spice Delight Restaurant")
    st.write("Welcome to our restaurant!")

# --- BOOK TABLE ---
elif choice == "Book Table":
    st.header("📅 Reserve Table")

    name = st.text_input("Name")
    email = st.text_input("Email")
    people = st.number_input("People", 1, 20)
    booking_date = st.date_input("Date", min_value=date.today())

    if st.button("Reserve"):
        if name and email:
            add_reservation(name, email, people, str(booking_date))

            try:
                send_email(
                    email,
                    "Reservation Confirmed",
                    f"Hello {name}, your table for {people} people on {booking_date} is confirmed."
                )
                st.success("Booked & Email Sent ✅")
            except:
                st.warning("Booked but email failed")

        else:
            st.error("Fill all fields")

# --- ADMIN ---
elif choice == "Admin":
    st.header("🔐 Admin Panel")

    tab1, tab2 = st.tabs(["Login", "Forgot Password"])

    # LOGIN
    with tab1:
        email = st.text_input("Admin Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if check_login(email, password):
                st.session_state["admin"] = True
                st.success("Login Successful")
            else:
                st.error("Invalid Credentials")

    # FORGOT PASSWORD
    with tab2:
        f_email = st.text_input("Enter Email")

        if st.button("Send OTP"):
            otp = random.randint(1000, 9999)
            st.session_state["otp"] = str(otp)
            st.session_state["reset_email"] = f_email

            try:
                send_email(
                    f_email,
                    "OTP Reset",
                    f"Your OTP is {otp}"
                )
                st.success("OTP Sent")
            except:
                st.error("Failed to send OTP")

        entered_otp = st.text_input("Enter OTP")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Reset Password"):
            if entered_otp == st.session_state.get("otp"):
                update_password(st.session_state["reset_email"], new_pass)
                st.success("Password Updated")
            else:
                st.error("Wrong OTP")

    # AFTER LOGIN
    if st.session_state.get("admin"):
        st.subheader("📋 Reservations")

        data = get_reservations()

        if data:
            df = pd.DataFrame(data, columns=["ID", "Name", "Email", "People", "Date"])
            st.dataframe(df)

            # GRAPH
            st.subheader("📊 People per Booking")
            fig, ax = plt.subplots()
            df["People"].plot(kind="bar", ax=ax)
            st.pyplot(fig)

            # SEND EMAIL
            st.subheader("📧 Send Custom Email")

            cust_email = st.text_input("Customer Email")
            msg = st.text_area("Message")

            if st.button("Send Email"):
                send_email(cust_email, "Notification", msg)
                st.success("Email Sent 🚀")

        else:
            st.info("No data yet")
