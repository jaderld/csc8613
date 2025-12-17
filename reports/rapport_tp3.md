# Contexte

Dans les précédents TP, nous avons mis en place un pipeline complet d’ingestion de données pour StreamFlow. Les données disponibles couvrent les utilisateurs, leurs abonnements, l’usage de la plateforme (heures de visionnage, sessions, skips, rebuffer events), les paiements et le support client. Ces informations sont historisées sous forme de snapshots mensuels et agrégées sur 30 ou 90 jours, permettant de suivre l’activité et l’engagement des utilisateurs dans le temps. Le pipeline inclut également des validations de qualité des données via Great Expectations pour garantir l’intégrité et la cohérence des tables avant toute exploitation.

L’objectif du TP3 est de brancher ces données au Feature Store Feast afin de préparer l’entraînement d’un modèle de churn. Concrètement, il s’agit de définir l’entity principale `user`, de connecter les DataSources PostgreSQL existantes, de créer des FeatureViews pour les différentes tables de snapshots, et de matérialiser les features à la fois en mode offline pour constituer un jeu d’entraînement et en mode online pour des requêtes rapides. Cette intégration permet non seulement de centraliser les features de manière reproductible, mais aussi de les exposer via un endpoint API minimal pour servir des prédictions en production. Ainsi, TP3 constitue le lien entre le pipeline de données existant et la mise en production des fonctionnalités d’IA au sein du projet StreamFlow, en assurant que les features utilisées pour l’entraînement et pour l’inférence sont identiques et à jour.

# Mise en place de Feast
# Définition du Feature Store
# Récupération offline & online
# Réflexion