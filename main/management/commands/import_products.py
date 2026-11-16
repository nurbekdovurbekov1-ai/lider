"""
Mahsulotlarni Excel (.xlsx) yoki CSV fayldan ommaviy yuklash, rasmlari bilan.

Ishlatish:
    python manage.py import_products data/products.xlsx --images data/photos
    python manage.py import_products data/products.csv  --images data/photos --dry-run

Fayl ustunlari (birinchi qator — sarlavha; o'zbekcha yoki inglizcha nom bo'lishi mumkin):
    nomi | kategoriya | mashinalar | brend | artikul | narx | sifat | kafolat | tavsif | ishlatilishi | yorliq | rasm

Rasmlar:  --images papkasiga artikul nomi bilan qo'ying:  BS-0986-F.jpg  (asosiy rasm),
          BS-0986-F_2.jpg, BS-0986-F_3.jpg ... (qo'shimcha rasmlar).
          Yoki "rasm" ustuniga fayl nomini yozing (bir nechta bo'lsa vergul bilan).
Mahsulot artikul bo'yicha topiladi: bor bo'lsa yangilanadi, yo'q bo'lsa yaratiladi.
"""
import csv
import io
import os
import re
from decimal import Decimal, InvalidOperation

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from main.models import Category, CarModel, Product, ProductImage

ALIASES = {
    "name": ["name", "nomi", "nom", "mahsulot"],
    "category": ["category", "kategoriya"],
    "cars": ["cars", "mashinalar", "mashina", "car_models", "mos mashinalar"],
    "brand": ["brand", "brend"],
    "article": ["article", "artikul", "kod"],
    "price": ["price", "narx", "narxi"],
    "quality": ["quality", "sifat", "sifat turi"],
    "warranty": ["warranty", "kafolat"],
    "description": ["description", "tavsif", "izoh"],
    "usage": ["usage", "ishlatilishi", "nima uchun ishlatiladi"],
    "badge": ["badge", "yorliq"],
    "image": ["image", "rasm", "rasmlar", "images"],
}
QUALITY = {"original": "original", "analog": "analog", "premium": "premium",
           "analog (sifatli)": "analog", "asl": "original"}
BADGE = {"new": "new", "yangi": "new", "hit": "hit", "ommabop": "hit", "sale": "sale", "aksiya": "sale", "sotuvda": "sale"}
IMG_EXT = (".jpg", ".jpeg", ".png", ".webp")


def slugify_uz(text):
    text = str(text).lower().replace("ʻ", "").replace("ʼ", "").replace("'", "").replace("’", "")
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def norm_header(h):
    h = str(h or "").strip().lower()
    for key, names in ALIASES.items():
        if h in names:
            return key
    return None


def read_rows(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xlsm"):
        from openpyxl import load_workbook
        ws = load_workbook(path, read_only=True, data_only=True).active
        rows = list(ws.iter_rows(values_only=True))
    elif ext == ".csv":
        with open(path, encoding="utf-8-sig", newline="") as f:
            sample = f.read(2048)
            f.seek(0)
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t") if sample else csv.excel
            rows = list(csv.reader(f, dialect))
    else:
        raise CommandError("Fayl .xlsx yoki .csv bo'lishi kerak")
    if not rows:
        return []
    cols = [norm_header(h) for h in rows[0]]
    out = []
    for r in rows[1:]:
        d = {}
        for k, v in zip(cols, r):
            if k and v is not None and str(v).strip() != "":
                d[k] = str(v).strip()
        if d.get("name"):
            out.append(d)
    return out


def to_price(v):
    s = re.sub(r"[^\d.,]", "", str(v))
    if re.fullmatch(r"\d+[.,]\d{1,2}", s):      # 289000.50  -> o'nli kasr
        s = s.replace(",", ".")
    else:                                          # 1,250,000 yoki 1.250.000 -> mingliklar ajratgichi
        s = re.sub(r"[.,]", "", s)
    try:
        return Decimal(s or "0")
    except InvalidOperation:
        return Decimal("0")


def prepare_image(data, name):
    """Rasmni tekshiradi, kattaligini cheklaydi va JPEG qilib qaytaradi."""
    from PIL import Image
    img = Image.open(io.BytesIO(data))
    img.load()
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        bg = Image.new("RGB", img.size, "white")
        bg.paste(img, mask=img.split()[-1])
        img = bg
    else:
        img = img.convert("RGB")
    img.thumbnail((1600, 1600))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=88, optimize=True)
    return ContentFile(buf.getvalue(), name=f"{slugify_uz(name)}.jpg")


