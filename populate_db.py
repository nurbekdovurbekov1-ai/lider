"""Eski skript o'rniga: bazani Lider Avto namunaviy ma'lumotlari bilan to'ldiradi.
Ishlatish:  python populate_db.py   (yoki)   python manage.py seed"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.core.management import call_command

if __name__ == "__main__":
    call_command("seed")
