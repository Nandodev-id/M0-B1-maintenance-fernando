# FastIA — API de maintenance prédictive

API REST développée avec **FastAPI** permettant d’exposer un modèle scikit-learn pré-entraîné de classification de criticité d’incidents machines.

Le modèle retourne trois niveaux de criticité :

* `basse`
* `moyenne`
* `haute`

L’API fournit également les probabilités associées à chaque classe.

## Fonctionnalités

* Chargement du modèle scikit-learn au démarrage de l’application
* Validation des données avec Pydantic
* Endpoint de santé `GET /health`
* Endpoint de prédiction `POST /predict`
* Documentation Swagger disponible sur `/docs`
* Journalisation des prédictions avec Loguru
* Tests fonctionnels avec pytest et FastAPI TestClient
* Conteneurisation avec Docker
* Exécution du conteneur avec un utilisateur non-root
* Healthcheck Docker intégré

## Prérequis

* Python 3.11 ou supérieur
* Git
* Docker Desktop pour l’exécution avec Docker

## Installation locale

Cloner le dépôt :

```bash
git clone <URL_DU_REPOSITORY>
cd M0-B1-maintenance-fernando
```

Créer et activer un environnement virtuel :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Sous Windows :

```powershell
.venv\Scripts\activate
```

Installer les dépendances :

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Lancement local

Démarrer l’API avec Uvicorn :

```bash
uvicorn app.main:app --reload
```

L’API est ensuite disponible sur :

```text
http://127.0.0.1:8000
```

Documentation Swagger :

```text
http://127.0.0.1:8000/docs
```

## Endpoints

### Vérifier l’état du service

```http
GET /health
```

Exemple :

```bash
curl http://127.0.0.1:8000/health
```

Réponse attendue :

```json
{
  "status": "ok",
  "model_loaded": true
}
```

### Effectuer une prédiction

```http
POST /predict
```

Exemple avec curl :

```bash
curl -X POST \
  http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "type_machine": "compresseur",
    "age_machine_jours": 1500,
    "derniere_maintenance_jours": 45,
    "temperature_moyenne": 68.5,
    "vibration_moyenne": 3.2,
    "pression_moyenne": 7.8,
    "nb_incidents_3_mois": 2
  }'
```

Exemple de réponse :

```json
{
  "criticite": "basse",
  "probabilites": {
    "basse": 0.945,
    "haute": 0.0,
    "moyenne": 0.055
  }
}
```

## Données d’entrée

| Champ                        | Type    | Description                                                               |
| ---------------------------- | ------- | ------------------------------------------------------------------------- |
| `type_machine`               | string  | Type de machine : `pompe`, `compresseur`, `convoyeur`, `presse` ou `four` |
| `age_machine_jours`          | integer | Âge de la machine en jours                                                |
| `derniere_maintenance_jours` | integer | Nombre de jours depuis la dernière maintenance                            |
| `temperature_moyenne`        | float   | Température moyenne en degrés Celsius                                     |
| `vibration_moyenne`          | float   | Vibration moyenne en mm/s                                                 |
| `pression_moyenne`           | float   | Pression moyenne en bar                                                   |
| `nb_incidents_3_mois`        | integer | Nombre d’incidents sur les trois derniers mois                            |

Une entrée invalide produit automatiquement une réponse HTTP `422`.

Exemples d’entrées invalides :

* type de machine inconnu ;
* champ obligatoire manquant ;
* valeur négative pour un champ qui doit être positif ;
* valeur supérieure aux limites définies dans le schéma Pydantic.

## Tests

Lancer tous les tests :

```bash
python -m pytest -v
```

Les tests couvrent notamment :

* la route `/health` ;
* une prédiction valide ;
* le format de la réponse ;
* la présence des trois probabilités ;
* la somme des probabilités ;
* un type de machine invalide ;
* les cinq types de machine autorisés.

## Logs

Les prédictions sont enregistrées avec Loguru dans :

```text
logs/api.log
```

Chaque prédiction contient notamment :

* la date et l’heure ;
* le niveau du log ;
* les données d’entrée ;
* la criticité prédite ;
* la durée du traitement en millisecondes.

Les fichiers de logs :

* effectuent une rotation à partir de 5 Mo ;
* sont conservés pendant 7 jours ;
* sont ensuite compressés au format ZIP.

Le dossier `logs/` est généré à l’exécution et n’est pas versionné dans Git.

## Docker

Docker Desktop doit être lancé.

Construire l’image :

```bash
docker build -t fastia-maintenance:dev .
```

Lancer le conteneur :

```bash
docker run --rm \
  --name fastia-maintenance \
  -p 8000:8000 \
  fastia-maintenance:dev
```

Vérifier le service depuis la machine hôte :

```bash
curl http://localhost:8000/health
```

Vérifier la taille de l’image :

```bash
docker images fastia-maintenance:dev
```

Arrêter le conteneur lorsque celui-ci fonctionne dans un autre terminal :

```bash
docker stop fastia-maintenance
```

Le conteneur utilise :

* l’image `python:3.11-slim` ;
* un utilisateur non-root ;
* un healthcheck appelant `/health` ;
* Uvicorn sans l’option de développement `--reload`.

## Structure du projet

```text
M0-B1-maintenance-fernando/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── schemas.py
├── data/
│   ├── generate_dataset.py
│   └── maintenance_data.csv
├── model/
│   ├── train_baseline.py
│   └── model.joblib
├── tests/
│   ├── __init__.py
│   ├── test_health.py
│   └── test_predict.py
├── ressources/
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```

## Choix techniques

* **FastAPI** pour exposer le modèle via une API REST.
* **Pydantic** pour valider les entrées et les sorties.
* **Pandas** pour construire le DataFrame attendu par le pipeline.
* **scikit-learn et Joblib** pour charger et exécuter le modèle livré.
* **Loguru** pour journaliser les prédictions et leur durée.
* **pytest et TestClient** pour tester l’API sans lancer manuellement un serveur.
* **Docker** pour fournir un service reproductible et déployable.
