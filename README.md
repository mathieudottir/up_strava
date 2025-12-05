# 🏃 Strava Gamification Platform

Transform your Strava activities into an epic adventure with points, badges, challenges, and leaderboards!

## 🎯 Features

- **Points System**: Earn points for every activity based on distance, elevation, and time
- **Badges & Achievements**: Unlock exclusive badges by reaching milestones
- **Leaderboards**: Compete with others on global and segment-specific leaderboards
- **Challenges**: Join time-bound challenges and compete with the community
- **Strava Integration**: Seamless OAuth2 integration with Strava
- **Real-time Sync**: Sync your activities from Strava with one click

## 🛠️ Tech Stack

### Backend
- **Python 3.11** with **FastAPI**
- **SQLAlchemy** (async) + **PostgreSQL**
- **Redis** for caching and jobs
- **APScheduler** for background tasks
- **Strava OAuth2** integration
- **JWT** authentication

### Frontend
- **Next.js 15** (App Router)
- **React 19**
- **TailwindCSS**
- **TanStack Query** for data fetching
- **TypeScript**

### Infrastructure
- **Docker** + **Docker Compose**
- **Nginx** reverse proxy
- **Let's Encrypt** SSL certificates
- **PostgreSQL 16**
- **Redis 7**

## 📁 Project Structure

```
up_strava/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── api/                    # API routes
│   │   │   └── api_v1/
│   │   │       ├── api.py          # Main router
│   │   │       └── endpoints/      # API endpoints
│   │   ├── core/                   # Core configuration
│   │   │   ├── config.py           # Settings
│   │   │   └── security.py         # Auth utilities
│   │   ├── models/                 # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── activity.py
│   │   │   ├── segment.py
│   │   │   ├── badge.py
│   │   │   ├── leaderboard.py
│   │   │   └── challenge.py
│   │   ├── db/                     # Database configuration
│   │   │   ├── database.py
│   │   │   └── redis.py
│   │   └── services/               # Business logic
│   │       ├── strava_service.py
│   │       └── gamification_service.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/
│   │   ├── layout.tsx              # Root layout
│   │   ├── page.tsx                # Home page
│   │   ├── providers.tsx           # React Query provider
│   │   ├── globals.css             # Global styles
│   │   ├── auth/
│   │   │   └── callback/           # OAuth callback
│   │   └── dashboard/              # Dashboard page
│   ├── components/                 # React components
│   ├── lib/                        # Utilities
│   │   └── api.ts                  # API client
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── next.config.js
│   └── Dockerfile
├── proxy/
│   └── nginx.conf                  # Nginx configuration
├── docker-compose.yml              # Docker orchestration
├── .env.example                    # Environment variables template
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Strava API credentials (Client ID and Secret)
- Domain name (optional, for SSL)

### 1. Clone the Repository

```bash
git clone https://github.com/mathieudottir/up_strava.git
cd up_strava
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:

```env
# Database
POSTGRES_USER=strava_user
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=strava_gamification

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Strava OAuth2
STRAVA_CLIENT_ID=your_strava_client_id
STRAVA_CLIENT_SECRET=your_strava_client_secret
STRAVA_REDIRECT_URI=https://your-domain.com/auth/callback

# Security
SECRET_KEY=your_secret_key_here_change_in_production

# URLs
BACKEND_CORS_ORIGINS=https://your-domain.com,http://localhost:3000
FRONTEND_URL=https://your-domain.com
NEXT_PUBLIC_API_URL=https://your-domain.com
```

### 3. Get Strava API Credentials

1. Go to https://www.strava.com/settings/api
2. Create a new application
3. Set the Authorization Callback Domain to your domain
4. Copy the Client ID and Client Secret to your `.env` file

### 4. Start the Application

```bash
# Build and start all services
docker-compose up -d

# Check logs
docker-compose logs -f
```

The services will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 5. Setup SSL with Let's Encrypt (Production)

For production deployment with SSL:

