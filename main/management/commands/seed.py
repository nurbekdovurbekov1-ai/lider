import io
from django.conf import settings
import re
from django.core.management.base import BaseCommand
from django.core.files.uploadedfile import SimpleUploadedFile
from main.models import (
    CustomUser, Category, CarModel, Product, ProductImage,
    SiteSettings, Banner, Address,
)
from .seed_data import CAR_MODELS, CATEGORIES, PRODUCTS

CAT_SLUG = {
    "Yogʻlar": "yoglar", "Tormoz": "tormoz", "Filtrlar": "filtrlar", "Elektr": "elektr",
    "Dvigatel": "dvigatel", "Yoritish": "yoritish", "Osma": "osma", "Sovitish": "sovitish",
    "Uzatma": "uzatma", "Kuzov": "kuzov", "Salon": "salon",
}
ORIGINAL = {"Bosch", "Mann", "Mahle", "Gates", "NGK", "Valeo"}
PREMIUM = {"Brembo", "Castrol", "Sachs", "Varta", "Philips", "Denso", "TRW", "ATE", "GKN"}
TILE_COLORS = ["#12307a", "#1f4fb5", "#0f2a5c", "#2457c9", "#16244a"]


def slugify_uz(text):
    text = text.lower().replace("ʻ", "").replace("ʼ", "").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def make_image(text, size=(800, 600), color="#12307a", name="image.jpg"):
    """Pillow bilan oddiy rasm (placeholder). Haqiqiy rasmlarni admin paneldan yuklang."""
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", size, color)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, size[1] - 14, size[0], size[1]], fill="#ff7a00")
    try:
        font = ImageFont.load_default(size=36)
    except TypeError:
        font = ImageFont.load_default()
    lines, line = [], ""
    for word in text.split():
        if len(line) + len(word) + 1 > 22:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    lines.append(line)
    y = size[1] // 2 - 22 * len(lines)
    for ln in lines:
        w = draw.textlength(ln, font=font) if hasattr(draw, "textlength") else 0
        draw.text(((size[0] - w) / 2, y), ln, fill="white", font=font)
        y += 48
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=85)
    return SimpleUploadedFile(name=name, content=buf.getvalue(), content_type="image/jpeg")


class Command(BaseCommand):
    help = "Bazani Lider Avto namunaviy maʼlumotlari bilan toʻldirish"

    def handle(self, *args, **kwargs):
        self.stdout.write("Maʼlumotlar yaratish boshlandi...")

        # 1. Sayt sozlamalari (namuna — admin paneldan oʻzgartiring)
        s, _ = SiteSettings.objects.get_or_create(pk=1)
        s.phone_main = "+998900000000"
        s.phone_whatsapp = "+998900000000"
        s.email = "info@liderauto.uz"
        s.address = "Shahar, koʻcha, uy (manzilingizni kiriting)"
        s.work_hours = "Du-Sha 09:00 dan 19:00 gacha"
        s.telegram_url = "https://t.me/liderauto"
        s.instagram_url = "https://instagram.com/liderauto"
        s.footer_about = "Lider Avto — Chevrolet (Nexia, Lacetti, Gentra, Cobalt, Spark) va boshqa yengil avtomobillar uchun original va sifatli ehtiyot qismlar."
        s.footer_copyright = "Lider Avto. Barcha huquqlar himoyalangan."
        s.site_title = "Lider Avto — avto ehtiyot qismlar"
        s.save()

        # 2. Bannerlar
        Banner.objects.all().delete()
        # Banner rasmlarini admin paneldan yuklang (Bannerlar). Yuklanmaguncha chiroyli gradient ko'rinadi.

        # 3. Kategoriyalar va mashina turlari
        Category.objects.all().delete()
        cats = {}
        for i, (name, slug) in enumerate(CATEGORIES, 1):
            cats[slug] = Category.objects.create(name=name, slug=slug, order=i)
        CarModel.objects.all().delete()
        cars = {}
        for i, name in enumerate(CAR_MODELS, 1):
            cars[name] = CarModel.objects.create(name=name, slug=slugify_uz(name), order=i)

        # 4. Mahsulotlar
        Product.objects.all().delete()
        used = set()
        for i, d in enumerate(PRODUCTS, 1):
            slug = slugify_uz(d["n"]) or f"mahsulot-{i}"
            if slug in used:
                slug = f"{slug}-{i}"
            used.add(slug)
            old = d.get("o") or 0
            on_sale = old and (1 - d["p"] / old) >= 0.2
            badge = "sale" if on_sale else ("hit" if d["r"] >= 4.8 else ("new" if i % 9 == 0 else ""))
            quality = "original" if d["b"] in ORIGINAL else ("premium" if d["b"] in PREMIUM else "analog")
            product = Product.objects.create(
                category=cats[CAT_SLUG[d["c"]]], name=d["n"], slug=slug, description=d["d"],
                quality=quality, base_price=d["p"], price_type="fixed",
                badge=badge, status="sale" if on_sale else "active",
                brand=d["b"], article=d["a"], warranty="6 oy", usage=d["u"],
                stock=20 + (i * 7) % 60,
                delivery_info="Shahar boʻyicha 1–2 kun ichida yetkazib beramiz.",
            )
            names = [n for n in CAR_MODELS if n in d["m"]]
            product.car_models.set([cars[n] for n in (names or CAR_MODELS)])

        # 5. Test foydalanuvchi va manzil (faqat lokal DEBUG rejimida, productionda yaratilmaydi)
        if settings.DEBUG:
            user, created = CustomUser.objects.get_or_create(phone_number="+998901112233")
            if created:
                user.set_password("password123")
                user.full_name = "Test Mijoz"
                user.save()
            Address.objects.get_or_create(
                user=user, region="tashkent_city", city="Toshkent", street="Amir Temur", house_number="15",
                defaults={"full_address": "Toshkent sh., Amir Temur koʻchasi, 15-uy", "is_default": True},
            )

        self.stdout.write(self.style.SUCCESS(f"Tayyor: {len(PRODUCTS)} ta mahsulot, {len(CAR_MODELS)} ta mashina turi."))
        self.stdout.write("Mahsulot rasmlari yo'q. Haqiqiy rasmlarni qo'shish: data/products.xlsx + data/photos, keyin python manage.py import_products data/products.xlsx --images data/photos")
        if settings.DEBUG:
            self.stdout.write("Test user logini: +998901112233")
            self.stdout.write("Test user paroli: password123")
