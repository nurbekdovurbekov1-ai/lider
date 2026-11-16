from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_auto_parts"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="stock",
            field=models.PositiveIntegerField(
                default=0,
                help_text="Omborda nechta dona qolgani",
                verbose_name="Qoldiq (dona)",
            ),
        ),
    ]
