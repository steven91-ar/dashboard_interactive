import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from query import *  # Assurez-vous que view_all_data() est bien défini ici
import time

# Config de la page
st.set_page_config(page_title="Tableau de bord", page_icon="🌏", layout="wide")
st.subheader("⚠ Analyse descriptive des assurances")
st.markdown("##")

# Chargement des données depuis MySQL ou autre
result = view_all_data()
df = pd.DataFrame(result, columns=["Police", "Expiration", "Localisation", "État", "Région", "Investissement", "Construction", "Type d'entreprise", "Séisme", "Inondation", "Évaluation", "id"])

# 🔧 Sécurité : convertir les colonnes numériques
df["Investissement"] = pd.to_numeric(df["Investissement"], errors='coerce')
df["Évaluation"] = pd.to_numeric(df["Évaluation"], errors='coerce')

# Sidebar
st.sidebar.image("data/logo1.png", caption="Analyses en ligne")

st.sidebar.header("Veuillez filtrer")
state = st.sidebar.multiselect("SÉLECTIONNER L'ÉTAT", options=df["État"].unique(), default=df["État"].unique())
location = st.sidebar.multiselect("SÉLECTIONNER LA LOCALISATION", options=df["Localisation"].unique(), default=df["Localisation"].unique())
construction = st.sidebar.multiselect("SÉLECTIONNER LA CONSTRUCTION", options=df["Construction"].unique(), default=df["Construction"].unique())

# Filtrage des données
df_selection = df.query("État == @state & Localisation == @location & Construction == @construction")

# Fonction Accueil : KPIs et tableau
def Accueil():
    with st.expander("AFFICHER LE JEU DE DONNÉES"):
        showData = st.multiselect('Filtrer :', df_selection.columns, default=df_selection.columns)
        st.dataframe(df_selection[showData], use_container_width=True)

    total_investment = df_selection["Investissement"].sum()
    investment_mode = df_selection["Investissement"].mode()[0] if not df_selection["Investissement"].mode().empty else 0
    investment_mean = df_selection["Investissement"].mean()
    investment_median = df_selection["Investissement"].median()
    rating = df_selection["Évaluation"].sum()

    total1, total2, total3, total4, total5 = st.columns(5, gap='small')

    with total1:
        st.info('Somme des investissements', icon="💰")
        st.metric("Somme TZS", f"{total_investment:,.0f}")

    with total2:
        st.info('Investissement le plus élevé', icon="💰")
        st.metric("Mode TZS", f"{investment_mode:,.0f}")

    with total3:
        st.info('Moyenne', icon="💰")
        st.metric("Moyenne TZS", f"{investment_mean:,.0f}")

    with total4:
        st.info('Gains centraux', icon="💰")
        st.metric("Médiane TZS", f"{investment_median:,.0f}")

    with total5:
        st.info('Évaluations', icon="📊")
        st.metric("Évaluation", numerize(rating), help=f"Évaluation totale : {rating}")

    st.markdown("""---""")

# Graphiques
def graphiques():
    investment_by_business_type = df_selection.groupby("Type d'entreprise").count()[["Investissement"]].sort_values("Investissement")
    fig_investment = px.bar(
        investment_by_business_type,
        x="Investissement",
        y=investment_by_business_type.index,
        orientation="h",
        title="<b>INVESTISSEMENT PAR TYPE D'ENTREPRISE</b>",
        color_discrete_sequence=["#0083B8"] * len(investment_by_business_type),
        template="plotly_white",
    )
    fig_investment.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="black"),
        xaxis=dict(showgrid=True, gridcolor="#cecdcd"),
        yaxis=dict(showgrid=True, gridcolor="#cecdcd"),
    )

    investment_state = df_selection.groupby("État").count()[["Investissement"]]
    fig_state = px.line(
        investment_state,
        x=investment_state.index,
        y="Investissement",
        title="<b>INVESTISSEMENT PAR ÉTAT</b>",
        color_discrete_sequence=["#0083B8"],
        template="plotly_white",
    )
    fig_state.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=False),
    )

    left, right = st.columns(2)
    left.plotly_chart(fig_state, use_container_width=True)
    right.plotly_chart(fig_investment, use_container_width=True)

# Barre de progression vers un objectif
def BarreDeProgression():
    st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00); }</style>""", unsafe_allow_html=True)
    target = 3_000_000_000
    current = df_selection["Investissement"].sum()
    percent = round((current / target) * 100)
    mybar = st.progress(0)

    if percent > 100:
        st.subheader("✅ Objectif atteint !")
    else:
        st.write(f"Vous avez atteint {percent}% de {format(target, ',d')} TZS")
        for i in range(percent):
            time.sleep(0.01)
            mybar.progress(i + 1, text=" Pourcentage de l'objectif")

# Menu latéral
def menuLateral():
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu Principal",
            options=["Accueil", "Progression"],
            icons=["house", "eye"],
            menu_icon="cast",
            default_index=0
        )

    if selected == "Accueil":
        Accueil()
        graphiques()
    elif selected == "Progression":
        BarreDeProgression()
        graphiques()

# Exécution principale
menuLateral()

# Masquer le style par défaut Streamlit
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)