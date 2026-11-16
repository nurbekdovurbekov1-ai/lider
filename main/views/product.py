from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from ..models import Category, CarModel, Product
from ..serializers.product import (
    CategorySerializer, CarModelSerializer, ProductListSerializer,
    ProductDetailSerializer, ProductColorSerializer,
    PriceCalculateSerializer,
)
from ..filters.filters import ProductFilter


@extend_schema(tags=["🏷️ Kategoriyalar"])
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Mahsulot kategoriyalari.

    Kategoriyalar: Dvigatel, Tormoz, Filtrlar, Osma (podveska), Elektr, Yoritish, Moylar va suyuqliklar, Kuzov, Salon.
    Katalogni filterlash uchun kategoriya slugidan foydalaning.
    """
    queryset = Category.objects.filter(is_active=True).order_by("order")
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None
    lookup_field = "slug"

    @extend_schema(
        summary="Kategoriyalar ro'yxati",
        description="Barcha faol kategoriyalarni tartib raqami bo'yicha ko'rsatadi.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Kategoriya detali",
        description="Bitta kategoriyaning to'liq ma'lumotlarini slug bo'yicha ko'rsatadi.",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@extend_schema(tags=["🚗 Mashina turlari"])
class CarModelViewSet(viewsets.ReadOnlyModelViewSet):
    """Mashina turlari (Nexia, Lacetti, Cobalt ...). Katalogni mashina bo'yicha filterlash uchun."""
    queryset = CarModel.objects.filter(is_active=True).order_by("order", "name")
    serializer_class = CarModelSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    lookup_field = "slug"


@extend_schema(tags=["📦 Mahsulotlar"])
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Mahsulot katalogi.

    Barcha mahsulotlarni ko'rish, filterlash, qidirish va narx hisoblash.

    **Filtr parametrlari:**
    - category — Kategoriya slug (masalan: tormoz)
    - car — Mashina turi slugi (masalan: nexia, lacetti, cobalt)
    - quality — Sifat turi: original, analog, premium
    - brand — Brend nomi (masalan: Bosch)
    - status — Holat: active, sale, out_of_stock
    - adge — Yorliq: new, hit, sale
    - min_price / max_price — Narx oralig'i
    - search — Nom yoki tavsif bo'yicha qidiruv
    - ordering — Saralash: base_price, -base_price, created_at, -created_at
    """
    queryset = (
        Product.objects.filter(is_active=True)
        .select_related("category")
        .prefetch_related("images", "colors", "car_models")
    )
    permission_classes = [AllowAny]
    filterset_class = ProductFilter
    search_fields = ["name", "description", "brand", "article"]
    ordering_fields = ["base_price", "created_at", "name"]
    ordering = ["-created_at"]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductListSerializer

    @extend_schema(
        summary="Mahsulotlar ro'yxati",
        description="""
Katalogdagi barcha faol mahsulotlarni ko'rsatadi.

Filterlash, qidiruv va saralash qo'llab-quvvatlanadi.
Har sahifada 20 ta mahsulot keladi (pagination).

**Misol so'rov:** /api/products/?category=tormoz&car=nexia&ordering=base_price
        """,
        parameters=[
            OpenApiParameter("category", OpenApiTypes.STR, description="Kategoriya slug: tormoz, filtrlar, ..."),
            OpenApiParameter("car", OpenApiTypes.STR, description="Mashina turi slugi: nexia, lacetti, cobalt, ..."),
            OpenApiParameter("quality", OpenApiTypes.STR, description="Sifat turi: original, analog, premium"),
            OpenApiParameter("brand", OpenApiTypes.STR, description="Brend nomi"),
            OpenApiParameter("status", OpenApiTypes.STR, description="Holat: active, sale, out_of_stock"),
            OpenApiParameter("min_price", OpenApiTypes.NUMBER, description="Minimal narx (UZS)"),
            OpenApiParameter("max_price", OpenApiTypes.NUMBER, description="Maksimal narx (UZS)"),
            OpenApiParameter("search", OpenApiTypes.STR, description="Nom yoki tavsif bo'yicha qidiruv"),
            OpenApiParameter("ordering", OpenApiTypes.STR, description="Saralash: base_price, -base_price, created_at"),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Mahsulot detali",
        description="""
Mahsulotning to'liq ma'lumotlarini ko'rsatadi:
- Asosiy ma'lumotlar (nom, kategoriya, tavsif)
- Brend, artikul, kafolat va nima uchun ishlatilishi
- Mos mashina turlari
- Barcha rasmlar (galereya)
- Rang variantlari va ularning narx farqlari
- Yetkazib berish ma'lumotlari
        """,
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Rang variantlari",
        description="""
Mahsulotning mavjud rang variantlarini ko'rsatadi.

Har bir rangda:
- 
ame — Rang nomi (Oq, Jigarrang, Antrasit, ...)
- hex_code — Rang kodi (#FFFFFF, ...)
- price_modifier — Asosiy narxga qo'shiladigan yoki ayiriladigan narx farqi (UZS)
  - 0 = asosiy rang (narx o'zgarmaydi)
  - +500000 = qimmatroq rang
  - -100000 = arzonroq rang
        """,
    )
    @action(detail=True, methods=["get"])
    def colors(self, request, slug=None):
        """Mahsulot rang variantlari"""
        product = self.get_object()
        colors = product.colors.filter(is_available=True)
        serializer = ProductColorSerializer(colors, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Narx hisoblash",
        description="""
Tanlangan o'lcham va rang asosida narxni hisoblash.

**Narx formulasi:**
`
narx = (base_price + color.price_modifier) × (kenglik_m × balandlik_m)
`

**So'rov:**
- width_mm — Kenglik millimetrda (100–10000)
- height_mm — Balandlik millimetrda (100–10000)
- color_id — Rang ID (ixtiyoriy, ko'rsatilmasa asosiy narx hisoblanadi)

**Javob:**
- calculated_price — Hisoblangan narx (UZS)
- sqm — Kv.m (kvadrat metr)
- price_type — Narx turi (per_sqm = kv.m uchun, fixed = qat'iy narx)
        """,
        request=PriceCalculateSerializer,
        responses={
            200: OpenApiResponse(description="Hisoblangan narx ma'lumotlari"),
            400: OpenApiResponse(description="Noto'g'ri o'lcham yoki rang"),
        },
    )
    @action(detail=True, methods=["post"])
    def calculate_price(self, request, slug=None):
        """Narxni hisoblash: o'lcham va rang asosida"""
        product = self.get_object()
        serializer = PriceCalculateSerializer(
            data=request.data, context={"product": product, "request": request}
        )
        serializer.is_valid(raise_exception=True)

        width_mm = serializer.validated_data["width_mm"]
        height_mm = serializer.validated_data["height_mm"]
        color = serializer.validated_data.get("color")

        calculated = product.calculate_price(width_mm, height_mm, color)
        sqm = (width_mm / 1000) * (height_mm / 1000)

        color_price = color.get_effective_price() if color else float(product.base_price)
        calc_rounded = round(calculated, 2)

        return Response({
            "product": product.name,
            "width_mm": width_mm,
            "height_mm": height_mm,
            "sqm": round(sqm, 4),
            "color": color.name if color else None,
            "color_id": color.id if color else None,
            "base_price": float(product.base_price),
            "color_price": color_price,
            "price_modifier": float(color.price_modifier) if color else 0,
            "price_type": product.price_type,
            "calculated_price": calc_rounded,
            "total_price": calc_rounded,
            "currency": "UZS",
        })
