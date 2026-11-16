"""Tekshiruv: baza va maʼlumotlar holatini koʻrsatadi.
    python manage.py doctor                 # faqat tekshirish
    python manage.py doctor --seed-if-empty # mahsulot yoʻq boʻlsa namunaviy maʼlumotni yuklaydi
"""
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Baza va maʼlumotlar holatini tekshirish"

    def add_arguments(self, parser):
        parser.add_argument("--seed-if-empty", action="store_true")

    def handle(self, *args, **opts):
        from main.models import Category, CarModel, Product, ProductImage, Banner
        tables = connection.introspection.table_names()
        for t in ("main_product", "main_carmodel", "main_category"):
            if t not in tables:
                self.stdout.write(self.style.ERROR(f"Jadval yoʻq: {t}. Avval: python manage.py migrate"))
                return
        n = Product.objects.count()
        if n == 0 and opts["seed_if_empty"]:
            self.stdout.write("Mahsulotlar yoʻq, namunaviy maʼlumot yuklanmoqda (seed)...")
            call_command("seed")
            n = Product.objects.count()
        self.stdout.write(f"Kategoriyalar : {Category.objects.count()}")
        self.stdout.write(f"Mashina turlari: {CarModel.objects.count()}")
        self.stdout.write(f"Mahsulotlar    : {n}  (rasmli: {Product.objects.filter(images__isnull=False).distinct().count()})")
        self.stdout.write(f"Bannerlar      : {Banner.objects.count()}")
        if n == 0:
            self.stdout.write(self.style.WARNING("Mahsulot yoʻq -> python manage.py seed"))
        else:
            self.stdout.write(self.style.SUCCESS("Baza tayyor. API: http://127.0.0.1:8000/api/products/"))
