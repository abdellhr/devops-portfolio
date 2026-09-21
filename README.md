# DevOps Portfolio — Infra as Code, CI/CD & Observabilité

Projet de démonstration illustrant une chaîne DevOps complète, du provisionnement de l'infrastructure jusqu'au monitoring, en passant par l'intégration continue et le scan de sécurité.

## Architecture

Voir [docs/architecture.md](docs/architecture.md) pour le schéma détaillé (Mermaid).

En résumé :

```
GitHub push → CI (lint/tests) → Build image → Scan Trivy → Push GHCR
Terraform (provisionnement) → Ansible (configuration) → Docker Compose (runtime)
App Flask → Prometheus (métriques) → Grafana (dashboards)
```

## Stack technique

| Domaine              | Outil                          |
|-----------------------|--------------------------------|
| Application            | Python / Flask                |
| Conteneurisation        | Docker, Docker Compose        |
| Infra as Code           | Terraform                     |
| Configuration Management | Ansible                     |
| CI/CD                   | GitHub Actions                |
| Sécurité                | Trivy (scan de vulnérabilités)|
| Observabilité            | Prometheus, Grafana           |

## Lancer le projet en local

```bash
git clone https://github.com/abdellhr/devops-portfolio.git
cd devops-portfolio
docker compose up --build
```

Une fois démarré :

- Application : http://localhost:5000
- Prometheus : http://localhost:9090
- Grafana : http://localhost:3000 (identifiants : `admin` / `admin`) — le dashboard **"DevOps Portfolio - Vue d'ensemble"** est chargé automatiquement, aucune configuration manuelle nécessaire

## Provisionner avec Terraform

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

Le provider utilisé ici est `kreuzwerker/docker`, ce qui permet de faire tourner la démo sans compte cloud, tout en gardant une structure (variables, ressources, outputs) directement transposable à un provider AWS, OVHcloud ou Scaleway.

## Déployer sur un serveur avec Ansible

```bash
cd ansible
ansible-playbook -i inventory.ini playbook.yml
```

Le playbook installe Docker sur le serveur cible, copie le projet et lance la stack via `docker compose`.

## Pipeline CI/CD

Chaque push sur `main` déclenche automatiquement :

1. Lint (`flake8`) et tests unitaires (`pytest`)
2. Build de l'image Docker
3. Scan de vulnérabilités avec **Trivy** (bloque le pipeline si une faille critique/haute est détectée)
4. Publication de l'image sur **GitHub Container Registry (GHCR)**
5. Validation de la syntaxe Terraform (`terraform validate`)

## Sécurité

- Conteneur applicatif exécuté avec un **utilisateur non-root**
- Image construite en **multi-stage build** pour réduire la surface d'attaque
- Scan automatisé des vulnérabilités intégré à la CI (approche *shift-left*)
- Secrets gérés via GitHub Actions Secrets, jamais en dur dans le code

## Ce que ce projet démontre

- Séparation claire entre provisionnement (Terraform) et configuration (Ansible)
- Mise en place d'une chaîne CI/CD complète avec contrôle qualité et sécurité
- Observabilité pensée dès la conception, pas ajoutée après coup
- Structure de projet claire et documentée, réutilisable en contexte professionnel

## Pistes d'évolution

- Migrer le provider Terraform vers un cloud réel (AWS/OVHcloud) avec un état distant (backend S3 ou équivalent)
- Ajouter des dashboards Grafana pré-configurés (JSON versionné)
- Passer à Kubernetes (Helm chart) pour la partie orchestration
- Ajouter des tests d'intégration bout en bout dans la CI
