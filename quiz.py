import streamlit as st
import pandas as pd
from io import BytesIO
import qrcode
import os
import matplotlib.pyplot as plt

# =========================
# CONFIGURATION DE LA PAGE
# =========================
# =========================
# AFFICHAGE DE L'IMAGE D'EN-TÊTE
# =========================
st.image("pag de garde.png", use_container_width=True)

st.set_page_config(page_title="Quiz – Réglementation des Marchés Financiers", layout="centered")
st.title("Quiz sur la Réglementation des Marchés Financiers et Rôle des Autorités de Marché")

# =========================
# QUESTIONS DU QUIZ
# =========================
« Questions : (une seule chose correcte parmi) = {
    "1️⃣ Quelle institution supervise le marché financier au Maroc ?":
        ["Bank Al-Maghrib", "Ministère des Finances", "AMMC", "CDG", "AMMC"],

    "2️⃣ Quelle est la principale mission de l’AMMC ?":
        ["Contrôler la fiscalité", "Protéger les investisseurs", "Émettre la monnaie", "Fixer les taux d’intérêt", "Protéger les investisseurs"],

    "3️⃣ Quelle autorité est responsable de la politique monétaire ?":
        ["AMMC", "Bank Al-Maghrib", "CDVM", "CMR", "Bank Al-Maghrib"],

    "4️⃣ Quelle loi encadre le marché des valeurs mobilières au Maroc ?":
        ["Loi 12-03", "Loi 43-12", "Loi 17-95", "Loi 20-19", "Loi 43-12"],

    "5️⃣ Quel est le rôle principal d’une autorité financière ?":
        ["Favoriser la spéculation", "Réguler et contrôler les marchés", "Fixer les prix des actions", "Protéger les banques", "Réguler et contrôler les marchés"],

    "6️⃣ Quelle entité veille à la stabilité du système bancaire marocain ?":
        ["Bank Al-Maghrib", "AMMC", "Ministère du Commerce", "Trésor Général du Royaume", "Bank Al-Maghrib"],

    "7️⃣ Quelle institution gère les cotations à la Bourse de Casablanca ?":
        ["AMMC", "Bourse de Casablanca", "Bank Al-Maghrib", "CDVM", "Bourse de Casablanca"],

    "8️⃣ Quelle est la mission du Conseil Déontologique des Valeurs Mobilières (CDVM) avant sa transformation ?":
        ["Régulation du marché financier", "Supervision des banques", "Audit des entreprises publiques", "Fiscalité des investisseurs", "Régulation du marché financier"],

    "9️⃣ Quelle autorité veille à la transparence de l’information financière ?":
        ["AMMC", "ONCF", "Ministère de l’Intérieur", "BAM", "AMMC"],

    "🔟 Quelle est la principale finalité de la réglementation des marchés financiers ?":
        ["Limiter la concurrence", "Protéger les investisseurs et assurer la confiance", "Encourager les monopoles", "Réduire les taux d’intérêt", "Protéger les investisseurs et assurer la confiance"]
}

# =========================
# IDENTITÉ DE L'UTILISATEUR
# =========================
st.subheader("Veuillez saisir votre nom et prénom.")
nom = st.text_input("Nom et prénom :")

# =========================
# QUIZ
# =========================
st.divider()
st.write("Veuillez répondre à toutes les questions :")

reponses = {}
score = 0

for question, options in questions.items():
    reponse = st.radio(question, options[:-1], key=question)
    reponses[question] = reponse
    if reponse == options[-1]:
        score += 1

