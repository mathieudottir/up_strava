# 🚀 Guide d'Installation Complet - Serveur Ubuntu Vierge

Ce guide vous accompagne pas à pas pour installer la plateforme Strava Gamification sur un serveur Ubuntu 22.04 LTS complètement vierge.

**IP du serveur:** 51.159.67.199

---

## 📋 Table des matières

1. [Installation automatique (recommandé)](#installation-automatique)
2. [Installation manuelle](#installation-manuelle)
3. [Configuration de l'application](#configuration-de-lapplication)
4. [Démarrage de l'application](#démarrage-de-lapplication)
5. [Configuration SSL (optionnel)](#configuration-ssl)
6. [Dépannage](#dépannage)

---

## ⚡ Installation automatique (recommandé)

### Étape 1: Se connecter au serveur

```bash
ssh root@51.159.67.199
# ou
ssh votre_utilisateur@51.159.67.199
```

### Étape 2: Lancer le script d'installation automatique

```bash
curl -sSL https://raw.githubusercontent.com/mathieudottir/up_strava/claude/strava-gamification-app-01MtDwcP9s5YtxgqY3EYyBDp/server-setup.sh | bash
```

Le script va automatiquement:
- ✅ Mettre à jour le système
- ✅ Installer Git
- ✅ Installer Docker et Docker Compose
- ✅ Cloner le repository
- ✅ Créer le fichier .env
- ✅ Configurer le firewall

**Ensuite passez à la section [Configuration de l'application](#configuration-de-lapplication)**

---

## 🔧 Installation manuelle

Si vous préférez installer manuellement étape par étape:

### 1. Mise à jour du système

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 2. Installation de Git

```bash
sudo apt-get install -y git curl wget
```

Vérifier l'installation:
```bash
git --version
# Devrait afficher: git version 2.x.x
```

### 3. Installation de Docker

#### 3.1. Désinstaller les anciennes versions (si existantes)

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

#### 3.2. Installer les dépendances

```bash
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

#### 3.3. Ajouter la clé GPG de Docker

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

#### 3.4. Configurer le repository Docker

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

#### 3.5. Installer Docker

```bash
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### 3.6. Configurer les permissions

```bash
# Ajouter votre utilisateur au groupe docker
sudo usermod -aG docker $USER

# Démarrer Docker
sudo systemctl enable docker
sudo systemctl start docker
```

#### 3.7. Vérifier l'installation

```bash
docker --version
# Devrait afficher: Docker version 24.x.x

docker compose version
# Devrait afficher: Docker Compose version v2.x.x
```

⚠️ **IMPORTANT:** Après avoir ajouté votre utilisateur au groupe docker, vous devez:
- Soit vous déconnecter et reconnecter
- Soit exécuter: `newgrp docker`

### 4. Cloner le repository

```bash
cd ~
git clone -b claude/strava-gamification-app-01MtDwcP9s5YtxgqY3EYyBDp https://github.com/mathieudottir/up_strava.git
cd up_strava
```

### 5. Configurer le firewall (UFW)

```bash
# Installer UFW
sudo apt-get install -y ufw

# Autoriser SSH (IMPORTANT!)
sudo ufw allow 22/tcp

# Autoriser HTTP et HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Activer le firewall
sudo ufw enable

# Vérifier le status
sudo ufw status
```

---

## ⚙️ Configuration de l'application

### 1. Obtenir les credentials Strava API

1. Aller sur: https://www.strava.com/settings/api
2. Créer une nouvelle application avec:
   - **Application Name:** Strava Gamification (ou votre choix)
   - **Category:** Quantified Self
   - **Website:** http://51.159.67.199
   - **Authorization Callback Domain:** 51.159.67.199
3. Copier le **Client ID** et **Client Secret**

### 2. Configurer le fichier .env

```bash
cd ~/up_strava
cp .env.example .env
nano .env
```

Modifier les valeurs suivantes:

```env
# Database - CHANGER LE MOT DE PASSE!
POSTGRES_USER=strava_user
POSTGRES_PASSWORD=VotreMotDePasseSecurise123!
POSTGRES_DB=strava_gamification

# Strava OAuth2 - REMPLIR AVEC VOS CREDENTIALS
STRAVA_CLIENT_ID=123456
STRAVA_CLIENT_SECRET=abc123def456...
STRAVA_REDIRECT_URI=http://51.159.67.199/auth/callback

# Security - CHANGER LA CLÉ SECRÈTE!
SECRET_KEY=GenerezUneCleAleatoireTresLongue123456789

# URLs - ADAPTER À VOTRE DOMAINE
BACKEND_CORS_ORIGINS=http://51.159.67.199,https://51.159.67.199
FRONTEND_URL=http://51.159.67.199
NEXT_PUBLIC_API_URL=http://51.159.67.199
```

**Sauvegarder:** `Ctrl+X`, puis `Y`, puis `Entrée`

---

## 🚀 Démarrage de l'application

### Méthode 1: Avec le script de déploiement

```bash
cd ~/up_strava
chmod +x deploy.sh
./deploy.sh
```

### Méthode 2: Avec Docker Compose directement

```bash
cd ~/up_strava

# Activer le groupe docker pour cette session
newgrp docker

# Construire et démarrer les conteneurs
docker compose up -d

# Vérifier que tout fonctionne
docker compose ps
```

Vous devriez voir 5 conteneurs en cours d'exécution:
- ✅ strava_backend
- ✅ strava_frontend
- ✅ strava_postgres
- ✅ strava_redis
- ✅ strava_nginx

### Vérifier les logs

```bash
# Tous les logs
docker compose logs -f

# Logs d'un service spécifique
docker compose logs -f backend
docker compose logs -f frontend
```

### Accéder à l'application

Ouvrir dans votre navigateur:
- **Application:** http://51.159.67.199
- **API Backend:** http://51.159.67.199/api/v1
- **Documentation API:** http://51.159.67.199/docs

---

## 🔒 Configuration SSL (optionnel mais recommandé)

### Avec un nom de domaine

Si vous avez un nom de domaine pointant vers 51.159.67.199:

```bash
cd ~/up_strava

# Lancer l'initialisation SSL
make ssl-init

# Suivre les instructions et entrer:
# - Votre nom de domaine (ex: upstrava.com)
# - Votre email

# Redémarrer nginx
docker compose restart nginx
```

Ensuite, mettez à jour votre `.env` avec votre domaine:

```env
STRAVA_REDIRECT_URI=https://votre-domaine.com/auth/callback
BACKEND_CORS_ORIGINS=https://votre-domaine.com
FRONTEND_URL=https://votre-domaine.com
NEXT_PUBLIC_API_URL=https://votre-domaine.com
```

Redémarrer l'application:
```bash
docker compose down
docker compose up -d
```

---

## 🔧 Commandes utiles

### Gestion de l'application

```bash
# Voir les logs
docker compose logs -f

# Arrêter l'application
docker compose down

# Redémarrer l'application
docker compose restart

# Voir l'état des conteneurs
docker compose ps

# Reconstruire et redémarrer
docker compose up -d --build
```

### Accès aux conteneurs

```bash
# Backend
docker compose exec backend /bin/sh

# Base de données
docker compose exec postgres psql -U strava_user -d strava_gamification

# Frontend
docker compose exec frontend /bin/sh
```

### Backup de la base de données

```bash
# Créer un backup
docker compose exec postgres pg_dump -U strava_user strava_gamification > backup_$(date +%Y%m%d).sql

# Restaurer un backup
docker compose exec -T postgres psql -U strava_user strava_gamification < backup_20241205.sql
```

---

## 🐛 Dépannage

### Les conteneurs ne démarrent pas

```bash
# Voir les logs détaillés
docker compose logs

# Vérifier l'espace disque
df -h

# Nettoyer Docker
docker system prune -a
```

### Erreur de permissions Docker

```bash
# Si vous obtenez "permission denied"
sudo usermod -aG docker $USER
newgrp docker

# Ou redémarrer votre session SSH
exit
ssh user@51.159.67.199
```

### Le frontend ne se connecte pas au backend

Vérifier que les URLs dans `.env` sont correctes:
```bash
cat .env | grep URL
```

### Erreur "port already in use"

```bash
# Voir ce qui utilise le port 80
sudo lsof -i :80

# Arrêter apache2 si installé
sudo systemctl stop apache2
sudo systemctl disable apache2
```

### La base de données ne démarre pas

```bash
# Vérifier les logs
docker compose logs postgres

# Réinitialiser les volumes
docker compose down -v
docker compose up -d
```

---

## 📊 Monitoring

### Vérifier l'utilisation des ressources

```bash
# Utilisation CPU/RAM par conteneur
docker stats

# Espace disque
df -h

# Logs système
sudo journalctl -xe
```

### Vérifier que tout fonctionne

```bash
# Test API backend
curl http://51.159.67.199/api/v1/

# Test frontend
curl http://51.159.67.199/

# Test base de données
docker compose exec postgres pg_isready -U strava_user
```

---

## 🆘 Besoin d'aide?

- Vérifier les logs: `docker compose logs -f`
- Vérifier l'état: `docker compose ps`
- Redémarrer: `docker compose restart`
- Issue GitHub: https://github.com/mathieudottir/up_strava/issues

---

## ✅ Checklist finale

- [ ] Ubuntu à jour
- [ ] Git installé
- [ ] Docker installé et fonctionne
- [ ] Repository cloné
- [ ] Fichier .env configuré avec credentials Strava
- [ ] Firewall configuré (ports 22, 80, 443)
- [ ] Application démarrée
- [ ] Accessible via http://51.159.67.199
- [ ] Connexion Strava fonctionne

---

**Bon déploiement! 🚀**
