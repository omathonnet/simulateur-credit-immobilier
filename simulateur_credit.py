import streamlit as st

# Fonction pour calculer les mensualités d'un prêt immobilier avec assurance, apport des parents et frais de notaire
def calcul_mensualite_avec_assurance_et_apport_parents(capital_emprunte, taux_annuel, duree_annees, taux_assurance_annuel, apport_parents, duree_apport_parents, frais_notaire):
    # Convertir le taux annuel en taux mensuel
    taux_mensuel = taux_annuel / 100 / 12
    
    # Calculer le nombre total de mois pour le prêt principal
    nombre_mois = duree_annees * 12
    
    # Formule de calcul des mensualités d'un prêt (sans assurance)
    mensualite = capital_emprunte * taux_mensuel / (1 - (1 + taux_mensuel) ** -nombre_mois)
    
    # Calculer le coût mensuel de l'assurance
    assurance_mensuelle = capital_emprunte * (taux_assurance_annuel / 100) / 12
    
    # Ajouter l'assurance à la mensualité
    mensualite_totale = mensualite + assurance_mensuelle
    
    # Calculer la mensualité pour l'apport des parents (prêt à taux zéro)
    mensualite_apport_parents = apport_parents / (duree_apport_parents * 12)
    
    # Ajouter la mensualité du prêt à taux zéro des parents à la mensualité totale
    mensualite_totale_avec_apport = mensualite_totale + mensualite_apport_parents
    
    # Calculer le montant total payé à la banque (mensualités * nombre de mois - capital emprunté)
    montant_total_banque = (mensualite_totale * nombre_mois) - capital_emprunte
    
    # Ajouter les frais de notaire au montant total payé
    total_avec_frais_notaire = montant_total_banque + frais_notaire
    
    return mensualite_totale_avec_apport, mensualite_apport_parents, mensualite_totale, montant_total_banque

# Variables du prêt avec les widgets Streamlit dans la barre latérale
st.sidebar.header("Paramètres du prêt")
base_emprunt = st.sidebar.number_input("Montant total du projet immobilier (€)", value=412000)
frais_agence = st.sidebar.number_input("Frais d'agence (€)", value=13000)
apport_perso = st.sidebar.number_input("Apport personnel (€)", value=105000)
apport_parents_taux_zero = st.sidebar.number_input("Apport des parents à taux zéro (€)", value=90000)
taux_annuel = st.sidebar.slider("Taux d'intérêt annuel (%)", min_value=0.0, max_value=10.0, value=3.37, step=0.01)
duree_annees = st.sidebar.slider("Durée du prêt (années)", min_value=1, max_value=30, value=25)
taux_assurance_annuel = st.sidebar.slider("Taux annuel de l'assurance (%)", min_value=0.0, max_value=5.0, value=0.53, step=0.01)
duree_apport_parents = st.sidebar.slider("Durée du remboursement de l'apport des parents (années)", min_value=1, max_value=30, value=25)

# Calculer les frais de notaire estimés
frais_notaire = base_emprunt * 0.07  # Estimation des frais de notaire à 7% du montant du bien

# Calculer le capital emprunté
capital_emprunte = base_emprunt + frais_notaire - apport_perso - apport_parents_taux_zero + frais_agence

# Calculer les mensualités et le montant total à rembourser, y compris les frais de notaire
mensualite_totale_avec_apport, mensualite_apport_parents, mensualite_totale, montant_total_banque = calcul_mensualite_avec_assurance_et_apport_parents(
    capital_emprunte, taux_annuel, duree_annees, taux_assurance_annuel, apport_parents_taux_zero, duree_apport_parents, frais_notaire
)

# Afficher les résultats dans le corps principal pour alléger la sidebar
st.subheader("💰 Détail des Mensualités")
st.markdown(f"- Mensualité du prêt principal (avec assurance) : `{mensualite_totale:,.2f} €/mois`")
st.markdown(f"- Mensualité de l'apport des parents : `{mensualite_apport_parents:,.2f} €/mois`")
st.markdown(
    f"""
    <div style="padding: 10px; border: 2px solid #4CAF50; border-radius: 10px; background-color: #f9f9f9; text-align: center; font-size: 1.2em;">
        <strong>Mensualité totale (prêt + apport des parents)</strong> : <span style="color: #4CAF50;">{mensualite_totale_avec_apport:,.2f} €/mois</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("📊 Résultats du Calcul")
st.markdown(f"**Capital emprunté** : `{capital_emprunte:,.2f} €`")
st.markdown(f"**Frais de notaire estimés** : `{frais_notaire:,.2f} €`")

st.subheader("📈 Coût Total du Prêt")
st.markdown(f"- Montant total des intérêts et assurance versés à la banque : `{montant_total_banque:,.2f} €`")
st.markdown(f"- Montant total donné à la banque par an (hors capital emprunté) : `{montant_total_banque/duree_annees:,.2f} €/an`")
st.markdown(f"- Nombre d'années pour rembourser uniquement les intérêts : `{(montant_total_banque/mensualite_totale/12):.2f} ans`")


