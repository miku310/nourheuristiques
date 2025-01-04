import streamlit as st

def methode_coin_superieur_gauche(offres, demandes, couts):
    # Initialiser la matrice des coûts et le coût total à zéro
    matrice_couts = [[0 for j in range(len(demandes))] for i in range(len(offres))]
    cout_total = 0

    i = j = 0
    while i < len(offres) and j < len(demandes):
        # Trouver la quantité à transporter
        quantite_min = min(offres[i], demandes[j])
        matrice_couts[i][j] = quantite_min
        offres[i] -= quantite_min
        demandes[j] -= quantite_min

        # Calculer le coût pour cette allocation et l'ajouter au coût total
        cout_total += matrice_couts[i][j] * couts[i][j]

        # Mettre à jour les indices pour la prochaine itération
        if offres[i] == 0:
            i += 1
        if demandes[j] == 0:
            j += 1

    return matrice_couts, cout_total


def afficher_matrice(matrice, titre):
    """Affiche la matrice de manière lisible"""
    return "\n" + "=" * 50 + "\n" + f"{titre.center(50)}" + "\n" + "=" * 50 + "\n" + \
           "\n".join(["| " + " | ".join(f"{val:5}" for val in ligne) + " |" for ligne in matrice]) + "\n" + "-" * 50


def app():
    st.title("Méthode du Coin Supérieur Gauche - Problème de Transport")

    # Saisie des tailles des matrices
    nombres_sources = st.number_input("Nombre de sources (n)", min_value=1, value=3)
    nombres_destinations = st.number_input("Nombre de destinations (m)", min_value=1, value=3)

    # Saisie de la matrice des coûts
    st.subheader("Matrice des coûts")
    couts = []
    for i in range(nombres_sources):
        ligne = st.text_input(f"Coûts pour la source {i+1} (séparés par des espaces)", "")
        couts.append(list(map(int, ligne.split())))

    # Saisie des offres
    offres = list(map(int, st.text_input("Offres (séparées par des espaces)").split()))

    # Saisie des demandes
    demandes = list(map(int, st.text_input("Demandes (séparées par des espaces)").split()))

    if st.button("Exécuter l'algorithme"):
        # Calculer la solution avec la méthode du coin supérieur gauche
        matrice_couts, cout_total = methode_coin_superieur_gauche(offres.copy(), demandes.copy(), couts)

        # Afficher les matrices et le coût total
        st.subheader("Matrice des coûts")
        st.text(afficher_matrice(couts, "Matrice des coûts"))

        st.subheader("Matrice des allocations")
        st.text(afficher_matrice(matrice_couts, "Matrice des allocations"))

        st.write(f"Coût total minimal : {cout_total}")


if __name__ == "__main__":
    app()
