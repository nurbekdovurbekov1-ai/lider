from django.db import models


class About(models.Model):
    """
    Biz haqimizda sahifasi ma'lumotlari (Singleton).
    Admin panel orqali boshqariladi.
    """
    title = models.CharField(
        max_length=200,
        default="Lider Avto haqida",
        verbose_name="Sarlavha"
    )
    subtitle = models.CharField(
        max_length=300,
        blank=True,
        default="Sifatli va ishonchli mahsulotlar yetkazib beruvchisi",
        verbose_name="Qisqa izoh / Shior"
    )
    content = models.TextField(
        verbose_name="Asosiy matn / Kompaniya haqida",
        default="Lider Avto — avtomobillar uchun original va sifatli ehtiyot qismlar do'koni. Nexia, Lacetti, Gentra, Cobalt, Spark va boshqa Chevrolet modellari uchun keng assortiment, qulay narxlar va tez yetkazib berish. Bizning ustuvorligimiz — to'g'ri qismni tez topib berish va kafolat bilan sotish."
    )
    image = models.ImageField(
        upload_to="about/",
        blank=True,
        null=True,
        verbose_name="Kompaniya / Do'kon rasmi"
    )
    experience_years = models.CharField(
        max_length=50,
        blank=True,
        default="5+",
        verbose_name="Tajriba ko'rsatkichi (masalan: 5+ yil)"
    )

    # Statistika ko'rsatkichlari
    stat_1_number = models.CharField(max_length=50, blank=True, default="1000+", verbose_name="Statistika 1 raqam")
    stat_1_label = models.CharField(max_length=100, blank=True, default="Ehtiyot qism turlari", verbose_name="Statistika 1 nomi")

    stat_2_number = models.CharField(max_length=50, blank=True, default="10,000+", verbose_name="Statistika 2 raqam")
    stat_2_label = models.CharField(max_length=100, blank=True, default="Mamnun mijozlar", verbose_name="Statistika 2 nomi")

    stat_3_number = models.CharField(max_length=50, blank=True, default="100%", verbose_name="Statistika 3 raqam")
    stat_3_label = models.CharField(max_length=100, blank=True, default="Sifat kafolati", verbose_name="Statistika 3 nomi")

    stat_4_number = models.CharField(max_length=50, blank=True, default="24/7", verbose_name="Statistika 4 raqam")
    stat_4_label = models.CharField(max_length=100, blank=True, default="Qo'llab-quvvatlash", verbose_name="Statistika 4 nomi")

    # Missiya va qadriyatlar
    mission = models.TextField(
        blank=True,
        default="Har bir haydovchiga kerakli ehtiyot qismni tez, original va hamyonbop narxda yetkazib berish.",
        verbose_name="Bizning missiyamiz"
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Biz haqimizda sahifasi"
        verbose_name_plural = "Biz haqimizda sahifasi"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_about(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
