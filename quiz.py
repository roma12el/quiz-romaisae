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
# IMAGE D’EN-TÊTE
# =========================
try:
    st.image("pag de garde.png", use_container_width=True)
except Exception:
    st.warning("⚠️ Image d’en-tête introuvable (pag de garde.png).")

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
if st.button("Soumettre mes réponses"):
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

        # NOTE SUR 20
        note_sur_20 = round((score / total) * 20, 2)
        color = "#4CAF50" if note_sur_20 >= 16 else "#FFC107" if note_sur_20 >= 10 else "#F44336"

        st.markdown(f"""
        <div style="background-color: #e0e0e0; border-radius: 15px; padding: 10px; width: 300px; text-align: center;">
            <div style="width: {note_sur_20*5}%; background-color: {color}; padding: 15px 0; border-radius: 15px; font-size: 24px; font-weight: bold; color: white;">
                {note_sur_20} / 20
            </div>
        </div>
        """, unsafe_allow_html=True)

# =========================
# SECTION PROFESSEUR
# =========================
st.divider()
st.subheader("Résultats et Statistiques")

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

        # --- HISTOGRAMME INTERACTIF EN PREMIER ---
        top3 = classement.head(3).reset_index(drop=True)
        rangs = ["🥇 Première place", "🥈 Deuxième place", "🥉 Troisième place"]
        top3["Rang"] = rangs[:len(top3)]

        st.subheader("🏆 Classement des 3 premiers")
        fig = px.bar(
            top3, x="Nom", y="Score", color="Rang", text="Score",
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

        # --- TABLEAU DES RÉSULTATS COMPLET ---
        st.subheader("Détails des résultats")
        st.dataframe(classement, use_container_width=True)

        gagnant = classement.iloc[0]
        st.markdown(f"🏅 **{gagnant['Nom']}** est premier avec un score de {gagnant['Score']}/{len(questions)}")

        # --- ANALYSE DES QUESTIONS ---
        question_scores = {q: df[q].mean() * 100 for q in questions}
        stats_df = pd.DataFrame({
            "Question": list(question_scores.keys()),
            "Taux de réussite (%)": list(question_scores.values())
        })

        st.bar_chart(stats_df.set_index("Question"))
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




