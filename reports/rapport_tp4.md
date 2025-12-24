## Exercice 1 - Mise en route

![alt text](<Capture d'écran 2025-12-24 110231.png>)
![alt text](<Capture d'écran 2025-12-24 153618.png>)

Tous les composants principaux de la stack tournent correctement :

- **API** : service backend exposant l’endpoint `/health` et `/features/{user_id}` pour interagir avec Feast et la base Postgres.
- **Postgres** : base de données contenant les snapshots et labels.
- **Feast** : gestion des features offline et online.
- **MLflow** : serveur de tracking et Model Registry pour enregistrer les runs et modèles.

Cette configuration garantit que le pipeline MLOps est complet : ingestion de données, extraction de features, entraînement et suivi des modèles, avec accès web pour MLflow et endpoints REST pour l’API.


## Exercice 2 - Créer un script d'entraînement

### 2.b
![alt text](<Capture d'écran 2025-12-24 155444.png>)

### 2.c
- **AS_OF utilisé** : `2024-01-31`
- **Colonnes catégorielles détectées** : `net_service`

- **Métriques sur le jeu de validation** :
  - AUC : **0.6257**
  - F1-score : **0.0667**
  - Accuracy : **0.7456**
  - Temps d’entraînement : **13 s**

Le script train_baseline.py a été exécuté dans le conteneur Prefect avec la variable d’environnement TRAIN_AS_OF=2024-01-31.
L’entraînement s’est terminé avec succès, générant un run MLflow identifié par le run_id 7bb87d6e19194f25b83ac282fafe1ef9.
Le modèle RandomForest a été enregistré dans le Model Registry sous le nom streamflow_churn.


## Exercice 3 - Explorer l'interface MLflow

**Peu importe mon navigateur, la connexion est refusée sur localhost:5000 alors que la commande curl renvoie une sortie html correcte. Je n'ai donc pas pu visualiser l'interface.**

Le modèle `streamflow_churn` entraîné lors du run MLflow a été enregistré automatiquement dans le Model Registry.
La dernière version du modèle a été promue vers le stage **Production** via l’interface graphique MLflow.


## Exercice 4 - Etendre l'API pour exposer /predict

