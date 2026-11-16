from rest_framework import serializers
from django.utils.text import slugify
from ..models import Product, ProductImage, ProductColor, Order, CustomUser, Category, CarModel


class AdminProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['created_at', 'updated_at']
        extra_kwargs = {
            'slug': {'required': False, 'allow_blank': True},
            'quality': {'required': False, 'allow_blank': True},
            'car_models': {'required': False},
            'description': {'required': False, 'allow_blank': True},
            'badge': {'required': False, 'allow_blank': True},
            'status': {'required': False},
            'is_active': {'required': False},
            'price_type': {'required': False},
            'brand': {'required': False, 'allow_blank': True},
            'article': {'required': False, 'allow_blank': True},
            'warranty': {'required': False, 'allow_blank': True},
            'usage': {'required': False, 'allow_blank': True},
            'delivery_info': {'required': False, 'allow_blank': True},
        }


class AdminOrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.Status.choices)


class AdminDashboardSerializer(serializers.Serializer):
    total_orders = serializers.IntegerField()
    today_orders = serializers.IntegerField()
    pending_orders = serializers.IntegerField()
    total_products = serializers.IntegerField()
    total_customers = serializers.IntegerField()
    monthly_revenue = serializers.DecimalField(max_digits=20, decimal_places=2)
    order_by_status = serializers.DictField()


class AdminCustomerSerializer(serializers.ModelSerializer):
    orders_count = serializers.IntegerField(read_only=True)
    total_spent = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'full_name', 'is_active', 'created_at', 'orders_count', 'total_spent']



def make_unique_slug(model, source, exclude_pk=None, fallback="item"):
    """name dan takrorlanmas slug yasaydi (nexia, nexia-2, nexia-3 ...)."""
    base = slugify(source) or fallback
    slug, n = base, 2
    qs = model.objects.all()
    if exclude_pk:
        qs = qs.exclude(pk=exclude_pk)
    while qs.filter(slug=slug).exists():
        slug = f"{base}-{n}"
        n += 1
    return slug


class AdminCategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)
    remove_icon = serializers.BooleanField(write_only=True, required=False, default=False)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "icon", "order", "is_active", "products_count", "remove_icon"]
        extra_kwargs = {
            "slug": {"required": False, "allow_blank": True},
            "icon": {"required": False, "allow_null": True},
            "order": {"required": False},
            "is_active": {"required": False},
        }

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Nomi bo'sh bo'lishi mumkin emas")
        return value

    def validate_slug(self, value):
        value = slugify(value) if value else ""
        if value:
            qs = Category.objects.filter(slug=value)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("Bunday slug allaqachon mavjud")
        return value

    def create(self, validated_data):
        validated_data.pop("remove_icon", None)
        if not validated_data.get("slug"):
            validated_data["slug"] = make_unique_slug(Category, validated_data["name"], fallback="kategoriya")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        remove_icon = validated_data.pop("remove_icon", False)
        if "slug" in validated_data and not validated_data["slug"]:
            validated_data.pop("slug")
        if remove_icon and "icon" not in validated_data:
            if instance.icon:
                instance.icon.delete(save=False)
            instance.icon = None
        return super().update(instance, validated_data)


class AdminCarModelSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CarModel
        fields = ["id", "name", "slug", "order", "is_active", "products_count"]
        extra_kwargs = {
            "slug": {"required": False, "allow_blank": True},
            "order": {"required": False},
            "is_active": {"required": False},
        }

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Nomi bo'sh bo'lishi mumkin emas")
        return value

    def validate_slug(self, value):
        value = slugify(value) if value else ""
        if value:
            qs = CarModel.objects.filter(slug=value)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("Bunday slug allaqachon mavjud")
        return value

    def create(self, validated_data):
        if not validated_data.get("slug"):
            validated_data["slug"] = make_unique_slug(CarModel, validated_data["name"], fallback="mashina")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "slug" in validated_data and not validated_data["slug"]:
            validated_data.pop("slug")
        return super().update(instance, validated_data)