class Command(BaseCommand):
    help = "Mahsulotlarni Excel/CSV dan rasmlari bilan ommaviy yuklash"

    def add_arguments(self, parser):
        parser.add_argument("file", help="products.xlsx yoki products.csv")
        parser.add_argument("--images", default="data/photos", help="Rasmlar papkasi (default: data/photos)")
        parser.add_argument("--replace-images", action="store_true", help="Mavjud rasmlarni yangilari bilan almashtirish")
        parser.add_argument("--dry-run", action="store_true", help="Faqat tekshirish, bazaga yozmaslik")

    def handle(self, *args, **opts):
        rows = read_rows(opts["file"])
        if not rows:
            raise CommandError("Faylda mahsulot topilmadi (sarlavha qatori va 'nomi' ustuni kerak)")
        img_dir = opts["images"]
        files = {}
        if os.path.isdir(img_dir):
            for fn in os.listdir(img_dir):
                if fn.lower().endswith(IMG_EXT):
                    files[fn.lower()] = os.path.join(img_dir, fn)
        else:
            self.stdout.write(self.style.WARNING(f"Rasmlar papkasi topilmadi: {img_dir} (rasmsiz yuklanadi)"))

        created = updated = with_img = 0
        no_img, bad = [], []
        all_cars = list(CarModel.objects.filter(is_active=True))

        for i, d in enumerate(rows, 2):
            article = d.get("article", "")
            price = to_price(d.get("price", "0"))
            if price <= 0:
                bad.append(f"{i}-qator: '{d['name']}' — narx yo'q yoki noto'g'ri")
                continue
            if opts["dry_run"]:
                created += 1
                continue

            cat_name = d.get("category") or "Boshqa"
            category, _ = Category.objects.get_or_create(
                slug=slugify_uz(cat_name), defaults={"name": cat_name, "order": Category.objects.count() + 1})

            product = Product.objects.filter(article=article).first() if article else None
            is_new = product is None
            if is_new:
                product = Product(name=d["name"])
                base = slugify_uz(d["name"]) or f"mahsulot-{i}"
                slug, n = base, 1
                while Product.objects.filter(slug=slug).exists():
                    n += 1
                    slug = f"{base}-{n}"
                product.slug = slug
            product.name = d["name"]
            product.category = category
            product.base_price = price
            product.price_type = "fixed"
            product.brand = d.get("brand", product.brand)
            product.article = article
            product.warranty = d.get("warranty", product.warranty or "6 oy")
            product.description = d.get("description", product.description)
            product.usage = d.get("usage", product.usage)
            q = QUALITY.get(d.get("quality", "").lower())
            if q:
                product.quality = q
            b = BADGE.get(d.get("badge", "").lower())
            if b is not None:
                product.badge = b
            product.is_active = True
            product.save()

            # mos mashinalar
            cars_raw = d.get("cars", "")
            if cars_raw:
                if re.search(r"barcha|hammasi|all", cars_raw, re.I):
                    product.car_models.set(all_cars)
                else:
                    cars = []
                    for name in re.split(r"[,;/]", cars_raw):
                        name = name.strip()
                        if name:
                            c, _ = CarModel.objects.get_or_create(
                                slug=slugify_uz(name), defaults={"name": name, "order": CarModel.objects.count() + 1})
                            cars.append(c)
                    product.car_models.set(cars)

            # rasmlar
            names = []
            if d.get("image"):
                names += [x.strip().lower() for x in re.split(r"[,;]", d["image"]) if x.strip()]
            if article:
                a = article.lower()
                for fn in sorted(files):
                    stem = os.path.splitext(fn)[0]
                    if (stem == a or stem.startswith(a + "_")) and fn not in names:
                        names.append(fn)
            paths = [files[n] for n in names if n in files]
            missing = [n for n in names if n not in files]
            if missing:
                bad.append(f"{i}-qator: '{d['name']}' — rasm topilmadi: {', '.join(missing)}")
            if paths and (opts["replace_images"] or not product.images.exists()):
                product.images.all().delete()
                for k, pth in enumerate(paths):
                    with open(pth, "rb") as fh:
                        try:
                            content = prepare_image(fh.read(), f"{article or product.slug}-{k+1}")
                        except Exception as e:
                            bad.append(f"{i}-qator: '{os.path.basename(pth)}' rasm ochilmadi ({e})")
                            continue
                    ProductImage.objects.create(product=product, image=content, is_main=(k == 0), order=k)
            if product.images.exists():
                with_img += 1
            else:
                no_img.append(f"{article or '-'}  {d['name']}")
            created += is_new
            updated += (not is_new)

        if opts["dry_run"]:
            self.stdout.write(self.style.SUCCESS(f"Tekshiruv: {created} ta mahsulot yuklashga tayyor, {len(bad)} ta muammo."))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"Tayyor: {created} ta yangi, {updated} ta yangilandi. Rasmli: {with_img}, rasmsiz: {len(no_img)}."))
        for line in bad:
            self.stdout.write(self.style.WARNING("  ! " + line))
        if no_img and len(no_img) <= 30:
            self.stdout.write("Rasmsiz mahsulotlar (rasm fayli artikul nomi bilan data/photos ga qo'yilsin):")
            for line in no_img:
                self.stdout.write("   - " + line)
