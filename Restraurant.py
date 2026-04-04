import streamlit as st

# Page config
st.set_page_config(page_title="Restaurant Website", layout="wide")

# --- HEADER ---
st.title("🍽️ Welcome to Spice Delight")
st.subheader("Delicious Food | Great Ambience | Fast Service")

st.image("https://images.unsplash.com/photo-1555396273-367ea4eb4db5", use_column_width=True)

# --- MENU SECTION ---
st.header("📜 Our Menu")

menu = {
    "Starters": ["Paneer Tikka - ₹250", "Veg Manchurian - ₹200", "Spring Rolls - ₹180"],
    "Main Course": ["Butter Paneer - ₹300", "Veg Biryani - ₹220", "Dal Tadka - ₹180"],
    "Desserts": ["Gulab Jamun - ₹120", "Ice Cream - ₹100", "Brownie - ₹150"]
}

for category, items in menu.items():
    st.subheader(category)
    for item in items:
        st.write("•", item)

# --- GALLERY ---
st.header("📸 Gallery")

col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://images.unsplash.com/photo-1600891964599-f61ba0e24092")

with col2:
    st.image("https://images.unsplash.com/photo-1540189549336-e6e99c3679fe")

with col3:
    st.image("https://images.unsplash.com/photo-1555939594-58d7cb561ad1")

# --- CONTACT ---
st.header("📍 Contact Us")

st.write("📞 Phone: +91 9876543210")
st.write("📍 Location: Mumbai, India")
st.write("⏰ Timings: 10 AM - 11 PM")

# --- RESERVATION ---
st.header("📅 Book a Table")

name = st.text_input("Your Name")
people = st.number_input("Number of People", min_value=1, max_value=20)
date = st.date_input("Select Date")

if st.button("Reserve"):
    st.success(f"Table booked for {name} on {date} for {people} people!")