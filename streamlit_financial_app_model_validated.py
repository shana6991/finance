
import streamlit as st
import pandas as pd
import numpy as np

# Valeurs réelles pour 588 CHF à différents taux de rendement
real_values_588_4_percent = np.array([
    2286, 4723, 7294, 10003, 12857, 20651, 28849, 37488, 46593, 56184,
    66287, 76928, 88133, 99930, 112348, 125418, 139173, 153645, 168870, 184885,
    201727, 219436, 238054, 257626, 278196, 299815, 322531, 346397, 371469, 397805,
    425467, 454520, 485032, 517073, 556753
])

real_values_588_7_percent = np.array([
    2321, 4867, 7628, 10622, 13867, 22245, 31310, 41138, 51790, 63334,
    75842, 89393, 104072, 119969, 137185, 155825, 176005, 197848, 221489, 247071,
    274751, 304697, 337090, 372124, 410013, 450984, 495281, 543171, 594938, 650893,
    711369, 776726, 847353, 923668, 1016927
])

# Ratios dynamiques basés sur les valeurs réelles 300 CHF par rapport à 588 CHF
real_values_300 = np.array([
    1130, 2388, 3752, 5232, 6835, 11053, 15617, 20565, 25928, 31740,
    38037, 44860, 52250, 60254, 68921, 78306, 88466, 99463, 111366, 124246,
    138183, 153260, 169569, 187209, 206286, 226914, 249217, 273330, 299395, 327568,
    358018, 390926, 426487, 464912, 511869
])

ratios_dynamic_300_588 = real_values_300 / real_values_588_7_percent

# Fonction pour appliquer le modèle validé
def refined_model(base_values, ratios_dynamic, contribution):
    refined_values = base_values * (
        0.5 * ratios_dynamic * (contribution / 300) + 0.5 * (contribution / 588)
    )
    return refined_values

# Application Streamlit
st.title("Prédictions des Valeurs de Rachat avec Modèle Validé")
st.write("Cet outil permet de prédire les valeurs de rachat pour une prime mensuelle donnée, en utilisant un modèle basé sur les données réelles.")

# Entrée utilisateur
contribution = st.number_input("Montant de la prime mensuelle (CHF)", min_value=100, max_value=1000, step=10, value=350)
taux_rendement = st.selectbox("Choisissez un taux de rendement (%)", [4, 7])

# Sélection des valeurs réelles en fonction du taux de rendement
if taux_rendement == 4:
    real_values_base = real_values_588_4_percent
else:
    real_values_base = real_values_588_7_percent

# Calcul des valeurs affinées
refined_values = refined_model(real_values_base, ratios_dynamic_300_588, contribution)

# Création du tableau des résultats
years = np.arange(2026, 2061)
results_df = pd.DataFrame({
    "Année": years,
    "Valeur prédite (CHF)": refined_values
})

# Affichage des résultats
st.write("### Résultats des prédictions")
st.dataframe(results_df)

# Option de téléchargement
csv = results_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Télécharger les résultats (CSV)",
    data=csv,
    file_name="valeurs_rachats_predictions.csv",
    mime="text/csv"
)
