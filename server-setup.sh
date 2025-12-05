#!/bin/bash

# Script d'installation complète pour serveur Ubuntu vierge
# Pour Strava Gamification Platform
# Usage: curl -sSL https://raw.githubusercontent.com/mathieudottir/up_strava/claude/strava-gamification-app-01MtDwcP9s5YtxgqY3EYyBDp/server-setup.sh | bash

set -e

echo "🚀 Installation de Strava Gamification Platform"
echo "================================================"
echo ""

# Vérifier qu'on est sur Ubuntu
if [ ! -f /etc/os-release ]; then
    echo "❌ Erreur: Ce script nécessite Ubuntu"
    exit 1
fi

echo "📦 Étape 1/6: Mise à jour du système..."
sudo apt-get update
sudo apt-get upgrade -y

echo ""
echo "📦 Étape 2/6: Installation de Git..."
sudo apt-get install -y git curl wget

echo ""
echo "🐳 Étape 3/6: Installation de Docker..."
# Désinstaller les anciennes versions
sudo apt-get remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true

# Installer les dépendances
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Ajouter la clé GPG officielle de Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Configurer le repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Installer Docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Ajouter l'utilisateur au groupe docker
sudo usermod -aG docker $USER

# Démarrer Docker
sudo systemctl enable docker
sudo systemctl start docker

echo ""
echo "✅ Docker installé avec succès!"
docker --version

echo ""
echo "📥 Étape 4/6: Clonage du repository..."
cd /home/$USER
if [ -d "up_strava" ]; then
    echo "⚠️  Le dossier up_strava existe déjà. Suppression..."
    rm -rf up_strava
fi

git clone -b claude/strava-gamification-app-01MtDwcP9s5YtxgqY3EYyBDp https://github.com/mathieudottir/up_strava.git
cd up_strava

echo ""
echo "⚙️  Étape 5/6: Configuration de l'environnement..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Fichier .env créé. Vous devrez le configurer avec vos credentials Strava."
fi

echo ""
echo "🔥 Étape 6/6: Configuration du firewall..."
# Installer UFW si pas déjà installé
sudo apt-get install -y ufw

# Autoriser SSH (important!)
sudo ufw allow 22/tcp

# Autoriser HTTP et HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Activer le firewall
echo "y" | sudo ufw enable

echo ""
echo "✅ Installation terminée!"
echo ""
echo "================================================"
echo "📋 PROCHAINES ÉTAPES:"
echo "================================================"
echo ""
echo "1. Obtenir vos credentials Strava API:"
echo "   → Aller sur: https://www.strava.com/settings/api"
echo "   → Créer une application"
echo "   → Authorization Callback Domain: 51.159.67.199"
echo ""
echo "2. Configurer le fichier .env:"
echo "   → cd /home/$USER/up_strava"
echo "   → nano .env"
echo "   → Remplir STRAVA_CLIENT_ID et STRAVA_CLIENT_SECRET"
echo "   → Changer SECRET_KEY et POSTGRES_PASSWORD"
echo ""
echo "3. Démarrer l'application:"
echo "   → cd /home/$USER/up_strava"
echo "   → newgrp docker  # Pour activer le groupe docker"
echo "   → docker compose up -d"
echo ""
echo "4. Accéder à l'application:"
echo "   → http://51.159.67.199"
echo ""
echo "================================================"
echo ""
echo "⚠️  IMPORTANT: Vous devez vous déconnecter et reconnecter pour que"
echo "   les permissions Docker prennent effet, OU utilisez:"
echo "   newgrp docker"
echo ""