```bash
# Update nginx.conf with your domain name
# Then run certbot to get SSL certificates

docker-compose run --rm certbot certonly --webroot \
  --webroot-path /var/www/certbot \
  -d your-domain.com \
  -d www.your-domain.com \
  --email your-email@example.com \
  --agree-tos \
  --no-eff-email

# Restart nginx to apply SSL
docker-compose restart nginx
```

## 🔧 Development

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## 📊 Database Models

### User
- Strava athlete information
- OAuth tokens
- Total points and level
- Activity statistics

### Activity
- Synced from Strava
- Distance, time, elevation
- Points earned

### Segment & SegmentEffort
- Strava segments
- User efforts on segments
- PR tracking

### Badge
- Achievement definitions
- User earned badges
- Points rewards

### Leaderboard
- Global and segment leaderboards
- User rankings
- Time-based leaderboards

### Challenge
- Time-bound competitions
- User progress tracking
- Completion rewards

## 🎮 Gamification System

### Points Calculation

Points are awarded based on:
- **Distance**: 10 points per km
- **Elevation**: 1 point per 10m
- **Time**: 5 points per hour
- **Activity Type Multiplier**: Run (1.0x), Ride (0.8x), Swim (1.2x)

### Leveling System

User level is calculated as:
```
level = floor(sqrt(total_points / 100))
```

### Badge Types
- **Distance**: Total distance milestones
- **Elevation**: Elevation gain achievements
- **Speed**: Performance-based badges
- **Consistency**: Activity streak rewards
- **Challenge**: Challenge completion badges
- **Special**: Limited-time exclusive badges

## 🔐 API Endpoints

### Authentication
- `GET /api/v1/auth/strava/authorize` - Get Strava OAuth URL
- `GET /api/v1/auth/strava/callback` - OAuth callback handler
- `GET /api/v1/auth/me` - Get current user

### Users
- `GET /api/v1/users/{user_id}` - Get user profile
- `GET /api/v1/users/{user_id}/stats` - Get user statistics

### Activities
- `GET /api/v1/activities/` - Get user activities
- `POST /api/v1/activities/sync` - Sync from Strava

### Badges
- `GET /api/v1/badges/` - Get all badges
- `GET /api/v1/badges/user/{user_id}` - Get user badges

### Leaderboards
- `GET /api/v1/leaderboards/` - Get all leaderboards
- `GET /api/v1/leaderboards/global` - Get global leaderboard

### Challenges
- `GET /api/v1/challenges/` - Get all challenges
- `POST /api/v1/challenges/{id}/join` - Join a challenge
- `GET /api/v1/challenges/user/{user_id}` - Get user challenges

## 🐳 Docker Services

### PostgreSQL
- Image: `postgres:16-alpine`
- Port: 5432 (internal)
- Persistent volume for data

### Redis
- Image: `redis:7-alpine`
- Port: 6379 (internal)
- AOF persistence enabled

### Backend (FastAPI)
- Port: 8000 (internal)
- Auto-restart enabled
- Health checks configured

### Frontend (Next.js)
- Port: 3000 (internal)
- Standalone output mode
- Optimized production build

### Nginx
- Ports: 80, 443
- Reverse proxy for backend and frontend
- SSL/TLS termination
- WebSocket support

### Certbot
- Automatic SSL certificate renewal
- Runs every 12 hours

## 📈 Monitoring & Logs

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f nginx

# Check service status
docker-compose ps

# Restart services
docker-compose restart backend
docker-compose restart frontend
```

## 🔄 Backup & Restore

### Database Backup

```bash
docker-compose exec postgres pg_dump -U strava_user strava_gamification > backup.sql
```

### Database Restore

```bash
docker-compose exec -T postgres psql -U strava_user strava_gamification < backup.sql
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Strava API for activity data
- FastAPI for the amazing web framework
- Next.js for the powerful React framework
- All contributors and users of this platform

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ for the Strava community**
