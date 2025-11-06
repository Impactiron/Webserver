# Bestellsystem

Open-source ordering system built with Python (Backend) and Vite (Frontend).

## Quick Setup / Schnellstart

**Development / Entwicklung:**
```bash
make install  # Install dependencies / Abhängigkeiten installieren
make dev      # Start dev servers (Backend: :8000, Frontend: :5173)
```

**Production / Produktion (Ubuntu 24.04):**
```bash
# 1. System dependencies / System-Abhängigkeiten
sudo apt update && sudo apt install -y python3-pip python3-venv postgresql nginx

# 2. PostgreSQL setup / PostgreSQL einrichten
sudo -u postgres psql -c "CREATE DATABASE bestellsystem;"
sudo -u postgres psql -c "CREATE USER bestellsystem WITH PASSWORD 'yourpass';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE bestellsystem TO bestellsystem;"

# 3. Clone & configure / Klonen & konfigurieren
git clone <repo-url> /var/www/bestellsystem && cd /var/www/bestellsystem
cp deploy/env.example .env  # Edit .env with production values

# 4. Install & build
make install && make build

# 5. Setup Gunicorn + NGINX (see detailed section below)
```

---

## Detailed Setup / Detaillierte Anleitung

### Development / Entwicklung
**Prerequisites:** Python 3.10+, Node.js 18+, PostgreSQL 14+

1. `make install` - Install dependencies
2. Copy `deploy/env.example` to `.env` and configure
3. `cd backend && source venv/bin/activate && python manage.py migrate`
4. `make dev` - Start servers (Frontend: :5173, Backend: :8000)

### Production Deployment / Produktions-Deployment
**Ubuntu 24.04 + NGINX + Gunicorn + PostgreSQL**

**1. System:**
```bash
sudo apt update && sudo apt install -y python3-pip python3-venv postgresql nginx certbot python3-certbot-nginx
```

**2. PostgreSQL:**
```bash
sudo -u postgres createdb bestellsystem
sudo -u postgres createuser bestellsystem
sudo -u postgres psql -c "ALTER USER bestellsystem WITH PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE bestellsystem TO bestellsystem;"
```

**3. Application:**
```bash
cd /var/www/bestellsystem && cp deploy/env.example .env
# Edit .env: Set SECRET_KEY, DATABASE_URL, DEBUG=False, ALLOWED_HOSTS
make install
cd backend && source venv/bin/activate && python manage.py migrate && python manage.py collectstatic
cd ../frontend && npm run build
```

**4. Gunicorn** (/etc/systemd/system/bestellsystem.service):
```ini
[Unit]
Description=Bestellsystem Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/bestellsystem/backend
Environment="PATH=/var/www/bestellsystem/backend/venv/bin"
ExecStart=/var/www/bestellsystem/backend/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:8000 wsgi:application

[Install]
WantedBy=multi-user.target
```
Enable: `sudo systemctl enable --now bestellsystem`

**5. NGINX** (/etc/nginx/sites-available/bestellsystem):
```nginx
server {
    listen 80;
    server_name your-domain.com;
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location /static/ { alias /var/www/bestellsystem/backend/static/; }
    location / {
        root /var/www/bestellsystem/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
}
```
Enable: `sudo ln -s /etc/nginx/sites-available/bestellsystem /etc/nginx/sites-enabled/ && sudo nginx -t && sudo systemctl reload nginx`

**6. SSL:** `sudo certbot --nginx -d your-domain.com`

### Troubleshooting

**Backend not starting:**
- Logs: `sudo journalctl -u bestellsystem -f`
- Check .env: DATABASE_URL, SECRET_KEY set?
- Test DB: `psql $DATABASE_URL`

**Frontend 404:**
- Check NGINX root: `ls frontend/dist/`
- Rebuild: `cd frontend && npm run build`

**Database errors:**
- Run migrations: `python manage.py migrate`
- Check permissions: `GRANT ALL PRIVILEGES ON DATABASE bestellsystem TO bestellsystem;`

**Port conflicts:**
- Check: `sudo lsof -i :8000` or `:5173`

**Permissions:**
- Fix owner: `sudo chown -R www-data:www-data /var/www/bestellsystem`

## Project Structure / Projektstruktur

```
bestellsystem/
├── backend/          # Python backend
├── frontend/         # Vite frontend
├── deploy/           # Deployment configs
│   └── env.example
├── .github/workflows/
├── .editorconfig
├── .gitignore
├── LICENSE
├── Makefile
└── README.md
```

## License / Lizenz

MIT License - see LICENSE file