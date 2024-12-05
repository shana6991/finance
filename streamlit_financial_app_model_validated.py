
import streamlit as st
import pandas as pd
import numpy as np

# Valeurs réelles pour 588 CHF à différents taux de rendement
real_values_588_base = np.array([
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

ratios_dynamic_300_588 = real_values_300 / real_values_588_base

# Fonction pour appliquer le modèle validé
def refined_model(base_values, ratios_dynamic, contribution, interest_rate, years):
    # Ajuster les valeurs réelles pour correspondre au taux d'intérêt personnalisé
    adjusted_values = base_values * (interest_rate / 7)
    refined_values = adjusted_values[:years] * (
        0.5 * ratios_dynamic[:years] * (contribution / 300) + 0.5 * (contribution / 588)
    )
    return refined_values

# Application Streamlit
st.title("Prédictions des Valeurs de Rachat avec Modèle Validé")
st.write("Cet outil permet de prédire les valeurs de rachat pour une prime mensuelle donnée, en utilisant un modèle basé sur les données réelles.")

# Entrées utilisateur
contribution = st.number_input("Montant de la prime mensuelle (CHF)", min_value=100, max_value=1000, step=10, value=350)
interest_rate = st.number_input("Taux d'intérêt (%)", min_value=1.0, max_value=10.0, step=0.1, value=7.0)
years = st.number_input("Nombre d'années de contrat", min_value=1, max_value=len(real_values_588_base), step=1, value=35)

# Calcul des valeurs affinées
refined_values = refined_model(real_values_588_base, ratios_dynamic_300_588, contribution, interest_rate, years)

# Création du tableau des résultats
years_display = np.arange(1, years + 1)  # Années affichées comme 1, 2, 3, ...
results_df = pd.DataFrame({
    "Année": years_display,
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
