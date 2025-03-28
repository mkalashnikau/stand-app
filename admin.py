import sqlite3
import os
import streamlit as st

# Ensure directories exist
os.makedirs("assets/images", exist_ok=True)
os.makedirs("assets/videos", exist_ok=True)

# Admin Authentication
def authenticate(admin_password):
    stored_password = "admin123"  # Default password, update for security
    return admin_password == stored_password

# Database Functions
def get_capsule(id):
    conn = sqlite3.connect('capsules_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, information FROM capsules WHERE id = ?", (id,))
    result = cursor.fetchone()
    conn.close()
    return result

def update_capsule(id, title, information, image_file=None, video_file=None):
    conn = sqlite3.connect('capsules_database.db')
    cursor = conn.cursor()

    # Update capsule data explicitly
    cursor.execute("""
        UPDATE capsules 
        SET title = ?, information = ? 
        WHERE id = ?
    """, (title, information, id))
    conn.commit()
    conn.close()

    # Save or replace associated image
    if image_file:
        save_image(id, image_file)

    # Save or replace associated video
    if video_file:
        save_video(id, video_file)

def delete_capsule(id):
    conn = sqlite3.connect('capsules_database.db')
    cursor = conn.cursor()

    # Delete the capsule from the database
    cursor.execute("DELETE FROM capsules WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    # Delete associated image file
    image_path = f"assets/images/{id}.jpg"
    if os.path.exists(image_path):
        os.remove(image_path)

    # Delete associated video file
    video_path = f"assets/videos/{id}.mp4"
    if os.path.exists(video_path):
        os.remove(video_path)

def add_capsule(id, title, information, image_file=None, video_file=None):
    conn = sqlite3.connect('capsules_database.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO capsules (id, title, information) 
        VALUES (?, ?, ?)
    """, (id, title, information))
    conn.commit()
    conn.close()

    # Save image if uploaded
    if image_file:
        save_image(id, image_file)

    # Save video if uploaded
    if video_file:
        save_video(id, video_file)

def save_image(id, image_file):
    # Save image file to the updated path
    with open(f"assets/images/{id}.jpg", "wb") as f:
        f.write(image_file.getbuffer())

def save_video(id, video_file):
    # Save video file to the updated path
    with open(f"assets/videos/{id}.mp4", "wb") as f:
        f.write(video_file.getbuffer())

# Persist searched capsule in session state
if "editing_capsule" not in st.session_state:
    st.session_state.editing_capsule = None

if "editing_mode" not in st.session_state:
    st.session_state.editing_mode = False

# Admin Panel UI
st.title("Админ-панель капсул времени")
admin_password = st.text_input("Введите пароль администратора:", type="password")

if authenticate(admin_password):
    st.success("Аутентификация успешна!")
    
    # Search Capsules
    st.subheader("Поиск капсулы")
    search_id = st.text_input("Введите ID капсулы для поиска:")
    if st.button("Найти капсулу"):
        capsule = get_capsule(search_id)
        if capsule:
            st.success(f"Капсула найдена: ID ({capsule[0]})")
            st.session_state.editing_capsule = capsule  # Persist capsule details in session state
            st.session_state.editing_mode = True
        else:
            st.error("Капсула не найдена!")

    # Editing Capsule Section
    if st.session_state.editing_mode and st.session_state.editing_capsule:
        st.write("### Редактировать капсулу")
        capsule_id = st.session_state.editing_capsule[0]
        capsule_title = st.session_state.editing_capsule[1]
        capsule_information = st.session_state.editing_capsule[2]

        # Editable Fields
        new_title = st.text_input("Название капсулы:", value=capsule_title, key="capsule_title")
        new_information = st.text_area("Информация о капсуле:", value=capsule_information, key="capsule_information")
        new_image_file = st.file_uploader("Загрузить новое изображение (необязательно)", type=["jpg", "jpeg", "png"])
        new_video_file = st.file_uploader("Загрузить новое видео (необязательно)", type=["mp4"])

        if st.button("Обновить капсулу"):
            if new_title.strip() and new_information.strip():
                update_capsule(capsule_id, new_title, new_information, new_image_file, new_video_file)
                st.success("Капсула успешно обновлена!")
                st.session_state.editing_capsule = (capsule_id, new_title, new_information)  # Update session state
                if new_image_file:
                    st.info("Изображение обновлено!")
                if new_video_file:
                    st.info("Видео обновлено!")
            else:
                st.error("Все поля должны быть заполнены!")

        # Delete Capsule
        if st.button("Удалить капсулу"):
            delete_capsule(capsule_id)
            st.warning("Капсула удалена!")
            st.session_state.editing_capsule = None
            st.session_state.editing_mode = False

        # Add a back button to exit editing
        if st.button("Вернуться к поиску"):
            st.session_state.editing_capsule = None
            st.session_state.editing_mode = False

    # Add Capsule Section
    st.subheader("Добавить новую капсулу")
    new_id = st.text_input("ID новой капсулы:")
    new_title = st.text_input("Название новой капсулы:")
    new_information = st.text_area("Информация о новой капсуле:")
    new_image_file = st.file_uploader("Загрузить изображение капсулы:", type=["jpg", "jpeg", "png"])
    new_video_file = st.file_uploader("Загрузить видео капсулы:", type=["mp4"])

    if st.button("Добавить капсулу"):
        if new_id.strip() and new_title.strip() and new_information.strip():
            add_capsule(new_id, new_title, new_information, new_image_file, new_video_file)
            st.success(f"Капсула {new_id} успешно добавлена!")
            if new_image_file:
                st.info(f"Изображение добавлено: assets/images/{new_id}.jpg")
            if new_video_file:
                st.info(f"Видео добавлено: assets/videos/{new_id}.mp4")
        else:
            st.error("Все поля должны быть заполнены!")
else:
    st.error("Ошибка аутентификации.")