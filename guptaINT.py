import streamlit as st

# Fonctions de calcul
def heuristique_gupta(matrice_temps):
    num_taches = len(matrice_temps)
    num_machines = len(matrice_temps[0])
    e = [1 if matrice_temps[i][0] < matrice_temps[i][-1] else -1 for i in range(num_taches)]
    s = []

    for i in range(num_taches):
        ratios = [e[i] / (matrice_temps[i][k] + matrice_temps[i][k + 1]) for k in range(num_machines - 1)]
        s.append((i, min(ratios)))

    # Trier les tâches par l'indice s dans l'ordre décroissant
    s.sort(key=lambda x: x[1], reverse=True)
    # Extraire les indices des tâches triées
    sequence_optimale = [x[0] for x in s]
    
    return sequence_optimale

def calculer_cmax(matrice_temps, sequence_optimale):
    temps_machines = [0] * len(matrice_temps[0])
    temps_debut = [0] * len(matrice_temps)
    for tache in sequence_optimale:
        temps_debut[tache] = temps_machines[0] + matrice_temps[tache][0]
        temps_machines[0] = temps_debut[tache]
        for machine in range(1, len(matrice_temps[tache])):
            temps_debut[tache] = max(temps_machines[machine], temps_debut[tache]) + matrice_temps[tache][machine]
            temps_machines[machine] = temps_debut[tache]
    return max(temps_machines)

# Interface Streamlit
st.title("Ordonnancement des Tâches avec GUPTA")
st.markdown("Optimisation du makespan Cmax pour un système à plusieurs machines.")

# Saisie des paramètres
st.header("Paramètres d'entrée")
num_taches = st.number_input("Nombre de tâches", min_value=1, step=1, value=3)
num_machines = st.number_input("Nombre de machines", min_value=2, step=1, value=3)

# Initialisation de la matrice des temps
matrice_temps = []
for i in range(num_taches):
    temps = st.text_input(f"Tâche {i + 1} : Entrez les temps de traitement (séparés par un espace)", "1 2 3")
    matrice_temps.append([int(x) for x in temps.split()])

# Calcul
if st.button("Calculer la séquence optimale et le makespan"):
    try:
        sequence_optimale = heuristique_gupta(matrice_temps)
        cmax = calculer_cmax(matrice_temps, sequence_optimale)

        # Affichage des résultats
        sequence_optimale_noms = [f'Tâche {i+1}' for i in sequence_optimale]
        st.success("Calcul terminé avec succès.")
        st.write("### Résultats :")
        st.write(f"1. **Séquence optimale des tâches :** {' → '.join(sequence_optimale_noms)}")
        st.write(f"2. **Makespan optimal Cmax) :** {cmax}")

    except Exception as e:
        st.error(f"Erreur lors du calcul : {e}")
