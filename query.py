import mysql.connector
import streamlit as st

# Connexion à la base de données
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            passwd="",  # Tu peux mettre ton mot de passe ici
            database="mydb"
        )
        return conn
    except mysql.connector.Error as e:
        st.error(f"Erreur de connexion à la base de données : {e}")
        return None

# Fonction pour récupérer les données
def view_all_data():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM insurance ORDER BY id ASC")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    else:
        return []