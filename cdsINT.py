import streamlit as st

def johnsons_algorithm(tasks):
    set_X = [task for task in tasks if task[1] <= task[2]]
    set_Y = [task for task in tasks if task[1] > task[2]]
    set_X.sort(key=lambda x: x[1])
    set_Y.sort(key=lambda x: x[2], reverse=True)
    return set_X + set_Y

def calculer_cmax(taches, sequence_optimale, m):
    temps_machines = [0] * m  # Initialiser les temps de fin des machines
    cmax = 0  # Initialiser le makespan
    for index in sequence_optimale:
        tache = taches[index]  # Récupérer la tâche originale à l'indice
        temps_m1 = temps_machines[0] + tache[0]  # Temps de début pour la première machine
        temps_machines[0] = temps_m1
        for j in range(1, m):
            temps_m1 = max(temps_m1, temps_machines[j]) + tache[j]
            temps_machines[j] = temps_m1
        cmax = max(cmax, temps_m1)  # Mettre à jour le makespan si nécessaire
    return cmax

st.title("Ordonnancement des Tâches avec CDS")
st.markdown("Cette application utilise l'heuristique de CDS et l'algorithme de Johnson pour optimiser le **makespan (Cmax)**.")

# Entrée utilisateur
num_tasks = st.number_input("Entrez le nombre de tâches", min_value=1, step=1)
num_machines = st.number_input("Entrez le nombre de machines", min_value=1, step=1)

if num_tasks and num_machines:
    st.subheader("Saisissez les temps de traitement")
    matrice_temps = []
    for i in range(num_tasks):
        times = st.text_input(f"Tâche {i + 1} : Entrez les temps (séparés par des espaces)")
        if times:
            try:
                times_list = [int(t) for t in times.split()]
                if len(times_list) != num_machines:
                    st.error(f"Vous devez entrer exactement {num_machines} valeurs pour chaque tâche.")
                else:
                    matrice_temps.append(times_list)
            except ValueError:
                st.error("Veuillez entrer des nombres valides.")

    if len(matrice_temps) == num_tasks:
        st.subheader("Calcul des résultats")

        best_sequence = None
        best_cmax = float('inf')

        for k in range(1, num_machines):
            # Création des pseudo-machines
            pseudo_tasks = []
            for i, task in enumerate(matrice_temps):
                p1 = sum(task[:k])
                p2 = sum(task[k:])
                pseudo_tasks.append((i, p1, p2))

            # Application de l'algorithme de Johnson
            current_sequence = johnsons_algorithm(pseudo_tasks)
            task_indices = [t[0] for t in current_sequence]  # Extraire les indices originaux des tâches
            current_cmax = calculer_cmax(matrice_temps, task_indices, num_machines)

            # Mise à jour de la meilleure séquence et du Cmax
            if current_cmax < best_cmax:
                best_cmax = current_cmax
                best_sequence = task_indices

        if best_sequence is not None:
            best_sequence_readable = [f"Tâche {t + 1}" for t in best_sequence]

            st.success("Calcul terminé !")
            st.write("**Meilleure séquence des tâches :**")
            st.write(" → ".join(best_sequence_readable))

            st.write(f"**Makespan (Cmax) optimal :** {best_cmax}")
        else:
            st.error("Impossible de trouver une solution optimale.")
