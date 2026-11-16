from rest_framework import serializers
from ..models import Category, CarModel, Product, ProductImage, ProductColor


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'order']


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'name', 'slug', 'order']


class ProductColorSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    calculated_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductColor
        fields = ['id', 'name', 'hex_code', 'price', 'price_modifier', 'calculated_price', 'is_available']

    def get_calculated_price(self, obj):
        return round(obj.get_effective_price(), 2)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main', 'order']


class ProductListSerializer(serializers.ModelSerializer):
    in_stock = serializers.BooleanField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    main_image = serializers.SerializerMethodField()
    colors_count = serializers.IntegerField(source='colors.count', read_only=True)
    colors = ProductColorSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    max_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category_name',
            'quality', 'brand', 'article',
            'base_price', 'price_type',
            'badge', 'status',
            'stock', 'in_stock',
            'main_image', 'colors_count', 'colors',
            'min_price', 'max_price',
        ]

    def get_main_image(self, obj):
        img = obj.images.filter(is_main=True).first() or obj.images.first()
        if img and img.image:
            request = self.context.get('request')
            return request.build_absolute_uri(img.image.url) if request else img.image.url
        return None

    def get_min_price(self, obj):
        colors = obj.colors.filter(is_available=True)
        if colors.exists():
            return round(min(c.get_effective_price() for c in colors), 2)
        return round(float(obj.base_price), 2)

    def get_max_price(self, obj):
        colors = obj.colors.filter(is_available=True)
        if colors.exists():
            return round(max(c.get_effective_price() for c in colors), 2)
        return round(float(obj.base_price), 2)


class ProductDetailSerializer(serializers.ModelSerializer):
    in_stock = serializers.BooleanField(read_only=True)
    category = CategorySerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    colors = ProductColorSerializer(many=True, read_only=True)
    quality_display = serializers.CharField(source='get_quality_display', read_only=True)
    car_models = CarModelSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    price_type_display = serializers.CharField(source='get_price_type_display', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug',
            'category', 'category_name',
            'description',
            'quality', 'quality_display',
            'car_models',
            'base_price', 'price_type', 'price_type_display',
            'badge', 'status', 'status_display',
            'brand', 'article', 'warranty',
            'usage', 'delivery_info',
            'stock', 'in_stock', 'is_active', 'images', 'colors',
            'created_at', 'updated_at',
        ]


class PriceCalculateSerializer(serializers.Serializer):
    width_mm = serializers.IntegerField(min_value=100, max_value=10000)
    height_mm = serializers.IntegerField(min_value=100, max_value=10000)
    color_id = serializers.IntegerField(required=False, allow_null=True)

    def validate(self, attrs):
        product = self.context.get('product')
        color_id = attrs.get('color_id')
        if color_id:
            try:
                color = product.colors.get(id=color_id, is_available=True)
                attrs['color'] = color
            except ProductColor.DoesNotExist:
                raise serializers.ValidationError({'color_id': 'Rang topilmadi yoki mavjud emas'})
        else:
            attrs['color'] = None
        return attrs
