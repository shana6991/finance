
import streamlit as st
import pandas as pd

# Fonction pour calculer les valeurs de rachat et frais
def calculate_values(contribution, years, rate, f_entry=0.01, f_annual=0.03):
    values = []
    cumulative_contributions = 0
    total_fees = 0

    for year in range(1, years + 1):
        # Montant total déposé
        annual_contribution = contribution * 12
        cumulative_contributions += annual_contribution

        # Valeur projetée avec rendement sans frais
        projected_value = sum([annual_contribution * (1 + rate) ** (year - i) for i in range(1, year + 1)])

        # Calcul des frais (d'entrée et annuels)
        entry_fee = annual_contribution * f_entry
        annual_fee = annual_contribution * f_annual
        yearly_fee = entry_fee + annual_fee
        total_fees += yearly_fee

        # Valeur de rachat après frais
        rachat_value = projected_value - total_fees

        # Stocker les résultats
        values.append({
            "Année": year,
            "Montant Déposé (CHF)": cumulative_contributions,
            "Valeur Proj. Sans Frais (CHF)": projected_value,
            "Valeur de Rachat (CHF)": rachat_value,
            "Frais Annuel (CHF)": yearly_fee,
            "Frais Cumulé (CHF)": total_fees,
            "Pourcentage des Frais (%)": (total_fees / projected_value) * 100 if projected_value != 0 else 0
        })

    return pd.DataFrame(values)

# Interface utilisateur avec Streamlit
st.title("Calculateur de Valeur de Rachat et Frais")

# Entrées utilisateur
contribution = st.number_input("Montant de la rente mensuelle (CHF)", min_value=100, step=10, value=400)
years = st.number_input("Nombre d'années du contrat", min_value=1, step=1, value=20)
rate = st.number_input("Taux de rendement annuel (%)", min_value=0.0, step=0.1, value=5.0) / 100

# Calcul des résultats
if st.button("Calculer"):
    results = calculate_values(contribution, years, rate)
    st.write("### Résultats")
    st.dataframe(results)

    # Export en CSV
    csv = results.to_csv(index=False).encode('utf-8')
    st.download_button("Télécharger les résultats (CSV)", data=csv, file_name="resultats_calculs.csv")
