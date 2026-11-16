# Lider Avto — avto ehtiyot qismlar do'koni

Django (REST API) + Vue 3 (Vite, Tailwind) loyihasi. Dastlab eshik-deraza do'koni (Saramax/AKFA) edi,
endi **Lider Avto** — Chevrolet (Nexia, Lacetti, Gentra, Cobalt, Spark ...) va boshqa yengil avtomobillar
uchun ehtiyot qismlar do'koniga moslangan.

## Nimalar o'zgardi

**Brend va dizayn**
- Nom, logotip, favicon, meta teglar, footer, admin panel va hisobotlar — "Lider Avto".
- Ranglar: to'q ko'k (brand) va apelsin (accent) — `frontend/tailwind.config.js` va `src/styles/main.css`.

**Mahsulot tuzilishi (eshik-deraza → ehtiyot qism)**
- Narx endi **1 dona uchun** (kv.m kalkulyatori va o'lchamlar olib tashlandi). Savatga o'lcham yuborilmaydi.
- Yangi: **Mashina turlari** (`CarModel`) va mahsulotning "Mos mashinalar" maydoni.
- Maydonlar qayta nomlandi: `material → quality` (Original/Analog/Premium), `profile_thickness → brand`,
  `max_glass → article` (artikul), `sound_insulation → warranty` (kafolat), `climate_resistance → usage`
  ("Nima uchun ishlatiladi"). `design_style` olib tashlandi. Badge: `warm → hit` ("Ommabop").
- Ranglar ("ProductColor") endi ixtiyoriy **variantlar** sifatida (masalan: Original / Analog, har birining narxi bilan).

**Sahifalar**
- Bosh sahifa: "Mashinangizni tanlang" bloki, kategoriyalar, afzalliklar.
- Katalog: filtr **mashina turi** bo'yicha (`/catalog?car=nexia`), kategoriya, qidiruv (nom, brend, artikul).
- Mahsulot sahifasi: brend, artikul, mos mashinalar, "Nima uchun ishlatiladi?", miqdor tanlash.
- Admin: mahsulot formasida mashina turlarini belgilash, brend/artikul/kafolat/foydalanish maydonlari.
- API: `GET /api/car-models/`, `GET /api/products/?car=<slug>&category=<slug>&quality=&brand=`.

**Ma'lumotlar**
- `python manage.py seed` — 11 kategoriya, 12 mashina turi, 64 ta namunaviy mahsulot (rasmsiz), banner va sayt sozlamalari.
  Narxlar, artikullar, moslik va telefon/manzil **namuna** — o'zingizniki bilan almashtiring.
- Rasmsiz mahsulotda toza "Rasm tez orada qo'shiladi" belgisi chiqadi (soxta rasm yo'q).

## Mahsulotlarni haqiqiy rasmlari bilan ommaviy yuklash

1. `data/products.xlsx` ni oching: 64 ta namunaviy qator bor. Narx, artikul, tavsifni to'g'rilang, yangi qatorlar qo'shing
   (ustunlar: nomi, kategoriya, mashinalar, brend, artikul, narx, sifat, kafolat, tavsif, ishlatilishi, yorliq, rasm).
2. Haqiqiy fotosuratlarni `data/photos/` papkasiga **artikul nomi** bilan qo'ying: `BS-0986-F.jpg` (asosiy),
   `BS-0986-F_2.jpg`, `BS-0986-F_3.jpg` (qo'shimcha). Format: jpg, png, webp.
3. Yuklang:
   ```bash
   python manage.py import_products data/products.xlsx --images data/photos --dry-run   # avval tekshirish
   python manage.py import_products data/products.xlsx --images data/photos
   ```
   Artikul bo'yicha mavjud mahsulot yangilanadi, yangisi yaratiladi. Rasm topilmasa ro'yxat chiqadi.
   Rasmlarni almashtirish: `--replace-images`. Alohida mahsulot/rasm: admin panel -> Mahsulotlar.

## Ishga tushirish

**Eng oson yo'l (Mac/Linux):** loyiha papkasida `bash start.sh` — venv, kutubxonalar, migratsiya, namunaviy ma'lumotlar,
backend va frontend hammasini o'zi qiladi. Xato bo'lsa, aniq qaysi qadamda to'xtaganini yozadi.
Holatni tekshirish: `python manage.py doctor` (kategoriya/mashina/mahsulot soni).

Qo'lda:

Backend:
```bash
python -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed
python manage.py createsuperuser                      # admin akkaunt (telefon raqam + parol)
python manage.py runserver                            # http://127.0.0.1:8000
```
Frontend:
```bash
cd frontend
npm install
npm run dev                                           # http://localhost:3005
```
Test mijoz: `+998901112233` / `password123`. Admin panel: `/admin`, Swagger: `/api/docs/`.

## Muhim
- Bu o'zgartirishlar kod darajasida bajarilgan; sizning muhitingizda `migrate` va `npm run dev` bilan ishga tushirib tekshiring.
- Eski bazangiz bo'lsa: `0007_auto_parts` migratsiyasi maydonlarni qayta nomlaydi, ma'lumotlar saqlanadi, lekin
  eshik-deraza mahsulotlari qoladi. Toza boshlash uchun `db.sqlite3` ni o'chirib, `migrate` va `seed` qiling.
- `config/settings.py` da `DEBUG=True`, `SECRET_KEY` va `CORS_ALLOW_ALL_ORIGINS` ishlab chiqarish uchun mos emas.
  Serverga chiqarishdan oldin `deploy/SERVER_SETUP.md` dagi ko'rsatmalarga qarang va bu qiymatlarni almashtiring.
# lider
