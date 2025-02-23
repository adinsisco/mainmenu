import streamlit as st
import sqlite3
import webbrowser

# Połączenie z bazą danych SQLite
conn = sqlite3.connect('buttons.db')
c = conn.cursor()

# Tworzenie tabeli, jeśli nie istnieje
c.execute('''
    CREATE TABLE IF NOT EXISTS buttons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        url TEXT
    )
''')
conn.commit()

# Formularz dodawania przycisku
st.sidebar.header("Dodaj nowy przycisk")
new_name = st.sidebar.text_input("Nazwa przycisku")
new_url = st.sidebar.text_input("URL")

if st.sidebar.button("Dodaj"):
    if new_name and new_url:
        c.execute("INSERT INTO buttons (name, url) VALUES (?, ?)", (new_name, new_url))
        conn.commit()
        st.sidebar.success("Przycisk dodany!")

# Formularz usuwania przycisku
st.sidebar.header("Usuń przycisk")
delete_id = st.sidebar.number_input("ID do usunięcia", min_value=1, step=1)

if st.sidebar.button("Usuń"):
    c.execute("DELETE FROM buttons WHERE id = ?", (delete_id,))
    conn.commit()
    st.sidebar.success("Przycisk usunięty!")

# Pole sortowania
sort_option = st.selectbox("Sortuj wg", options=["Nazwa (A-Z)", "Nazwa (Z-A)", "ID (rosnąco)", "ID (malejąco)"])

if sort_option == "Nazwa (A-Z)":
    order_by = "name ASC"
elif sort_option == "Nazwa (Z-A)":
    order_by = "name DESC"
elif sort_option == "ID (rosnąco)":
    order_by = "id ASC"
else:
    order_by = "id DESC"

# Wyświetlanie przycisków
st.title("Menu")
c.execute(f"SELECT id, name, url FROM buttons ORDER BY {order_by}")
buttons = c.fetchall()

for button in buttons:
    button_label = f"{button[1]} (ID: {button[0]})"
    if st.button(button_label):
        webbrowser.open_new_tab(button[2])

conn.close()