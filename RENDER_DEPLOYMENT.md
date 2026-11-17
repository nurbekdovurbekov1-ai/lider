# Render.com ga Deploy Qilish Qo'llanmasi

Bu qo'llanma Lider Avto loyihasini Render.com platformasiga deploy qilish uchun yaratilgan.

---

## 1. Render.com ga hisob yaratish

[render.com](https://render.com) saytiga kirib, GitHub hisobingiz bilan ro'yxatdan o'ting.

---

## 2. GitHub'da repository tayyorlash

Loyihani GitHub'ga push qiling:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/USERNAME/lider-avto-site.git
git push -u origin main
```

---

## 3. Render.com da yangi Web Service yaratish

### Variant A: render.yaml fayli orqali (avtomatik)

1. Render dashboardda "New +" tugmasini bosing
2. "Build and deploy from a Git repository"ni tanlang
3. GitHub repositoryingizni ulang
4. Render `render.yaml` faylini avtomatik topadi va 3 ta service yaratadi:
   - **lider-avto-backend** - Django backend (PostgreSQL bilan)
   - **lider-avto-db** - PostgreSQL database
   - **lider-avto-frontend** - Vue.js frontend

### Variant B: Qo'lda yaratish

#### Backend Service (Django)
1. "New Web Service" tugmasini bosing
2. Repositoryni tanlang
3. Quyidagilarni sozlang:
   - **Name**: lider-avto-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 90`
   - **Instance Type**: Free (yoki Pro)

4. Environment Variables qo'shing:
   ```
   DJANGO_SECRET_KEY=<random-secret-key>
   DJANGO_DEBUG=0
   DJANGO_ALLOWED_HOSTS=*.onrender.com
   DJANGO_HTTPS=1
   DJANGO_CSRF_TRUSTED_ORIGINS=https://*.onrender.com
   ```

5. PostgreSQL database ulang:
   - "Database" sectionda "PostgreSQL"ni tanlang
   - Database nomi: `lider-avto-db`

#### Frontend Service (Vue.js)
1. "New Static Site" tugmasini bosing
2. Repositoryni tanlang
3. Quyidagilarni sozlang:
   - **Name**: lider-avto-frontend
   - **Runtime**: Node
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`

4. Environment Variables:
   ```
   VITE_API_URL=https://lider-avto-backend.onrender.com
   ```

---

## 4. Django settings sozlamalari

`config/settings.py` faylida DATABASE_URL qo'llab-quvvatlanadi (allaqachon qo'shilgan).

---

## 5. Media fayllar uchun Disk qo'shish (ixtiyoriy)

Agar admin panel orqali rasm yuklamoqchi bo'lsangiz:

1. Backend service settingsiga o'ting
2. "Disks" sectionda "Add Disk" tugmasini bosing
3. Quyidagilarni sozlang:
   - **Name**: media-files
   - **Mount Path**: `/opt/render/project/media`
   - **Size**: 1 GB (yoki ko'proq)

---

## 6. Deploydan keyin

1. **Superuser yaratish**:
   Render dashboardda backend servicega o'ting
   - "Shell" tugmasini bosing (Pro plan)
   - Yoki local'dan SSH orqali ulaning
   ```bash
   python manage.py createsuperuser
   ```

2. **Test data yuklash** (ixtiyoriy):
   ```bash
   python manage.py seed
   ```

3. **Saytni tekshiring**:
   - Frontend: `https://lider-avto-frontend.onrender.com`
   - Backend API: `https://lider-avto-backend.onrender.com/api/`
   - Django Admin: `https://lider-avto-backend.onrender.com/django-admin/`

---

## 7. Docker bilan deploy (ixtiyoriy)

Agar Docker ishlatmoqchi bo'lsangiz:

```bash
# Docker image build qilish
docker build -t lider-avto .

# Docker container ishga tushirish
docker run -p 8000:8000 \
  -e DJANGO_SECRET_KEY="your-secret-key" \
  -e DJANGO_DEBUG=0 \
  -e DJANGO_ALLOWED_HOSTS="localhost" \
  lider-avto
```

---

## 8. Muhim eslatmalar

- **Free plan**: 15 daqiqadan keyin sleep bo'ladi, keyin 30-60 sekundda wake bo'ladi
- **Database**: Free plan PostgreSQL 90 kun o'tgach o'chiriladi (backup oling)
- **Media files**: Disk ishlatmasangiz, deploydan keyin rasm yo'qoladi
- **Environment variables**: Har doim `.env.example` ga qarang
- **HTTPS**: Render avtomatik HTTPS ta'minlaydi

---

## 9. Troubleshooting

### Build xatosi bo'lsa
- Render logsni tekshiring
- `requirements.txt` dagi package versiyalarini tekshiring
- Python versiyasi mos kelishini tekshiring (3.11+)

### Database ulanish xatosi
- `DATABASE_URL` environment variable to'g'ri ekanligini tekshiring
- PostgreSQL service ishlayotganini tekshiring

### Static files yuklanmasa
- `collectstatic` command build commandda bo'lishini tekshiring
- `STATIC_ROOT` sozlamasini tekshiring

---

## 10. Local'dan production databasega ulanish (ixtiyoriy)

```bash
# Render dashboardda PostgreSQL servicega o'ting
# "Connections" sectiondan External Database URL ni oling
# Local .env fayliga qo'shing:
DATABASE_URL=postgres://user:pass@host:port/dbname
```

---

**Muvaffaqiyatli deploy!** 🚀
