# Serverda (Ubuntu VPS) Loyihani O'rnatish Qo'llanmasi

Loyiha monorepo (Django Backend + Vue 3 Frontend) shaklida bo'lgani uchun serverda bitta papkada (`/var/www/lider-avto`) joylashadi va **Nginx** barcha so'rovlarni avtomatik boshqaradi.

---

## 1. Serverga kerakli dasturlarni o'rnatish
Serverga SSH orqali ulaning va quyidagi buyruqlarni bajaring:

```bash
# Tizimni yangilash
sudo apt update && sudo apt upgrade -y

# Python, Git, Nginx va muhim kutubxonalar
sudo apt install -y python3 python3-pip python3-venv git nginx curl libpq-dev

# Node.js (v20 LTS) va npm o'rnatish
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

---

## 2. Loyihani GitHub'dan serverga yuklash (Clone)

```bash
# Loyiha papkasini yaratish va unga o'tish
sudo mkdir -p /var/www
cd /var/www

# GitHub'dagi repository'ingizni clone qiling:
sudo git clone <GITHUB_REPO_URL> lider-avto
cd lider-avto

# Papka huquqlarini to'g'irlash
sudo chown -R $USER:$USER /var/www/lider-avto
sudo chmod -R 755 /var/www/lider-avto
```

---

## 3. Backend'ni sozlash (Django + Gunicorn)

```bash
cd /var/www/lider-avto

# Maxfiy sozlamalar (.env) — SECRET_KEY, domen/IP
cp .env.example .env
nano .env     # DJANGO_SECRET_KEY va DJANGO_ALLOWED_HOSTS ni to'ldiring

# Python virtual muhit (venv) yaratish va faollashtirish
python3 -m venv venv
source venv/bin/activate

# Kerakli kutubxonalarni o'rnatish
pip install -r requirements.txt

# Migratsiyalar
python manage.py migrate

# Boshlang'ich ma'lumotlar (kategoriyalar, mashina turlari, namunaviy mahsulotlar).
# DIQQAT: narxlar, artikullar va telefon raqamlari NAMUNA. Keyin o'zingiznikiga almashtiring.
python manage.py seed

# Superadmin yaratish (Dashboardga kirish uchun)
python manage.py createsuperuser

# Statik fayllarni yig'ish
python manage.py collectstatic --noinput
```

SECRET_KEY yaratish uchun:
```bash
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```

**Haqiqiy mahsulot va rasmlarni yuklash** (ixtiyoriy, `data/products.xlsx` ni to'ldirgandan keyin):
```bash
# Rasmlarni data/photos/ ga artikul nomi bilan qo'ying (masalan BS-0986-F.jpg), keyin:
python manage.py import_products data/products.xlsx --images data/photos
```

---

## 4. Frontend'ni build qilish (Vue 3)

```bash
cd /var/www/lider-avto/frontend

# Paketlarni o'rnatish va ishlab chiqarish (production) uchun build qilish
npm install
npm run build
```
*(Bu buyruq `/var/www/lider-avto/frontend/dist` papkasini hosil qiladi)*

---

## 5. Gunicorn Service'ni sozlash (Systemd)

Gunicorn xizmati server yonganda yoki qayta ishga tushganda Django'ni avtomatik fonda ishlatib turadi:

```bash
# Konfiguratsiyani nusxalash; __DEPLOY_USER__ o'rniga hozirgi foydalanuvchi nomi yoziladi (root EMAS)
sed "s/__DEPLOY_USER__/$USER/" /var/www/lider-avto/deploy/lider-avto.service | sudo tee /etc/systemd/system/lider-avto.service

# Tizimni yangilash va xizmatni yoqish
sudo systemctl daemon-reload
sudo systemctl start lider-avto
sudo systemctl enable lider-avto

# Holatini tekshirish
sudo systemctl status lider-avto
```

---

## 6. Nginx'ni sozlash

```bash
# Nginx konfiguratsiyasini nusxalash
sudo cp /var/www/lider-avto/deploy/nginx.conf /etc/nginx/sites-available/lider-avto

# Domeningiz bo'lsa, server_name qatoriga yozing (IP bilan ishlasangiz "_" qolaversin):
sudo nano /etc/nginx/sites-available/lider-avto

# Saytni faollashtirish (symlink)
sudo ln -s /etc/nginx/sites-available/lider-avto /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Nginx konfiguratsiyasini tekshirish va qayta yuklash
sudo nginx -t
sudo systemctl reload nginx
```

---

## 7. Bepul SSL (HTTPS) Sertifikatini o'rnatish (Ixtiyoriy, domen bo'lsa)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d sayt.uz -d www.sayt.uz
```
Keyin `.env` faylida `DJANGO_HTTPS=1` va `DJANGO_CSRF_TRUSTED_ORIGINS=https://sayt.uz,https://www.sayt.uz` qo'ying, so'ng `sudo systemctl restart lider-avto`.
Domen bo'lmasa, sayt faqat HTTP da ishlaydi: parollar shifrlanmay ketadi, shuning uchun real mijozlar uchun domen + HTTPS tavsiya etiladi.

---

## 8. Keyinchalik yangi kod yuklaganda (1 ta buyruq bilan yangilash)

Kodlarga o'zgartirish kiritib GitHub'ga push qilganingizdan keyin, serverda faqat quyidagi buyruqni ishga tushirasiz:

```bash
bash /var/www/lider-avto/deploy/deploy.sh
```
Bu skript avtomatik:
1. `git pull` qiladi
2. `pip install` va `migrate` qiladi
3. Frontendni yangitdan `npm run build` qiladi
4. Gunicorn va Nginx'ni qayta yuklaydi!

---

## 9. Ishga tushgandan keyin tekshiring

- `http://SERVER_IP/` — sayt ochiladimi
- `http://SERVER_IP/django-admin/` — admin kirish sahifasi
- Mahsulotlar ko'rinyaptimi, savatga qo'shish va buyurtma ishlayaptimi
- `sudo journalctl -u lider-avto -n 50` — gunicorn loglari (xatolar shu yerda)
- Namunaviy telefon raqamlar va manzilni admin paneldan o'zingiznikiga almashtiring
