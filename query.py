import mysql.connector
import streamlit as st

# Connexion à la base de données
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="",
            port=,
            user="",
            passwd="",  # Tu peux mettre ton mot de passe ici
            database=""
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
        cursor.execute("")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    else:
        return []
