import streamlit as st
import pandas as pd
from io import BytesIO
import qrcode
import os

# =========================
# CONFIGURATION DE LA PAGE
# =========================
st.set_page_config(page_title="Quiz Interactif 🎓", page_icon="🎯", layout="centered")
st.title("🎯 Quiz Interactif – Par Romaisae")

# =========================
# QUESTIONS DU QUIZ
# =========================
questions = {
    "1️⃣ Quelle est la capitale du Maroc ?": ["Rabat", "Casablanca", "Marrakech", "Rabat"],
    "2️⃣ Combien font 7 + 5 ?": ["10", "11", "12", "12"],
    "3️⃣ Quelle devise utilise-t-on au Maroc ?": ["Euro", "Dollar", "Dirham", "Dirham"],
    "4️⃣ Qui régule le marché financier au Maroc ?": ["AMMC", "BAM", "AMF", "AMMC"],
    "5️⃣ Quelle est la couleur du drapeau marocain ?": ["Rouge et vert", "Bleu et blanc", "Rouge et jaune", "Rouge et vert"],
    "6️⃣ Combien de continents existe-t-il ?": ["5", "6", "7", "7"],
    "7️⃣ Python est un ...": ["Langage de programmation", "Reptile", "Logiciel", "Langage de programmation"],
    "8️⃣ Quel est le résultat de 9 * 9 ?": ["81", "72", "99", "81"],
    "9️⃣ Quelle est la capitale de la France ?": ["Lyon", "Paris", "Marseille", "Paris"],
    "🔟 En quelle année a été créée l’AMMC ?": ["2016", "2014", "2018", "2016"]
}

# =========================
# IDENTITÉ DE L'UTILISATEUR
# =========================
st.subheader("🧑 Identifiez-vous avant de commencer")
nom = st.text_input("Nom et prénom :")
email = st.text_input("Adresse e-mail (facultative) :")

# =========================
# QUIZ
# =========================
score = 0
st.divider()
st.write("📝 Répondez aux questions ci-dessous :")

for question, options in questions.items():
    reponse = st.radio(question, options[:-1], key=question)
    if reponse == options[-1]:
        score += 1

# =========================


# =========================
# PARTAGE QR CODE
# =========================
st.divider()
st.subheader("📱 Partage du quiz")

url = "https://romaisae-quiz.streamlit.app"  # ⚠️ À modifier après déploiement
qr = qrcode.make(url)
buf = BytesIO()
qr.save(buf, format="PNG")
st.image(buf.getvalue(), caption="Scannez pour participer au quiz 📲", width=200)
st.write("Ou cliquez directement ici :", f"[{url}]({url})")




