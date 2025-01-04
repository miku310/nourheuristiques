import streamlit as st

def least_cost_method(costs, supply, demand):
    filled_values = [[0 for _ in range(len(demand))] for _ in range(len(supply))]
    while sum(supply) > 0 and sum(demand) > 0:
        # Trouver la cellule avec le coût minimal
        min_cost = float('inf')
        for i in range(len(supply)):
            for j in range(len(demand)):
                if costs[i][j] < min_cost and supply[i] > 0 and demand[j] > 0:
                    min_cost = costs[i][j]
                    min_i, min_j = i, j

        # Calculer la quantité à transporter
        quantity = min(supply[min_i], demand[min_j])
        filled_values[min_i][min_j] = quantity
        supply[min_i] -= quantity
        demand[min_j] -= quantity

    return filled_values

def calculate_final_cost(allocation, costs):
    total_cost = 0
    for i in range(len(allocation)):
        for j in range(len(allocation[i])):
            total_cost += allocation[i][j] * costs[i][j]
    return total_cost

def afficher_matrice(matrice, titre):
    """Formatage de la matrice en texte lisible"""
    result = "\n" + "=" * 50 + "\n" + f"{titre.center(50)}" + "\n" + "=" * 50 + "\n"
    result += "\n".join(["| " + " | ".join(f"{val:5}" for val in ligne) + " |" for ligne in matrice]) + "\n" + "-" * 50
    return result

def app():
    st.title("Méthode du Moindre Coût - Problème de Transport")

    # Saisie des tailles des matrices
    rows = st.number_input("Nombre de sources (n)", min_value=1, value=3)
    columns = st.number_input("Nombre de destinations (m)", min_value=1, value=3)

    # Saisie de la matrice des coûts
    st.subheader("Matrice des coûts")
    costs = []
    for i in range(rows):
        ligne = st.text_input(f"Coûts pour la source {i+1} (séparés par des espaces)", "")
        costs.append(list(map(int, ligne.split())))

    # Saisie des offres
    supply = list(map(int, st.text_input("Offres (séparées par des espaces)").split()))

    # Saisie des demandes
    demand = list(map(int, st.text_input("Demandes (séparées par des espaces)").split()))

    if st.button("Exécuter l'algorithme"):
        # Calculer l'allocation avec la méthode du moindre coût
        allocation = least_cost_method(costs, supply.copy(), demand.copy())

        # Calculer le coût total
        final_cost = calculate_final_cost(allocation, costs)

        # Afficher les résultats
        st.subheader("Matrice des coûts")
        st.text(afficher_matrice(costs, "Matrice des coûts"))

        st.subheader("Matrice des allocations")
        st.text(afficher_matrice(allocation, "Matrice des allocations"))

        st.write(f"Coût total minimal : {final_cost}")

if __name__ == "__main__":
    app()
