from django.db import migrations, models


class Migration(migrations.Migration):
    """Saramax (eshik-deraza) -> Lider Avto (avto ehtiyot qismlar)."""

    dependencies = [
        ("main", "0006_productcolor_price"),
    ]

    operations = [
        migrations.CreateModel(
            name="CarModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=60, verbose_name="Mashina nomi")),
                ("slug", models.SlugField(max_length=80, unique=True, verbose_name="Slug")),
                ("order", models.PositiveSmallIntegerField(default=0, verbose_name="Tartib")),
                ("is_active", models.BooleanField(default=True, verbose_name="Faol")),
            ],
            options={
                "verbose_name": "Mashina turi",
                "verbose_name_plural": "Mashina turlari",
                "ordering": ["order", "name"],
            },
        ),
        migrations.RenameField(model_name="product", old_name="material", new_name="quality"),
        migrations.RenameField(model_name="product", old_name="profile_thickness", new_name="brand"),
        migrations.RenameField(model_name="product", old_name="max_glass", new_name="article"),
        migrations.RenameField(model_name="product", old_name="sound_insulation", new_name="warranty"),
        migrations.RenameField(model_name="product", old_name="climate_resistance", new_name="usage"),
        migrations.RemoveField(model_name="product", name="design_style"),
        migrations.AlterField(
            model_name="product",
            name="quality",
            field=models.CharField(
                blank=True,
                choices=[("original", "Original"), ("analog", "Analog (sifatli)"), ("premium", "Premium")],
                max_length=20,
                verbose_name="Sifat turi",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="brand",
            field=models.CharField(blank=True, max_length=60, verbose_name="Brend"),
        ),
        migrations.AlterField(
            model_name="product",
            name="article",
            field=models.CharField(blank=True, max_length=40, verbose_name="Artikul"),
        ),
        migrations.AlterField(
            model_name="product",
            name="warranty",
            field=models.CharField(blank=True, max_length=40, verbose_name="Kafolat"),
        ),
        migrations.AlterField(
            model_name="product",
            name="usage",
            field=models.TextField(blank=True, verbose_name="Nima uchun ishlatiladi"),
        ),
        migrations.AlterField(
            model_name="product",
            name="badge",
            field=models.CharField(
                blank=True,
                choices=[("new", "Yangi"), ("hit", "Ommabop"), ("sale", "Sotuvda")],
                default="",
                max_length=10,
                verbose_name="Badge (yorliq)",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="price_type",
            field=models.CharField(
                choices=[("per_sqm", "Kv.m uchun"), ("fixed", "Qat'iy narx")],
                default="fixed",
                max_length=10,
                verbose_name="Narx turi",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="base_price",
            field=models.DecimalField(
                decimal_places=2,
                help_text="Bir dona uchun narx (UZS)",
                max_digits=12,
                verbose_name="Asosiy narx (UZS)",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="car_models",
            field=models.ManyToManyField(blank=True, related_name="products", to="main.carmodel", verbose_name="Mos mashinalar"),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="footer_copyright",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Masalan: © 2026 Lider Avto. Barcha huquqlar himoyalangan.",
                max_length=200,
                verbose_name="Copyright matni",
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="site_title",
            field=models.CharField(blank=True, default="Lider Avto", max_length=100, verbose_name="Sayt nomi (SEO title)"),
        ),
        migrations.AlterField(
            model_name="about",
            name="title",
            field=models.CharField(default="Lider Avto haqida", max_length=200, verbose_name="Sarlavha"),
        ),
        migrations.AlterField(
            model_name="about",
            name="subtitle",
            field=models.CharField(
                blank=True,
                default="Sifatli va ishonchli mahsulotlar yetkazib beruvchisi",
                max_length=300,
                verbose_name="Qisqa izoh / Shior",
            ),
        ),
            migrations.AlterField(
            model_name="about",
            name="content",
            field=models.TextField(
                default="Lider Avto — avtomobillar uchun original va sifatli ehtiyot qismlar do'koni. Nexia, Lacetti, Gentra, Cobalt, Spark va boshqa Chevrolet modellari uchun keng assortiment, qulay narxlar va tez yetkazib berish. Bizning ustuvorligimiz — to'g'ri qismni tez topib berish va kafolat bilan sotish.",
                verbose_name="Asosiy matn / Kompaniya haqida",
            ),
        ),
        migrations.AlterField(
            model_name="about",
            name="mission",
            field=models.TextField(
                blank=True,
                default="Har bir haydovchiga kerakli ehtiyot qismni tez, original va hamyonbop narxda yetkazib berish.",
                verbose_name="Bizning missiyamiz",
            ),
        ),
        migrations.AlterField(
            model_name="about",
            name="stat_1_label",
            field=models.CharField(blank=True, default="Ehtiyot qism turlari", max_length=100, verbose_name="Statistika 1 nomi"),
        ),
    ]