# =========================
# SOUMISSION DU QUIZ
# =========================
if st.button("Soumettre mes réponses"):
    if nom.strip() == "":
        st.warning("Veuillez entrer votre nom et prénom avant de soumettre.")
    else:
        total = len(questions)
        pourcentage = round((score / total) * 100, 2)

        # Préparer la ligne de données
        result = {q: (1 if reponses[q] == questions[q][-1] else 0) for q in questions}
        data_row = {"Nom": nom, "Score": score, "Pourcentage": pourcentage, **result}

        # Gestion du fichier CSV
        try:
            if os.path.exists("scores.csv") and os.path.getsize("scores.csv") > 0:
                df_old = pd.read_csv("scores.csv")
            else:
                df_old = pd.DataFrame(columns=["Nom", "Note", "Pourcentage", *questions.keys()])
        except (pd.errors.EmptyDataError, FileNotFoundError):
            df_old = pd.DataFrame(columns=["Nom", "Note", "Pourcentage", *questions.keys()])

        df = pd.concat([df_old, pd.DataFrame([data_row])], ignore_index=True)
        df.to_csv("scores.csv", index=False)

        # Résultat du participant
        st.success(f"{nom}, votre score est de {pourcentage}% ({score}/{total}).")

        # =========================
    # STATISTIQUES PERSONNELLES
# =========================
st.divider()
st.subheader("Résultats du quiz")

# Calcul de la note sur 20
Note_sur_20 = round((Note / total) * 20, 2)  # 2 décimales

# Couleur selon la performance
if Note_sur_20 >= 16:
    color = "#4CAF50"  # vert
elif Note_sur_20 >= 10:
    color = "#FFC107"  # orange
else:
    color = "#F44336"  # rouge

# Affichage stylé avec barre de progression
st.markdown(f"""
<div style="
    background-color: #e0e0e0; 
    border-radius: 15px; 
    padding: 10px; 
    width: 300px; 
    text-align: center;
">
    <div style="
        width: {Note_sur_20*5}%; 
        background-color: {color}; 
        padding: 15px 0; 
        border-radius: 15px; 
        font-size: 24px; 
        font-weight: bold;
        color: white;
    ">
        {Note_sur_20} / 20
    </div>
</div>
""", unsafe_allow_html=True)

        # =========================
        # SECTION PROFESSEUR
        # =========================
        st.divider()
        st.subheader("Résultats et Statistiques")
        password = st.text_input("Mot de passe enseignant :", type="password")

        if password == "prof2025":
            st.success("Accès autorisé")

            df = pd.read_csv("scores.csv")
            classement = df.sort_values(by="Score", ascending=False).reset_index(drop=True)
            st.dataframe(classement, use_container_width=True)

            gagnant = classement.iloc[0]
            st.markdown(f"Gagnant actuel : **{gagnant['Nom']}** avec un score de {gagnant['Note']}/{total}")

            st.subheader("Statistiques globales par question")
            question_scores = {q: df[q].mean() * 100 for q in questions}
            stats_df = pd.DataFrame({
                "Question": list(question_scores.keys()),
                "Taux de réussite (%)": list(question_scores.values())
            })
            st.bar_chart(stats_df.set_index("Question"))

            moyenne_globale = round(df["Pourcentage"].mean(), 2)
            st.info(f"Taux de réussite moyen de l’ensemble des participants : {moyenne_globale}%")

            meilleure = stats_df.loc[stats_df["Taux de réussite (%)"].idxmax()]
            pire = stats_df.loc[stats_df["Taux de réussite (%)"].idxmin()]
            st.success(f"Question la plus réussie : {meilleure['Question']} ({meilleure['Taux de réussite (%)']:.1f}%)")
            st.error(f"Question la moins réussie : {pire['Question']} ({pire['Taux de réussite (%)']:.1f}%)")
        else:
            if password:
                st.error("Mot de passe incorrect.")

# =========================
# PARTAGE DU QUIZ
# =========================
st.divider()
st.subheader("QR Code")

url = "https://romaquiz.streamlit.app/"  # à adapter
qr = qrcode.make(url)
buf = BytesIO()
qr.save(buf, format="PNG")
st.image(buf.getvalue(), caption="Scannez pour accéder au quiz", width=200)
st.write("Ou cliquez sur ce lien :", f"[{url}]({url})")




