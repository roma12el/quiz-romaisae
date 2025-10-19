import streamlit as st
import pandas as pd
from io import BytesIO
import qrcode
import os
import matplotlib.pyplot as plt

# =========================
# CONFIGURATION DE LA PAGE
# =========================
st.set_page_config(
    page_title="Quiz – Réglementation des Marchés Financiers",
    layout="centered"
)

# =========================
# AFFICHAGE DE L'IMAGE D'EN-TÊTE
# =========================
st.image("pag de garde.png", use_container_width=True)
st.title("Quiz sur la Réglementation des Marchés Financiers et Rôle des Autorités de Marché")

# =========================
# QUESTIONS DU QUIZ
# =========================
questions = {
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

col1, col2 = st.columns([2, 1])
with col1:
    nom = st.text_input("Nom et prénom :")

# 🔹 Ajout du champ Genre avec logos jolis
with col2:
    st.write("**Genre :**")
    colf, colm = st.columns(2)
    with colf:
        st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=60)
        if st.button("Féminin 💖"):
            st.session_state["genre"] = "Féminin"
    with colm:
        st.image("https://cdn-icons-png.flaticon.com/512/4140/4140037.png", width=60)
        if st.button("Masculin 💪"):
            st.session_state["genre"] = "Masculin"

genre = st.session_state.get("genre", "Non spécifié")
st.info(f"👤 Genre sélectionné : **{genre}**")

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
        data_row = {"Nom": nom, "Genre": genre, "Score": score, "Pourcentage": pourcentage, **result}

        # Gestion sécurisée du fichier CSV
        if os.path.exists("scores.csv") and os.path.getsize("scores.csv") > 0:
            try:
                df_old = pd.read_csv("scores.csv")
            except pd.errors.EmptyDataError:
                df_old = pd.DataFrame(columns=["Nom", "Genre", "Score", "Pourcentage", *questions.keys()])
        else:
            df_old = pd.DataFrame(columns=["Nom", "Genre", "Score", "Pourcentage", *questions.keys()])

        df = pd.concat([df_old, pd.DataFrame([data_row])], ignore_index=True)
        df.to_csv("scores.csv", index=False)

        st.success(f"{nom}, votre score est de {pourcentage}% ({score}/{total}).")

        # =========================
        # STATISTIQUES PERSONNELLES
        # =========================
        st.divider()
        st.subheader("Résultats du quiz")

        note_sur_20 = round((score / total) * 20, 2)
        if note_sur_20 >= 16:
            color = "#4CAF50"
        elif note_sur_20 >= 10:
            color = "#FFC107"
        else:
            color = "#F44336"

        st.markdown(f"""
        <div style="
            background-color: #e0e0e0; 
            border-radius: 15px; 
            padding: 10px; 
            width: 300px; 
            text-align: center;
        ">
            <div style="
                width: {note_sur_20*5}%; 
                background-color: {color}; 
                padding: 15px 0; 
                border-radius: 15px; 
                font-size: 24px; 
                font-weight: bold;
                color: white;
            ">
                {note_sur_20} / 20
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

    if os.path.exists("scores.csv") and os.path.getsize("scores.csv") > 0:
        try:
            df = pd.read_csv("scores.csv")
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=["Nom", "Genre", "Score", "Pourcentage", *questions.keys()])
    else:
        df = pd.DataFrame(columns=["Nom", "Genre", "Score", "Pourcentage", *questions.keys()])

    if not df.empty:
        classement = df.sort_values(by="Score", ascending=False).reset_index(drop=True)
        st.dataframe(classement, use_container_width=True)

        gagnant = classement.iloc[0]
        st.markdown(f"Gagnant actuel : **{gagnant['Nom']}** avec un score de {gagnant['Score']}/{len(questions)}")

        # 🔹 Histogramme interactif Top 3
        top3 = classement.head(3)
        top3["Rang"] = ["🥇 Première place", "🥈 Deuxième place", "🥉 Troisième place"]

        st.subheader("🏆 Classement des 3 premiers")
        st.table(top3[["Rang", "Nom", "Genre", "Score", "Pourcentage"]])

        fig, ax = plt.subplots()
        ax.bar(top3["Nom"], top3["Score"], color=["gold", "silver", "#cd7f32"])
        ax.set_title("🏅 Top 3 des meilleurs participants")
        ax.set_xlabel("Participants")
        ax.set_ylabel("Score sur 20")
        st.pyplot(fig)

        # Statistiques par question
        question_scores = {q: df[q].mean() * 100 for q in questions}
        stats_df = pd.DataFrame({
            "Question": list(question_scores.keys()),
            "Taux de réussite (%)": list(question_scores.values())
        })
        st.bar_chart(stats_df.set_index("Question"))

        moyenne_globale = round(df["Pourcentage"].mean(), 2)
        st.info(f"Taux de réussite moyen : {moyenne_globale}%")

        meilleure = stats_df.loc[stats_df["Taux de réussite (%)"].idxmax()]
        pire = stats_df.loc[stats_df["Taux de réussite (%)"].idxmin()]
        st.success(f"Question la plus réussie : {meilleure['Question']} ({meilleure['Taux de réussite (%)']:.1f}%)")
        st.error(f"Question la moins réussie : {pire['Question']} ({pire['Taux de réussite (%)']:.1f}%)")
elif password:
    st.error("Mot de passe incorrect.")

# =========================
# PARTAGE DU QUIZ
# =========================
st.divider()
st.subheader("QR Code")

url = "https://romaquiz.streamlit.app/"
qr = qrcode.make(url)
buf = BytesIO()
qr.save(buf, format="PNG")
st.image(buf.getvalue(), caption="Scannez pour accéder au quiz", width=200)
st.write("Ou cliquez sur ce lien :", f"[{url}]({url})")





