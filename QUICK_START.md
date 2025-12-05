# ⚡ Démarrage Rapide - Serveur Ubuntu Vierge

Guide ultra-simple pour installer l'application en 5 minutes sur votre serveur Ubuntu vierge (51.159.67.199).

---

## 🎯 En 3 commandes

### 1️⃣ Se connecter au serveur

```bash
ssh root@51.159.67.199
```

### 2️⃣ Installer tout automatiquement

```bash
curl -sSL https://raw.githubusercontent.com/mathieudottir/up_strava/claude/strava-gamification-app-01MtDwcP9s5YtxgqY3EYyBDp/server-setup.sh | bash
```

⏱️ **Attendre 2-3 minutes** que tout s'installe...

### 3️⃣ Configurer Strava et démarrer

```bash
# Activer Docker pour cette session
newgrp docker

# Aller dans le dossier
cd ~/up_strava

# Éditer la configuration
nano .env
```

**Dans l'éditeur nano**, remplir ces 3 lignes:

```env
STRAVA_CLIENT_ID=VOTRE_CLIENT_ID_ICI
STRAVA_CLIENT_SECRET=VOTRE_CLIENT_SECRET_ICI
SECRET_KEY=ChangezMoiParUneLongueClé123456789
```

**Sauvegarder:** `Ctrl+X`, puis `Y`, puis `Entrée`

```bash
# Démarrer l'application
docker compose up -d
```

---

## 🎉 C'est fait!

Ouvrir dans votre navigateur:

👉 **http://51.159.67.199**

---

## 🔑 Où obtenir les credentials Strava?

1. Aller sur: https://www.strava.com/settings/api
2. Créer une application:
   - **Application Name:** Strava Gamification
   - **Website:** http://51.159.67.199
   - **Authorization Callback Domain:** 51.159.67.199
3. Copier le **Client ID** et **Client Secret**
4. Les coller dans le fichier `.env`

---

## 📱 Commandes utiles

```bash
# Voir les logs
docker compose logs -f

# Arrêter
docker compose down

# Redémarrer
docker compose restart

# Voir l'état
docker compose ps
```

---

## ⚠️ Problèmes fréquents

### "permission denied" avec Docker

```bash
newgrp docker
```

### L'application ne démarre pas

```bash
# Voir ce qui ne va pas
docker compose logs

# Vérifier le .env
cat .env
```

### Impossible d'accéder à l'application

```bash
# Vérifier le firewall
sudo ufw status

# Autoriser le port 80 si nécessaire
sudo ufw allow 80/tcp
```

---

## 📖 Documentation complète

Pour plus de détails, voir [INSTALLATION.md](INSTALLATION.md)

---

**En cas de problème, les logs sont votre ami:**
```bash
docker compose logs -f
```
