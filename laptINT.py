import streamlit as st

# Fonction pour trouver la tâche la plus longue pour une machine spécifique
def LTache(machine_actuelle, taches):
    if machine_actuelle == 'M1':
        return max(taches, key=lambda t: taches[t]['p2'])
    else:
        return max(taches, key=lambda t: taches[t]['p1'])

# Fonction pour calculer Cmax
def calculer_cmax(sequence_M1, sequence_M2, taches):
    temps_M1 = sum(taches[tache]['p1'] for tache in sequence_M1 if 'p1' in taches[tache])
    return temps_M1

# Interface Streamlit
st.title("Ordonnancement des Tâches avec LAPT")
st.write("Cette application implémente l'algorithme LAPT pour planifier des tâches sur deux machines.")

# Saisie des données
st.header("Saisir les données des tâches")
nombre_taches = st.number_input("Nombre de tâches", min_value=1, step=1, value=5)
taches = {}

for i in range(1, nombre_taches + 1):
    with st.expander(f"Tâche T{i}"):
        temps_M1 = st.number_input(f"Temps sur M1 (Tâche T{i})", min_value=0, step=1, value=0)
        temps_M2 = st.number_input(f"Temps sur M2 (Tâche T{i})", min_value=0, step=1, value=0)
        taches[f"T{i}"] = {"p1": temps_M1, "p2": temps_M2}

# Planification des tâches
if st.button("Planifier les tâches et calculer le makespan"):
    copie_taches = taches.copy()
    taches_M1 = []
    taches_M2 = []
    temps_M1 = 0
    temps_M2 = 0

    while copie_taches:
        if temps_M1 <= temps_M2:
            tache = LTache('M1', copie_taches)
            taches_M1.append(tache)
            temps_M1 += copie_taches[tache]['p1']
        else:
            tache = LTache('M2', copie_taches)
            taches_M2.append(tache)
            temps_M2 += copie_taches[tache]['p2']

        del copie_taches[tache]

    # Construire les séquences finales pour M1 et M2
    sequence_M1 = taches_M1 + taches_M2
    sequence_M2 = taches_M2 + taches_M1

    # Calculer Cmax
    cmax = calculer_cmax(sequence_M1, sequence_M2, taches)

    # Affichage des résultats
    st.success("Résultats obtenus")
    st.write(f"Séquence pour Machine M1 : {' → '.join(sequence_M1)}")
    st.write(f"Séquence pour Machine M2 : {' → '.join(sequence_M2)}")
    st.write(f"Makespan (Cmax) : {cmax}")
