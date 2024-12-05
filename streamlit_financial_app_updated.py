
import streamlit as st
import pandas as pd

# Fonction pour calculer les valeurs de rachat et frais basées sur les contributions seulement
def calculate_values_without_yield(contribution, years):
    fees_data = []
    cumulative_contributions = 0

    for year in range(1, years + 1):
        # Montant total déposé (cumul des contributions)
        annual_contribution = contribution * 12
        cumulative_contributions += annual_contribution

        # Valeur projetée sans rendement (cumul des contributions seulement)
        projected_value_no_yield = cumulative_contributions

        # Simuler une valeur de rachat (ajuster selon les besoins)
        # Par exemple : supposer une réduction de 10% les premières années
        if year <= 5:
            rachat_value = projected_value_no_yield * 0.9
        else:
            rachat_value = projected_value_no_yield * 0.95

        # Frais effectifs
        annual_fee = projected_value_no_yield - rachat_value
        annual_fee_percentage = (annual_fee / projected_value_no_yield) * 100 if projected_value_no_yield != 0 else 0

        # Stockage des données
        fees_data.append({
            "Année": year,
            "Montant Déposé (CHF)": cumulative_contributions,
            "Valeur Proj. Sans Rendement (CHF)": projected_value_no_yield,
            "Valeur de Rachat (CHF)": rachat_value,
            "Frais Annuel Effectif (CHF)": annual_fee,
            "Pourcentage des Frais Annuel (%)": annual_fee_percentage,
        })

    return pd.DataFrame(fees_data)

# Interface utilisateur Streamlit
st.title("Calculateur de Valeur de Rachat et Frais (Sans Rendement)")

# Entrées utilisateur
contribution = st.number_input("Montant de la rente mensuelle (CHF)", min_value=100, step=10, value=400)
years = st.number_input("Nombre d'années du contrat", min_value=1, step=1, value=20)

# Calcul des résultats
if st.button("Calculer"):
    results = calculate_values_without_yield(contribution, years)
    st.write("### Résultats")
    st.dataframe(results)

    # Export en CSV
    csv = results.to_csv(index=False).encode('utf-8')
    st.download_button("Télécharger les résultats (CSV)", data=csv, file_name="resultats_calculs_sans_rendement.csv")
