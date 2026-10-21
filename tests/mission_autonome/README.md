# NOTE DE TEST - commandes multi-lignes


# Cas couverts :
#   1. Commande à 1 ligne : total = quantité x prix
#   2. Commande à 2 lignes (2 catégories différentes) : 2 lignes dans la réponse, total = somme
#   3. Après une commande acceptée : "available" baisse de la quantité commandée
#   4. RM3 : exactement 6 billets (2 catégories différentes minimum) au total -> acceptée
#   5. RM3 : 7 billets (2 catégories différentes minimum) au total -> refusée
#   6. RM1 : quantité = stock restant -> acceptée
#   7. RM1 : stock restant + 1 -> refusée
#   8. Une commande refusée ne change pas les disponibilités


# Anomalies constatées :
#   (rien pour l'instant)


# Données utilisées (cherchées dans l'API, jamais écrites en dur) :
#   - cas 1, 3, 8 : une catégorie d'un événement publié avec au moins 6 places
#   - cas 2, 4, 5 : deux catégories du même événement publié, chacune avec au moins 4 places
#   - cas 6, 7    : une catégorie avec entre 1 et 5 places (pour que seule RM1 puisse refuser)