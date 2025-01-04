import streamlit as st

# Fonction pour l'algorithme de Johnson
def algorithme_johnson(taches):
    X = {tache: temps for tache, temps in taches.items() if temps.get("M1", float('inf')) <= temps.get("M2", 0)}
    Y = {tache: temps for tache, temps in taches.items() if temps.get("M1", 0) > temps.get("M2", float('inf'))}
    X_trie = sorted(X, key=lambda tache: X[tache].get("M1", float('inf')))
    Y_trie = sorted(Y, key=lambda tache: Y[tache].get("M2", 0), reverse=True)
    sequence = X_trie + Y_trie
    return sequence

# Fonction pour l'algorithme généralisé de Johnson
def algorithme_johnson_generalise(taches_selectionnees, toutes_les_taches):
    taches_filtrees = {tache: toutes_les_taches[tache] for tache in taches_selectionnees if tache in toutes_les_taches}
    return algorithme_johnson(taches_filtrees)

# Interface Streamlit
def app():
    st.title("Algorithme de Johnson - Ordonnancement Flow Shop")

    # Exemples par défaut
    taches_par_defaut = {
        "T1": {"M1": 1, "M2": 2},
        "T2": {"M1": 3, "M2": 2},
        "T3": {"M2": 4, "M1": 2},
        "T4": {"M1": 1},
        "T5": {"M2": 1},
        "T6": {"M2": 9, "M1": 3},
        "T7": {"M1": 2},
        "T8": {"M1": 2, "M2": 1},
        "T9": {"M2": 2},
        "T10": {"M1": 1, "M2": 1},
        "T11": {"M2": 8, "M1": 4}
    }

    # Afficher les tâches par défaut ou laisser l'utilisateur entrer ses propres données
    st.subheader("Données d'entrée des tâches")
    taches = taches_par_defaut  # On garde les tâches par défaut pour pré-remplir les champs

    # Affichage des champs avec les données par défaut
    for tache, temps in taches.items():
        m1_time = temps.get("M1", 0)
        m2_time = temps.get("M2", 0)
        taches[tache]["M1"] = st.number_input(f"Temps M1 pour {tache}", min_value=0, value=m1_time)
        taches[tache]["M2"] = st.number_input(f"Temps M2 pour {tache}", min_value=0, value=m2_time)

    # Ajouter un bouton pour lancer l'exécution
    if st.button('Exécuter l\'algorithme'):
        # Partitionner les tâches
        O1 = [t for t in taches if "M1" in taches[t] and "M2" not in taches[t]]
        O2 = [t for t in taches if "M2" in taches[t] and "M1" not in taches[t]]
        O12 = [t for t in taches if "M1" in taches[t] and "M2" in taches[t] and list(taches[t].keys())[0] == "M1"]
        O21 = [t for t in taches if "M1" in taches[t] and "M2" in taches[t] and list(taches[t].keys())[0] == "M2"]

        O12 = algorithme_johnson_generalise(O12, taches)
        O21.sort(key=lambda t: taches[t]["M1"], reverse=True)

        # Construire les séquences
        sequence_M1 = O12 + O1 + O21
        sequence_M2 = O21 + O2 + O12

        # Calculer Cmax
        cmax = max(
            sum([taches[t]["M1"] for t in sequence_M1 if "M1" in taches[t]]),
            sum([taches[t]["M2"] for t in sequence_M2 if "M2" in taches[t]])
        )

        # Affichage des résultats
        st.subheader("Résultats de l'ordonnancement")
        st.write(f"Séquence pour Machine M1 : {sequence_M1}")
        st.write(f"Séquence pour Machine M2 : {sequence_M2}")
        st.write(f"Makespan (Cmax) : {cmax}")

if __name__ == "__main__":
    app()
