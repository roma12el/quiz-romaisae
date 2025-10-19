import streamlit as st
import pandas as pd
from io import BytesIO
import qrcode
import os
import matplotlib.pyplot as plt

# =========================
# CONFIGURATION DE LA PAGE
# =========================
st.set_page_config(page_title="🎯 Quiz Interactif – Par Romaisae", page_icon="🎓", layout="centered")
st.title("🎓 Quiz Interactif – Par Romaisae")

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
st.divider()
st.write("📝 Répondez aux questions ci-dessous :")

reponses = {}
score = 0

for question, options in questions.items():
    reponse = st.radio(question, options[:-1], key=question)
    reponses[question] = reponse
    if reponse == options[-1]:
        score += 1

# =========================
# SOUMISSION DES RÉPONSES
# =========================
if st.button("✅ Soumettre mes réponses"):
    if nom.strip() == "":
        st.warning("⚠️ Veuillez entrer votre nom avant de soumettre.")
    else:
        # Calcul du score
        total = len(questions)
        pourcentage = round((score / total) * 100, 2)

        # Sauvegarde dans le CSV
        result = {q: (1 if reponses[q] == questions[q][-1] else 0) for q in questions}
        data_row = {"Nom": nom, "Email": email, "Score": score, "Pourcentage": pourcentage, **result}

        if os.path.exists("scores.csv") and os.path.getsize("scores.csv") > 0:
            df_old = pd.read_csv("scores.csv")
            df = pd.concat([df_old, pd.DataFrame([data_row])], ignore_index=True)
        else:
            df = pd.DataFrame([data_row])

        df.to_csv("scores.csv", index=False)

        # Résultats pour le participant
        st.success(f"🎉 Bravo {nom} ! Ton score est **{score}/10 ({pourcentage}%)**")

        # Médaille si score parfait
        if score == len(questions):
            st.markdown("🏅 **Félicitations ! Tu obtiens la Médaille d'Or du Quiz !** 🥇")
        elif score >= 8:
            st.markdown("🥈 Excellent ! Médaille d’Argent !")
        elif score >= 6:
            st.markdown("🥉 Bon travail ! Médaille de Bronze !")
        else:
            st.markdown("💪 Continue de t'entraîner, tu y es presque !")

        # =========================
        # STATISTIQUES DU PARTICIPANT
        # =========================
        st.divider()
        st.subheader("📊 Tes statistiques personnelles")

        fig, ax = plt.subplots()
        labels = ['Bonnes réponses', 'Mauvaises réponses']
        values = [score, len(questions) - score]
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        st.pyplot(fig)

        # =========================
        # SECTION PROFESSEUR
        # =========================
        st.divider()
        st.subheader("🔒 Section Professeur – Classement et Statistiques Globales")
        password = st.text_input("Mot de passe professeur :", type="password")

        if password == "prof2025":
            st.success("🔓 Accès autorisé")

            if os.path.exists("scores.csv"):
                df = pd.read_csv("scores.csv")

                # Classement
                classement = df.sort_values(by="Score", ascending=False).reset_index(drop=True)
                st.dataframe(classement, use_container_width=True)

                # Gagnant
                gagnant = classement.iloc[0]
                st.markdown(f"🏆 **Gagnant actuel : {gagnant['Nom']}** – {gagnant['Score']}/10")

                # Statistiques globales
                st.subheader("📈 Statistiques globales par question")

                question_scores = {q: df[q].mean() * 100 for q in questions}
                stats_df = pd.DataFrame({
                    "Question": list(question_scores.keys()),
                    "Taux de réussite (%)": list(question_scores.values())
                })

                st.bar_chart(stats_df.set_index("Question"))

                # Taux de réussite moyen global
                moyenne_globale = round(df["Pourcentage"].mean(), 2)
                st.info(f"📊 Taux de réussite moyen de tous les participants : **{moyenne_globale}%**")

                # Questions les plus et moins réussies
                meilleure = stats_df.loc[stats_df["Taux de réussite (%)"].idxmax()]
                pire = stats_df.loc[stats_df["Taux de réussite (%)"].idxmin()]
                st.success(f"✅ Question la plus réussie : *{meilleure['Question']}* ({meilleure['Taux de réussite (%)']:.1f}%)")
                st.error(f"❌ Question la moins réussie : *{pire['Question']}* ({pire['Taux de réussite (%)']:.1f}%)")
            else:
                st.warning("Aucun résultat enregistré pour le moment.")
        else:
            if password:
                st.error("Mot de passe incorrect.")

# =========================
# PARTAGE QR CODE
# =========================
st.divider()
st.subheader("📱 Partage du quiz")

url = "https://romaquiz.streamlit.app/"  # ⚠️ à modifier après déploiement
qr = qrcode.make(url)
buf = BytesIO()
qr.save(buf, format="PNG")
st.image(buf.getvalue(), caption="Scannez pour participer 📲", width=200)
st.write("Ou cliquez ici :", f"[{url}]({url})")
