# Ressources M0-B1 — Intégrer un service IA via API REST

> Brief associé : **M0-B1**.
> Mode : individuel, présentiel mardi, 5 heures synchrone.
> Le brief lui-même est diffusé sur **Simplonline** (énoncé + 6 liens utiles).

Ce dossier rassemble **les 4 mini-cours pédagogiques** auxquels le brief M0-B1
fait référence + les liens officiels. Le **squelette de code**, ce sont les
fichiers à la **racine de ce repo** que tu as créé via « Use this template ».

---

## 📚 Ordre de mobilisation au fil de la journée

| Tâche du brief | Durée | Mini-cours associé |
|---|---|---|
| 1. Prise en main du squelette | 30 min | (cf. [`README` à la racine](../README.md)) |
| 2. Analyse de l'existant | 30 min | — |
| 3. Implémenter `/predict` | 1 h 30 | [`01_FastAPI_essentiel.md`](./01_FastAPI_essentiel.md) |
| 4. Logging Loguru | 30 min | [`03_Loguru_essentiel.md`](./03_Loguru_essentiel.md) |
| 5. Tests pytest `/predict` | 45 min | [`04_Pytest_API_essentiel.md`](./04_Pytest_API_essentiel.md) |
| 6. Conteneurisation Docker | 45 min | [`02_Docker_essentiel.md`](./02_Docker_essentiel.md) |
| 7. README + push GitHub | 30 min | — |

> 💡 **Tu n'es pas obligé·e de lire les mini-cours en amont.** Chacun est conçu
> pour être consulté **au moment où tu en as besoin**, pendant la tâche
> correspondante. Lecture + exercice guidé en ~15 min chacun.

---

## 🛠️ Le squelette du repo de départ

Ce dossier `ressources/` est livré dans le **repo template GitHub**
[`Formation-SIMPLON-IA/ia-dev-id-parcours-m0-b1`](https://github.com/Formation-SIMPLON-IA/ia-dev-id-parcours-m0-b1).
Si tu lis ce fichier, c'est que tu as déjà cliqué sur « Use this template » et
cloné ton repo perso `M0-B1-maintenance-<prénom>`. Vérifie qu'il tourne :

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload    # → /health doit répondre 200
pytest                            # → 2 tests passent
```

Si ces 3 commandes marchent, ton poste est OK pour la journée. Pour le
démarrage complet, cf. le [`README.md`](../README.md) à la racine du repo.

---

## 🎯 Ce qu'on cherche à atteindre

À la fin de M0-B1, tu dois avoir :

- Une **API FastAPI** avec `/health` + `/predict` qui retourne classe + probabilités
- Un **logging Loguru** qui trace chaque requête (entrée, sortie, durée)
- **≥ 3 tests pytest** pour `/predict` qui passent
- Un **Dockerfile** qui build une image < 500 Mo
- Un **README** qui permet à un dev externe de lancer le service en 5 minutes
- Un repo GitHub `M0-B1-maintenance-<prénom>` avec ≥ 5 commits propres

→ Compétence visée : **C6 — imiter** (intégration d'un modèle livré dans un service API).

---

## 🔗 Liens externes

Toutes les URLs externes utilisées dans les mini-cours sont consolidées dans
[`liens_officiels.md`](./liens_officiels.md), vérifiées avant chaque envoi de
brief par l'outillage formateur.

---

## 🆘 Bloqué·e ?

1. Relire l'**Exercice guidé** du mini-cours concerné (chacun a une solution
   attendue à la fin).
2. Ouvrir **Swagger** : <http://localhost:8000/docs> — souvent le plus rapide
   pour débugger une route FastAPI.
3. Lire les logs Loguru dans la console pour repérer les exceptions.
4. **Demander en direct mardi** — tu es en présentiel, autant en profiter. N'attends
   pas d'être bloqué·e 30 min sur le même point.

**Garde-fou** : pas besoin de coder hors mardi 9h-17h. Si tu finis avant,
implémente un des bonus (HEALTHCHECK Docker, test paramétré supplémentaire).