# Dockerfile — service de criticité maintenance prédictive (M0-B1)
#
# 🎯 À COMPLÉTER PAR L'APPRENANT.
#
# Indices d'implémentation (cf. mini-cours `02_Docker_essentiel.md`) :
#
#   1. Image de base : python:3.11-slim (légère, suffisante pour scikit-learn)
#
#   2. WORKDIR : choisir un répertoire de travail (/app par exemple)
#
#   3. Installer les dépendances système si nécessaire (rare pour ce projet)
#
#   4. COPIER `requirements.txt` puis lancer `pip install --no-cache-dir -r requirements.txt`
#      → astuce : copier le requirements AVANT le code source pour profiter du
#      cache Docker (les couches de l'image ne sont reconstruites que si le fichier change).
#
#   5. COPIER le code applicatif : `app/`, `model/`, et la donnée si nécessaire.
#
#   6. EXPOSE 8000 (port que uvicorn écoutera).
#
#   7. CMD ou ENTRYPOINT : démarrer uvicorn en production
#      → uvicorn app.main:app --host 0.0.0.0 --port 8000
#      → ne PAS utiliser --reload en image de production.
#
# Bonus (Critères de performance § 6) :
#   - Utilisateur non-root (USER non-root après mkdir + chown)
#   - HEALTHCHECK qui interroge /health
#   - Multi-stage build pour réduire la taille finale
#
# Commande type pour build et lancer une fois ce fichier complété :
#   docker build -t fastia-maintenance:dev .
#   docker run --rm -p 8000:8000 fastia-maintenance:dev
#   curl http://localhost:8000/health


FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Installer les dépendances avant de copier le code pour profiter du cache Docker.
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copier uniquement les fichiers nécessaires à l'exécution.
COPY app ./app
COPY model ./model

# Créer un utilisateur non-root et lui donner accès au dossier de logs.
RUN mkdir -p /app/logs \
    && useradd --create-home appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]