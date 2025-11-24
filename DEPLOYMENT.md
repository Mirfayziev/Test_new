# AF IMPERIYA - Deployment Guide

## 1. Render.com ga Deploy qilish

### Tayyorgarlik:

```bash
# 1. GitHub repository yarating
git init
git add .
git commit -m "Initial commit: AF IMPERIYA"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

### Render.com sozlamalari:

1. **Render.com** ga kiring: https://render.com
2. **New +** > **Web Service** ni tanlang
3. GitHub repository ni ulang
4. Quyidagi sozlamalarni kiriting:

**Settings:**
- **Name:** `af-imperiya`
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

**Environment Variables:**
```
DATABASE_URL=<your-postgresql-url>
SECRET_KEY=<random-secret-key>
TELEGRAM_BOT_TOKEN=<your-bot-token>
TELEGRAM_CHAT_ID=<your-chat-id>
```

5. **Create Web Service** ni bosing

### PostgreSQL Database:

1. **New +** > **PostgreSQL** ni tanlang
2. Database nomini kiriting
3. **Create Database** ni bosing
4. Connection string ni copy qiling
5. Web Service ga `DATABASE_URL` sifatida qo'shing

## 2. Railway.app ga Deploy qilish

### Tayyorgarlik:

```bash
# Railway CLI o'rnatish
npm i -g @railway/cli

# Login
railway login

# Loyihani yaratish
railway init
```

### Deploy qilish:

```bash
# Deploy
railway up

# Environment variables sozlash
railway variables set SECRET_KEY=your-secret-key
railway variables set TELEGRAM_BOT_TOKEN=your-bot-token

# Database qo'shish
railway add postgresql
```

## 3. Lokal Serverd'a Deploy qilish

### Nginx + Gunicorn:

```bash
# Gunicorn o'rnatish
pip install gunicorn

# Gunicorn ishga tushirish
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Nginx sozlash
sudo nano /etc/nginx/sites-available/afimperiya
```

**Nginx config:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/afimperiya /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Systemd Service:

```bash
sudo nano /etc/systemd/system/afimperiya.service
```

```ini
[Unit]
Description=AF IMPERIYA Web Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/afimperiya
Environment="PATH=/var/www/afimperiya/venv/bin"
ExecStart=/var/www/afimperiya/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable afimperiya
sudo systemctl start afimperiya
sudo systemctl status afimperiya
```

## 4. Docker bilan Deploy qilish

### Dockerfile:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Docker Compose:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/afimperiya
      - SECRET_KEY=your-secret-key
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=afimperiya
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Ishga tushirish:

```bash
# Build va run
docker-compose up -d

# Logsni ko'rish
docker-compose logs -f

# To'xtatish
docker-compose down
```

## 5. Telegram Bot Sozlash

### Bot yaratish:

1. Telegram'da @BotFather ni toping
2. `/newbot` komandasi
3. Bot nomini va username kiriting
4. Token ni copy qiling

### Webhook sozlash:

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://your-domain.com/telegram/webhook"
```

### Chat ID topish:

1. Bot ga xabar yuboring
2. Quyidagi URL'ni ochib, chat_id ni toping:
```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
```

## 6. Production Checklist

- [ ] SECRET_KEY o'zgartirildi
- [ ] Debug mode o'chirilgan
- [ ] PostgreSQL database sozlandi
- [ ] Environment variables to'g'ri kiritildi
- [ ] SSL sertifikat o'rnatildi (Let's Encrypt)
- [ ] Database backup sozlandi
- [ ] Monitoring sozlandi
- [ ] Logging sozlandi
- [ ] Telegram bot test qilindi
- [ ] Admin parol o'zgartirildi

## 7. Muammolarni Hal Qilish

### Database xatoliklari:

```bash
# Database yaratish
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
```

### Telegram bot ishlamayotgan:

- Token to'g'ri kiritilganini tekshiring
- Internet ulanishini tekshiring
- Bot'ni restart qiling

### 500 Internal Server Error:

- Logsni ko'ring: `railway logs` yoki `docker logs`
- Environment variables tekshiring
- Database connection tekshiring

## 8. Qo'shimcha Ma'lumotlar

### Monitoring:

- Render.com: Built-in monitoring
- Railway: Built-in logs and metrics
- Custom: Sentry, New Relic, Datadog

### Backup:

```bash
# Database backup
pg_dump $DATABASE_URL > backup.sql

# Fayllar backup
tar -czf uploads_backup.tar.gz uploads/
```

### Yangilash:

```bash
git add .
git commit -m "Update message"
git push origin main
```

Render va Railway avtomatik deploy qiladi.

---

**Yordam kerakmi?**
- GitHub Issues: https://github.com/your-repo/issues
- Email: support@afimperiya.uz
