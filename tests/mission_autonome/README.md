# NOTE DE TEST - commandes multi-lignes

# Cas couverts :

# CT-1. Commande à 1 ligne : total = quantité x prix

# CT-2. Commande à 2 lignes (2 catégories différentes) : 2 lignes dans la réponse, total = somme

# CT-3. Après une commande acceptée : "available" baisse de la quantité commandée

# CT-4. RM3 : exactement 6 billets (2 catégories différentes minimum) au total -> acceptée

# CT-5. RM3 : 7 billets (2 catégories différentes minimum) au total -> refusée

# CT-6. RM1 : quantité = stock restant -> acceptée

# CT-7. RM1 : stock restant + 1 -> refusée

# CT-8. Une commande refusée ne change pas les disponibilités

# Anomalies constatées :

# (rien pour l'instant)

# Données utilisées (un événement neuf par test, créé par une fixture, aucun ID en dur) :

# - cas 1, 2, 3, 6, 7, 8 : small_event (2 catégories de 3 places)

# - cas 4, 5 : événement avec plus de stock (7 places ou plus au total),

# pour que seule RM3 puisse refuser la commande
