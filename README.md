# Balboa Connect

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

**Une intégration Home Assistant pour les spas Balboa avec module Wi-Fi BW50350.**

## 📌 À propos

Cette intégration permet de contrôler votre spa Balboa via Home Assistant **sans déconnexions intempestives**. Elle respecte strictement le protocole Balboa pour éviter de surcharger le module Wi-Fi.

✅ **Fonctionnalités :**
- Contrôle de la température.
- Gestion des modes (chauffage, filtration, etc.).
- Polling optimisé pour éviter les déconnexions.
- Connexion TCP persistante.

⚠️ **Prérequis :**
- Un spa Balboa avec **module Wi-Fi BW50350** (firmware à jour).
- Carte mère compatible (ex : BP6013G3).
- Écran SpaTouch2 ou similaire.

## 🛠 Installation

### Via HACS (recommandé)
1. Ajoutez ce dépôt comme [repository personnalisé dans HACS](https://hacs.xyz/docs/faq/custom_repositories/).
2. Redémarrez Home Assistant.
3. Ajoutez l'intégration via **Paramètres > Appareils et services > Ajouter une intégration > Balboa Connect**.

### Manuellement
1. Copiez le dossier `balboa_connect` dans le dossier `custom_components/` de votre installation Home Assistant.
2. Redémarrez Home Assistant.
3. Ajoutez l'intégration via **Paramètres > Appareils et services**.

## ⚙ Configuration

1. **Adresse IP** : L'adresse IP locale de votre module BW50350.
2. **Port** : Par défaut `4257`.
3. **Nom** : Nom personnalisé pour votre spa (optionnel).

## 🐛 Résolution des problèmes

### Déconnexions fréquentes
- Vérifiez que votre **firmware BW50350 est à jour** (version ≥ 2.0.0).
- Assurez-vous qu'aucune autre application (ex : Balboa WorldWide App) n'est connectée simultanément.
- Réduisez la fréquence de polling dans les paramètres de l'intégration.

### Logs
Activez les logs en ajoutant ceci à votre `configuration.yaml` :
```yaml
logger:
  default: info
  logs:
    custom_components.balboa_connect: debug