import streamlit as st

# Fonction pour calculer le Cmax
def calculer_cmax(matrice_temps, sequence):
    num_machines = len(matrice_temps[0])
    temps_fin = [0] * num_machines
    for tache in sequence:
        temps_debut = temps_fin[0] + matrice_temps[tache][0]
        temps_fin[0] = temps_debut
        for machine in range(1, num_machines):
            temps_debut = max(temps_fin[machine], temps_debut) + matrice_temps[tache][machine]
            temps_fin[machine] = temps_debut
    return temps_fin[-1]

# Fonction pour implémenter l'heuristique NEH
def neh_heuristique(matrice_temps):
    num_taches = len(matrice_temps)
    # Calculer la somme des temps de traitement sur toutes les machines pour chaque tâche
    somme_temps = [sum(tache) for tache in matrice_temps]
    # Trier les tâches par la somme des temps de traitement en ordre décroissant
    taches_triees = sorted(range(num_taches), key=lambda i: somme_temps[i], reverse=True)
    sequence = [taches_triees.pop(0)]  # Commencer avec la tâche ayant le plus grand temps total

    # Ajouter chaque tâche dans la meilleure position
    for tache in taches_triees:
        best_cmax = float('inf')
        best_position = 0
        # Essayer d'insérer la tâche à chaque position possible et trouver le meilleur Cmax
        for position in range(len(sequence) + 1):
            nouvelle_sequence = sequence[:position] + [tache] + sequence[position:]
            cmax = calculer_cmax(matrice_temps, nouvelle_sequence)
            if cmax < best_cmax:
                best_cmax = cmax
                best_position = position
        sequence.insert(best_position, tache)
    return sequence, best_cmax

# Interface Streamlit
st.title("Ordonnancement des Tâches avec l'Heuristique NEH")
st.write("Cette application implémente l'heuristique NEH pour ordonnancer des tâches sur plusieurs machines et optimiser le makespan (\(C_{\text{max}}\)).")

# Saisie des données
st.header("Saisir les données")
num_taches = st.number_input("Nombre de tâches", min_value=1, step=1, value=5)
num_machines = st.number_input("Nombre de machines", min_value=1, step=1, value=3)

# Matrice des temps de traitement
st.header("Matrice des Temps de Traitement")
matrice_temps = []
for i in range(num_taches):
    with st.expander(f"Tâche {i + 1}"):
        temps_tache = []
        for j in range(num_machines):
            temps_machine = st.number_input(f"Temps de traitement sur Machine {j + 1}", min_value=0, step=1, value=0, key=f"tache{i}_machine{j}")
            temps_tache.append(temps_machine)
        matrice_temps.append(temps_tache)

# Calcul de la séquence optimale
if st.button("Calculer la Séquence Optimale et le Cmax"):
    sequence_optimale, cmax = neh_heuristique(matrice_temps)

    # Affichage des résultats
    st.success("Résultats obtenus")
    sequence_noms = [f"Tâche {i + 1}" for i in sequence_optimale]
    st.write("**1. La séquence optimale des tâches :**")
    st.write(" → ".join(sequence_noms))
    st.write("**2. Le Cmax (makespan) optimal :**")
    st.write(cmax)
