# Balboa Connect

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacs-shield]][hacs]

**Intégration Home Assistant pour les spas Balboa avec module Wi-Fi BW50350.**

## ✨ Fonctionnalités
- ✅ Contrôle de la température et des modes (chauffage, filtration).
- ✅ Gestion des pompes, jets, lumières.
- ✅ Polling optimisé (30 secondes) pour éviter les déconnexions.
- ✅ Connexion TCP persistante et respect du protocole Balboa.
- ✅ Compatible avec **BP6013G3** et **SpaTouch2**.

## 📥 Installation via HACS
1. **Ajoutez ce dépôt comme repository personnalisé** :
   - Allez dans **HACS > Paramètres > Dépôts personnalisés**.
   - Ajoutez l'URL du dépôt : `https://github.com/votre-utilisateur/balboa_connect`.
   - Sélectionnez **Catégorie : Intégration**.
   - Cliquez sur **Ajouter**.

2. **Installez l'intégration** :
   - Allez dans **HACS > Intégrations**.
   - Recherchez **Balboa Connect** et cliquez sur **Installer**.
   - Redémarrez Home Assistant.

3. **Configurez l'intégration** :
   - Allez dans **Paramètres > Appareils et services > Ajouter une intégration**.
   - Sélectionnez **Balboa Connect**.
   - Entrez l'**adresse IP** de votre module BW50350 (ex: `192.168.1.100`), le **port** (`4257`), et un **nom** (ex: "Mon Spa").

## ⚙ Configuration
   Paramètre       | Description                          | Valeur par défaut |
 |-----------------|--------------------------------------|-------------------|
 | **Adresse IP**  | Adresse locale du module BW50350.    | -                 |
 | **Port**        | Port du module.                      | 4257              |
 | **Nom**         | Nom personnalisé pour votre spa.     | Balboa Spa        |

## 📊 Entités disponibles
 | Type          | Description                          | Exemple d'utilisation          |
 |---------------|--------------------------------------|----------------------------------|
 | **Climate**   | Contrôle de la température et modes. | `climate.mon_spa_climate`        |
 | **Switch**    | Pompes, jets, etc.                   | `switch.mon_spa_pump1`           |
 | **Light**     | Lumière du spa.                      | `light.mon_spa_light`            |
 | **Sensor**    | Température actuelle.                | `sensor.mon_spa_temperature`     |
 | **Binary Sensor** | Alertes (erreur, filtre sale).   | `binary_sensor.mon_spa_error`    |

## 🐛 Dépannage
### Déconnexions fréquentes
- **Vérifiez le firmware** : Contactez le support Balboa avec votre numéro de série pour confirmer que le firmware est à jour (version ≥ 2.0.0).
- **Désactivez les autres applications** : Aucune autre application (ex: Balboa WorldWide App) ne doit être connectée simultanément.
- **Activez les logs** :
  ```yaml
  # configuration.yaml
  logger:
    default: info
    logs:
      custom_components.balboa_connect: debug