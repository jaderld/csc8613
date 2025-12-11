## Exercice 1 - Installation de Docker et vérification de l’environnement

![alt text](<Capture d'écran 2025-12-05 103923.png>)

La commande `docker ps -a` affiche tous les conteneurs présents sur la machine, qu’ils soient en cours d’exécution ou arrêtés. On voit pour chaque conteneur : son id, le nom de l’image, la commande exécutée, la date de création, le statut et les ports. Cela permet de savoir quels conteneurs sont actifs, quels conteneurs ont été créés précédemment et de gérer les ressources.

## Exercice 2 - Premiers pas avec Docker : images et conteneurs

### 2.a Image Docker vs. Conteneur Docker

*   **Une image Docker** est un modèle statique qui contient tout l’environnement nécessaire pour exécuter une application.
*   **Un conteneur Docker** est une instance active d’une image qui s’exécute sur le système. On peut créer plusieurs conteneurs à partir de la même image.

### 2.b Exécution d'un conteneur Alpine

On exécute la commande suivante : `docker run alpine echo "Bonjour depuis un conteneur Alpine"`

Après exécution, le message “Bonjour depuis un conteneur Alpine” est affiché dans le terminal, puis le conteneur se termine immédiatement. Cela se produit car Alpine n’a été lancé que pour exécuter la commande echo, puis se ferme.

### 2.c Statut du conteneur après exécution

Le conteneur Alpine apparaît avec le statut `Exited` car il a terminé son exécution. Docker conserve l’historique du conteneur même s’il n’est plus actif.

### 2.d Vérification du système de fichiers du conteneur

À l’intérieur du conteneur, les commandes `ls` et `uname -a` permettent de vérifier les fichiers présents et d’afficher les informations sur le système. Après `exit`, on retourne au terminal hôte. On observe donc que le conteneur possède son propre mini-système de fichiers.

## Exercice 3 - Construire une première image Docker avec une mini-API FastAPI

La commande `docker build -t simple-api .` construit l’image à partir du Dockerfile. Elle s’exécute étape par étape, créant l’environnement Python, copiant app.py et installant FastAPI et Uvicorn. Le succès de la construction se traduit par un message indiquant “Successfully built” et “Successfully tagged simple-api:latest”. Cela confirme que l’image est prête à être utilisée pour exécuter l’API.

## Exercice 4 - Exécuter l’API FastAPI dans un conteneur Docker

### 4.a
L’option `-p 8000:8000` mappe le port 8000 du conteneur au port 8000 de la machine hôte. Elle permet d’accéder à l’API depuis le navigateur ou un outil comme curl sur la machine locale.

### Observation de docker ps :
On peut identifier le conteneur simple-api en cours d’exécution, l’image utilisée (simple-api), et le port mappé (0.0.0.0:8000->8000/tcp).

Différence docker ps / docker ps -a :

4.d docker ps : liste uniquement les conteneurs en cours d’exécution.
docker ps -a : liste tous les conteneurs, même ceux arrêtés ou terminés.

Exercice 5 - Démarrer un mini-système multi-conteneurs avec Docker Compose

5.e docker stop <id> : arrête un conteneur spécifique, mais les autres services continuent de tourner. Le conteneur reste visible avec docker ps -a.
docker compose down : arrête tous les services définis dans le docker-compose.yml et supprime automatiquement les conteneurs, les réseaux créés et éventuellement les volumes si -v est utilisé.

Exercice 6 - Interagir avec PostgreSQL dans un conteneur

6.a exec : exécute une commande dans un conteneur déjà en cours d’exécution.
db : nom du conteneur cible.
-U demo : se connecte en tant qu’utilisateur demo.
-d demo : se connecter à la base de données demo.

Connexion d’un autre service (API) à PostgreSQL :

Hostname : db (le nom du service dans Docker Compose)

Port : 5432

Utilisateur / mot de passe : demo / demo

Nom de la base : demo

6.d L’option -v supprime les volumes associés aux conteneurs donc la perte des données stockées dans PostgreSQL.
