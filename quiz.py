import streamlit as st
import pandas as pd
from io import BytesIO
import qrcode
import os
import matplotlib.pyplot as plt
import plotly.express as px

# =========================
# CONFIGURATION DE LA PAGE
# =========================
st.set_page_config(
    page_title="Quiz – Réglementation des Marchés Financiers",
    layout="centered"
)

# =========================
# STYLE GLOBAL MODERNE
# =========================
st.markdown("""
    <style>
    /* Arrière-plan dégradé doux */
    .stApp {
        background: linear-gradient(135deg, #f0f4ff, #e8f0fe);
    }

    /* Titres */
    h1, h2, h3 {
        color: #1e3a8a !important;
        font-family: 'Poppins', sans-serif;
    }

    /* Questions */
    .stRadio > div {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 12px;
    }

    /* Boutons stylisés */
    button[kind="primary"] {
        background-color: #3B82F6 !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        border: none !important;
        transition: 0.3s;
    }
    button[kind="primary"]:hover {
        background-color: #2563eb !important;
        transform: scale(1.03);
    }

    /* Carte de note */
    .note-bar {
        width: 300px;
        border-radius: 12px;
        overflow: hidden;
        background: #ddd;
        margin: 15px auto;
    }
    .note-fill {
        height: 40px;
        text-align: center;
        font-weight: bold;
        color: white;
        line-height: 40px;
        border-radius: 12px;
    }

    /* Tableau moderne */
    div[data-testid="stDataFrame"] table {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #ccc;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# IMAGE D’EN-TÊTE
# =========================
try:
    st.image("pag de garde.png", use_container_width=True)
except Exception:
    st.warning("⚠️ Image d’en-tête introuvable (pag de garde.png).")

st.markdown("""
    <h2 style='text-align:center; color:#1e40af; font-weight:bold;'>
    🎓 Testez vos connaissances sur la réglementation des marchés financiers !
    </h2>
""", unsafe_allow_html=True)

st.title("Quiz sur la Réglementation des Marchés Financiers et Rôle des Autorités de Marché ")

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
# IDENTITÉ UTILISATEUR
# =========================
st.subheader("Veuillez saisir vos informations")

col1, col2 = st.columns([2, 1])
with col1:
    nom = st.text_input("Nom et prénom :")

with col2:
    st.write("**Genre :**")
    colf, colm = st.columns(2)
    with colf:
        if st.button("👩 Féminin"):
            st.session_state["genre"] = "Féminin"
    with colm:
        if st.button("👨 Masculin"):
            st.session_state["genre"] = "Masculin"

genre = st.session_state.get("genre", "Non spécifié")
st.info(f"Genre sélectionné : **{genre}**")

# =========================
# QUIZ
# =========================
st.divider()
st.write("Répondez à toutes les questions (une seule réponse possible) :")

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
if st.button("📝 Soumettre mes réponses"):
    if nom.strip() == "":
        st.warning("Veuillez entrer votre nom et prénom avant de soumettre.")
    else:
        total = len(questions)
        pourcentage = round((score / total) * 100, 2)

        result = {q: (1 if reponses[q] == questions[q][-1] else 0) for q in questions}
        data_row = {"Nom": nom, "Genre": genre, "Score": score, "Pourcentage": pourcentage, **result}

        try:
            if os.path.exists("scores.csv") and os.path.getsize("scores.csv") > 0:
                df_old = pd.read_csv("scores.csv")
            else:
                df_old = pd.DataFrame(columns=["Nom", "Genre", "Score", "Pourcentage", *questions.keys()])
        except Exception:
            df_old = pd.DataFrame(columns=["Nom", "Genre", "Score", "Pourcentage", *questions.keys()])

        df = pd.concat([df_old, pd.DataFrame([data_row])], ignore_index=True)

        try:
            df.to_csv("scores.csv", index=False)
        except Exception:
            st.warning("⚠️ Impossible d’enregistrer les résultats (vérifiez les permissions).")

        st.success(f"{nom}, votre score est de {pourcentage}% ({score}/{total}).")

        # NOTE SUR 20 (design moderne)
        note_sur_20 = round((score / total) * 20, 2)
        color = "#4CAF50" if note_sur_20 >= 16 else "#FFC107" if note_sur_20 >= 10 else "#F44336"

        st.markdown(f"""
        <div style="
            background-color:white;
            padding:20px;
            border-radius:15px;
            box-shadow:0px 4px 15px rgba(0,0,0,0.1);
            text-align:center;
            width:320px;
            margin:auto;
        ">
            <h3 style="color:#1e3a8a;">🎯 Votre note finale</h3>
            <div class="note-bar">
                <div class="note-fill" style="width:{note_sur_20*5}%; background-color:{color};">
                    {note_sur_20} / 20
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# =========================
# SECTION PROFESSEUR
# =========================
st.divider()
st.subheader("📊 Résultats et Statistiques")
password = st.text_input("Mot de passe :", type="password")

if password == "prof2025":
    st.success("✅ Accès autorisé")

    try:
        if os.path.exists("scores.csv") and os.path.getsize("scores.csv") > 0:
            df = pd.read_csv("scores.csv")
        else:
            df = pd.DataFrame(columns=["Nom", "Genre", "Score", "Pourcentage", *questions.keys()])
    except Exception:
        st.error("❌ Erreur lors du chargement des données.")
        df = pd.DataFrame(columns=["Nom", "Genre", "Score", "Pourcentage", *questions.keys()])

    if not df.empty:
        classement = df.sort_values(by="Score", ascending=False).reset_index(drop=True)

        top3 = classement.head(3).reset_index(drop=True)
        rangs = ["🥇 Première place", "🥈 Deuxième place", "🥉 Troisième place"]
        top3["Rang"] = rangs[:len(top3)]

        st.subheader("🏆 Classement des 3 premiers")
        fig = px.bar(
            top3,
            x="Nom",
            y="Score",
            color="Rang",
            text="Score",
            color_discrete_map={
                "🥇 Première place": "gold",
                "🥈 Deuxième place": "silver",
                "🥉 Troisième place": "#cd7f32"
            },
            title="🏅 Les 3 meilleures notes du quiz"
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(xaxis_title="Participants", yaxis_title="Score", showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📋 Détails des résultats")
        st.dataframe(classement, use_container_width=True)

        gagnant = classement.iloc[0]
        st.markdown(f"🏅 **{gagnant['Nom']}** est premier avec un score de {gagnant['Score']}/{len(questions)}")

        # --- GRAPHIQUE MODERNE DES QUESTIONS ---
        question_scores = {q: df[q].mean() * 100 for q in questions}
        stats_df = pd.DataFrame({
            "Question": list(question_scores.keys()),
            "Taux de réussite (%)": list(question_scores.values())
        })

        fig2 = px.bar(
            stats_df,
            x="Question",
            y="Taux de réussite (%)",
            text="Taux de réussite (%)",
            color="Taux de réussite (%)",
            color_continuous_scale="Blues",
            title="📈 Taux de réussite par question"
        )
        fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig2.update_layout(xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig2, use_container_width=True)

        moyenne_globale = round(df["Pourcentage"].mean(), 2)
        st.info(f"📊 Taux de réussite moyen : **{moyenne_globale}%**")

        meilleure = stats_df.loc[stats_df["Taux de réussite (%)"].idxmax()]
        pire = stats_df.loc[stats_df["Taux de réussite (%)"].idxmin()]
        st.success(f"✅ Question la plus réussie : {meilleure['Question']} ({meilleure['Taux de réussite (%)']:.1f}%)")
        st.error(f"⚠️ Question la moins réussie : {pire['Question']} ({pire['Taux de réussite (%)']:.1f}%)")

elif password:
    st.error("Mot de passe incorrect.")

# =========================
# QR CODE PARTAGE
# =========================
st.divider()
st.subheader("QR Code")

url = "https://fads-quiz.app/"
qr = qrcode.make(url)
buf = BytesIO()
qr.save(buf, format="PNG")
st.image(buf.getvalue(), caption="Scannez pour accéder au quiz", width=200)
st.write("Ou cliquez sur ce lien :", f"[{url}]({url})")











