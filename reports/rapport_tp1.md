## Exercice 1 - Installation de Docker et vérification de l’environnement

![alt text](<Capture d'écran 2025-12-05 103923.png>)

![alt text](<Capture d'écran 2025-12-05 103944.png>)

### 1.c
La commande `docker ps -a` affiche tous les conteneurs présents sur la machine, qu’ils soient en cours d’exécution ou arrêtés. On voit pour chaque conteneur : son id, le nom de l’image, la commande exécutée, la date de création, le statut et les ports. Cela permet de savoir quels conteneurs sont actifs, quels conteneurs ont été créés précédemment et de gérer les ressources.

## Exercice 2 - Premiers pas avec Docker : images et conteneurs

### 2.a
*   **Une image Docker** est un modèle statique qui contient tout l’environnement nécessaire pour exécuter une application.
*   **Un conteneur Docker** est une instance active d’une image qui s’exécute sur le système. On peut créer plusieurs conteneurs à partir de la même image.

### 2.b
On exécute la commande suivante : `docker run alpine echo "Bonjour depuis un conteneur Alpine"`

Après exécution, le message “Bonjour depuis un conteneur Alpine” est affiché dans le terminal, puis le conteneur se termine immédiatement. Cela se produit car Alpine n’a été lancé que pour exécuter la commande echo, puis se ferme.

### 2.c
Le conteneur Alpine apparaît avec le statut `Exited` car il a terminé son exécution. Docker conserve l’historique du conteneur même s’il n’est plus actif.

### 2.d
À l’intérieur du conteneur, les commandes `ls` et `uname -a` permettent de vérifier les fichiers présents et d’afficher les informations sur le système. Après `exit`, on retourne au terminal hôte. On observe donc que le conteneur possède son propre mini-système de fichiers.

## Exercice 3 - Construire une première image Docker avec une mini-API FastAPI

La commande `docker build -t simple-api .` construit l’image à partir du Dockerfile. Elle s’exécute étape par étape, créant l’environnement Python, copiant app.py et installant FastAPI et Uvicorn. Le succès de la construction se traduit par un message indiquant “Successfully built” et “Successfully tagged simple-api:latest”. Cela confirme que l’image est prête à être utilisée pour exécuter l’API.

## Exercice 3 - Construire une première image Docker avec une mini-API FastAPI

![alt text](<Capture d'écran 2025-12-05 111817.png>)

## Exercice 4 - Exécuter l’API FastAPI dans un conteneur Docker

### 4.a
L’option `-p 8000:8000` mappe le port 8000 du conteneur au port 8000 de la machine hôte. Elle permet d’accéder à l’API depuis le navigateur ou un outil comme curl sur la machine locale.

![alt text](<Capture d'écran 2025-12-05 111900.png>)

### 4.c
![alt text](<Capture d'écran 2025-12-05 111955.png>)

On peut identifier le conteneur nommé quizzical_snyder en cours d’exécution, l’image utilisée (simple-api), et le port mappé (0.0.0.0:8000->8000/tcp).

## 4.d
![alt text](<Capture d'écran 2025-12-05 112121.png>)

docker ps : liste uniquement les conteneurs en cours d’exécution.
docker ps -a : liste tous les conteneurs, même ceux arrêtés ou terminés.

## Exercice 5 - Démarrer un mini-système multi-conteneurs avec Docker Compose

### 5.c
![alt text](<Capture d'écran 2025-12-05 113414.png>)

### 5.d
![alt text](<Capture d'écran 2025-12-05 113432.png>)

### 5.e
docker stop <id> : arrête un conteneur spécifique, mais les autres services continuent de tourner. Le conteneur reste visible avec docker ps -a.
docker compose down : arrête tous les services définis dans le docker-compose.yml et supprime automatiquement les conteneurs, les réseaux créés et éventuellement les volumes si -v est utilisé.

## Exercice 6 - Interagir avec PostgreSQL dans un conteneur

![alt text](<Capture d'écran 2025-12-05 113613.png>)

### 6.a
exec : exécute une commande dans un conteneur déjà en cours d’exécution.
db : nom du conteneur cible.
-U demo : se connecte en tant qu’utilisateur demo.
-d demo : se connecter à la base de données demo.

![alt text](<Capture d'écran 2025-12-05 113613-1.png>)

### 6.c
Pour se connecter, il faudrait :
Hostname : db
Port : 5432
Utilisateur / mot de passe : demo / demo
Nom de la base : demo

### 6.d
L’option -v supprime les volumes associés aux conteneurs donc la perte des données stockées dans PostgreSQL.

## Exercice 7 - Déboguer des conteneurs Docker

### 7.a
![alt text](<Capture d'écran 2025-12-05 113827.png>)

Au démarrage de l’API, on observe les messages d’initialisation d’Uvicorn et FastAPI.
Lors d’une requête /health, on observe une ligne indiquant l’IP source, le type de requête (GET), le endpoint (/health), et le code HTTP 200.

### 7.b
![alt text](<Capture d'écran 2025-12-05 113914.png>)

ls : affiche les fichiers du conteneur, dont app.py.
python --version : permet de vérifier que Python est installé.
exit : retourne au terminal hôte.

### 7.c
![alt text](<Capture d'écran 2025-12-05 113943.png>)

Le redémarrage permet de relancer uniquement l’API sans affecter les autres services. C’est utile lors de mises à jour du code ou pour corriger un conteneur qui a crashé.

### 7.d
![alt text](<Capture d'écran 2025-12-05 114335.png>)
Lorsqu’une erreur est introduite dans app.py, les logs (docker compose logs -f api) affichent l’historique Python et permettent d’identifier la cause. Ici, on voit qu'il n'arrive pas à copier 

### 7.e
Un nettoyage régulier permet de libérer de l’espace disque et de supprimer les conteneurs ou images inutilisés. Cela évite l’encombrement et réduit les risques de conflits avec d’anciennes versions.

Exercice 8 - Questions de réflexion

### Pourquoi un notebook Jupyter n’est pas adapté pour déployer un modèle ML en production ?
Reproductibilité limitée : les notebooks contiennent souvent des cellules exécutées dans un ordre non linéaire, ce qui rend difficile la reproduction exacte de l’environnement.
Automatisation difficile : un notebook n’est pas conçu pour être déployé comme un service web ou intégré dans un pipeline CI/CD. Docker permet de créer un environnement isolé et stable pour l’API ou le modèle.

### Pourquoi Docker Compose est essentiel pour plusieurs services ?
Docker permet de lancer plusieurs services simultanément (API, base de données) avec un seul fichier de configuration. Il facilite la gestion des dépendances et du réseau entre services et permet de reproduire facilement l’environnement sur n’importe quelle machine ou pour différents membres d’une équipe.
