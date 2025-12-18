# TP3

## Contexte

Dans les précédents TP, nous avons mis en place un pipeline complet d’ingestion de données pour StreamFlow. Les données disponibles couvrent les utilisateurs, leurs abonnements, l’usage de la plateforme, les paiements et le support client. Ces informations sont historisées sous forme de snapshots mensuels et agrégées sur 30 ou 90 jours, permettant de suivre l’activité et l’engagement des utilisateurs dans le temps. Le pipeline inclut également des validations de qualité des données via Great Expectations pour garantir la cohérence des tables avant toute exploitation.

L’objectif du TP3 est de brancher ces données au Feature Store Feast afin de préparer l’entraînement d’un modèle de churn. Il s’agit de définir l’entity principale `user`, de connecter les DataSources PostgreSQL existantes, de créer des FeatureViews pour les différentes tables de snapshots, et de matérialiser les features à la fois en mode offline pour constituer un jeu d’entraînement et en mode online pour des requêtes rapides. Cette intégration permet non seulement de centraliser les features de manière reproductible, mais aussi de les exposer via un endpoint API minimal pour servir des prédictions en production. Ce TP3 sert de lien entre le pipeline de données existant et la mise en production des fonctionnalités ML au sein du projet StreamFlow.

## Mise en place de Feast

Commande utilisée pour démarrer les services : `docker compose up -d`

Le conteneur feast contient toute la configuration du Feature Store dans le dossier /repo. C’est ici que l’on définit les Entities, les DataSources et les FeatureViews. On utilise ce conteneur pour appliquer la configuration et matérialiser les featuresavec des commandes comme :

`docker compose exec feast feast apply`
`docker compose exec feast feast materialize 2024-01-01 2024-01-31`

# Définition du Feature Store

### 2.d
Une Entity dans Feast représente une entité métier pour laquelle on souhaite suivre ou calculer des features. Dans notre cas, l’Entity user correspond à un client StreamFlow.
`user_id` est un bon choix comme clé de jointure car il identifie de manière unique chaque utilisateur dans toutes les tables du pipeline (abonnements, usage, paiements, support), ce qui permet de relier facilement toutes les features au bon utilisateur.

### 3.b
Exemple d’une table de snapshot : usage_agg_30d_snapshots
Colonnes :
- user_id : identifiant unique de l’utilisateur
- as_of : date du snapshot
- watch_hours_30d : nombre d’heures regardées sur 30 jours
- avg_session_mins_7d : durée moyenne des sessions sur 7 jours
- unique_devices_30d : nombre d’appareils utilisés

### 3.c
La commande `feast apply` sert à synchroniser la configuration Python de votre Feature Store avec le registre Feast (registry.db). Elle crée les entités, DataSources et FeatureViews définis dans votre code et les enregistre dans le registre afin qu’ils puissent être utilisés pour la récupération de features en mode offline ou online. Cela permet de rendre les features disponibles de manière cohérente et centralisée pour l’entraînement ou la prédiction.

# Récupération offline & online

### 4.c
![alt text](<Capture d'écran 2025-12-18 144510.png>)

Les features ont été matérialisées dans l’Online Store sur une fenêtre temporelle donnée, avec `docker compose exec feast feast materialize 2024-01-01T00:00:00 2024-02-01T00:00:00`

Une récupération online a ensuite été testée pour un utilisateur existant via `get_online_features`

![alt text](<Capture d'écran 2025-12-18 144444.png>)

### 4.d
Feast garantit la cohérence temporelle lors de la récupération offline grâce à deux mécanismes clés :
- chaque DataSource définit explicitement un `timestamp_field` (`as_of`) ;
- le `entity_df` fournit un `event_timestamp` pour chaque user.

Feast sélectionne alors uniquement les valeurs de features disponibles au moment du snapshot.

### 4.g
![alt text](<Capture d'écran 2025-12-18 145324.png>)

Si un `user_id` est interrogé alors qu’il ne possède pas de features matérialisées (utilisateur inexistant ou hors fenêtre temporelle), Feast retourne des valeurs nulles ou absentes, indiquant que les données ne sont pas disponibles dans l’Online Store.

### 4.j
@jaderld ➜ ~/csc8613 (main) $ curl http://localhost:8000/health
{"status":"ok"}
@jaderld ➜ ~/csc8613 (main) $ curl http://localhost:8000/features/7590-VHVEG
{"user_id":"7590-VHVEG","features":{"user_id":"7590-VHVEG","paperless_billing":true,"monthly_fee":29.850000381469727,"months_active":1}}

# Réflexion
L’endpoint `/features/{user_id}` permet d’exposer en production exactement les mêmes features que celles utilisées lors de l’entraînement du modèle, car elles sont définies, versionnées et servies par Feast. Cela garantit que les transformations, les sources de données et la logique temporelle sont identiques entre les modes offline et online. En centralisant l’accès aux features via le Feature Store, on évite les divergences de calcul entre les pipelines d'entraînement et de service. Ce mécanisme améliore la cohérence, la fiabilité du système de ML en production.
