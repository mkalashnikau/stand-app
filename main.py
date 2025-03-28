import sqlite3
import os
import streamlit as st
from PIL import Image


# Connect to SQLite database
def search_capsule(search_key, search_type):
    conn = sqlite3.connect("capsules_database.db")
    cursor = conn.cursor()

    # Search by ID or Title
    if search_type == "ID":
        cursor.execute(
            "SELECT id, title, information FROM capsules WHERE id = ?", (search_key,)
        )
    elif search_type == "Title":
        cursor.execute(
            "SELECT id, title, information FROM capsules WHERE title LIKE ?",
            ("%" + search_key + "%",),
        )

    result = cursor.fetchone()
    conn.close()
    return result


# Streamlit app configuration
st.title("Добро пожаловать в библиотеку капсул времени")
st.subheader("Поиск капсулы по номеру или названию")
st.set_option("client.toolbarMode", "viewer")
st.markdown(
    """
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""",
    unsafe_allow_html=True,
)

# Dropdown for search type
search_type = st.selectbox("Поиск по:", ["номеру", "названию"])

# Map Russian options to English values
search_type_mapping = {
    "номеру": "ID",
    "названию": "Title"
}
search_type_mapped = search_type_mapping.get(search_type)

# Input field based on search type
search_key = st.text_input("Строка поиска")

if st.button("Поиск"):
    result = search_capsule(search_key, search_type_mapped)
    if result:
        capsule_id, title, info = result
        st.write(f"### Capsule ID: {capsule_id}")
        st.write(f"### {title}")
        st.write(info)
        # Use ID to locate the image file
        image_path = f"assets/images/{capsule_id}.jpg"
        try:
            image = Image.open(image_path)
            st.image(image, caption=f"Image for Capsule '{title}'")
        except FileNotFoundError:
            st.write("Image not found.")
        # Display Capsule Video
        video_path = f"assets/videos/{capsule_id}.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning("No video available for this capsule.")
    else:
        st.error("Capsule not found.")
