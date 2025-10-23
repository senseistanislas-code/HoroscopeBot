# Discord Horoscope Bot

## Overview
Bot Discord en français qui envoie des horoscopes quotidiens personnalisés. Le bot répond aux commandes et peut envoyer automatiquement les horoscopes à 8h00 chaque matin.

## Recent Changes
- 2025-10-22: Projet initialisé avec Python 3.11 et discord.py
- Configuration des dépendances: discord.py, python-dotenv, requests
- Code complet du bot avec système d'abonnement et envoi automatique
- Corrections critiques appliquées:
  - Gestion d'erreur JSON robuste pour éviter les crashes au démarrage
  - Suppression des intents privilégiés non nécessaires (members)
  - Bot testé et fonctionnel, connecté avec succès à Discord

## Project Architecture

### Main Components
- **bot.py**: Fichier principal du bot Discord
  - Gestion des commandes (!horoscope, !abonner, !désabonner, !liste)
  - Envoi automatique quotidien à 8h00
  - Génération d'horoscopes stylés avec API externe
  - Système d'abonnement avec stockage JSON

### Commands
- `!horoscope <signe>`: Obtenir l'horoscope pour un signe donné
- `!abonner <signe>`: S'abonner aux horoscopes quotidiens en DM
- `!désabonner`: Se désabonner des horoscopes quotidiens
- `!liste`: Afficher la liste des abonnés (admin)

### Features
- 12 signes du zodiaque supportés (français → anglais pour l'API)
- Horoscopes stylés avec: énergie, amour, travail, conseil du jour
- Envoi automatique dans un salon Discord à 8h
- Envoi personnalisé par DM aux utilisateurs abonnés
- Stockage persistant des abonnés dans abonnes.json

## Environment Setup
Requires two environment secrets:
- `DISCORD_TOKEN`: Token du bot Discord (Discord Developer Portal)
- `CHANNEL_ID`: ID du salon pour l'envoi automatique quotidien

## User Preferences
- Language: Français
- User dismissed Discord integration - using manual secret management instead
