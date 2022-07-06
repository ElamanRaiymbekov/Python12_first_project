from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters

from product.models import Product, ProductReview
from product.permissions import IsAuthorOrIsAdmin
from product.serializers import ProductSerializer, ProductDetailsSerializer, CreateProductSerializer, ReviewSerializer


def test_view(request):
    return HttpResponse('Hello world!')


class ProductFilter(filters.FilterSet):
    price_from = filters.NumberFilter('price', 'gte')
    price_to = filters.NumberFilter('price', 'lte')

    class Meta:
        model = Product
        fields = ('price_from', 'price_to')


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    filter_backends = [filters.DjangoFilterBackend, rest_filters.SearchFilter,
                       rest_filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'price']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        elif self.action == 'retrieve':
            return ProductDetailsSerializer
        return CreateProductSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return []


class ReviewViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthorOrIsAdmin()]
        return []

    @action(['GET'], detail=True)
    def reviews(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=200)




#TODO: Тесты переписать на PyTest
#TODO: Ограничение на кол-во запросов
#TODO: Документация
#TODO: README
#TODO: Фабрика теста
#TODO: FactoryBoy



# CRUD - CREATE, RETRIEVE, UPDATE, DELETE
#       POST    GET    PUT, PUTCH  DELETE


# REST - архитектурный подход
#         1) Модель: клиент - сервер (серверная часть отделяется от клиентской)
#         2) Отсутствие состояния
#         3) Кеширование
#         4) Единообразие интерфейса
#                 1) Определение ресурсов
#                         URI('api/v1/products/1/')
#                 2) Управление ресурсом через представление
#                 3) Самодостаточные сообщения
#         5) Слои
#         6) Код по требованию

# "GET"
# list - много значений
# retrieve - одно значение

# # "POST"
# create - создание

# # "PUT"
# редактирование

# # "PATCH"
# UPDATE - обновление

# # "DELETE"
# destroy - удаление




# Product.objects.all() - выдает весь список записей объектов модели --------------->SELECT * FROM products;

# Product.objects.create() - создает новые объекты --------------> INSERT INTO product.....;

# Product.objects.update() - обновляет выбранные объекты ------> UPDATE product.....;

# Product.objects.delete() - удаляет объекты ----------> DELETE FROM product;

# Product.objects.filter(условие) - фильтрация --------> SELECT * FROM product WHERE условие;



# Операции сравнения:
# '='
# Product.objects.filter(price=1000) ------> SELECT * FROM product WHERE price =1000;
#
# '>'
# Product.objects.filter(price__gt=1000) -------> SELECT * FROM product WHERE price > 1000;
#
# '<'
# Product.objects.filter(price__lt=1000) -------> SELECT * FROM product WHERE price < 1000;
#
# '>='
# Product.objects.filter(price__gti=1000) -------> SELECT * FROM product WHERE price >= 1000;
#
# '<='
# Product.objects.filter(price__lti=1000) -------> SELECT * FROM product WHERE price <= 1000;



# BETWEEN
# Product.objects.filter(price__range=[50000, 80000])   ------->SELECT * FROM product WHERE price BETWEEN 50000 AND 80000;

# IN
# Product.objects.filter(price__in=[50000, 80000])   ------->SELECT * FROM product WHERE price IN (50000, 80000);

#LIKE
#ILIKE
# 'work%' - начинается
# Product.objects.filter(title__startswith='Apple') ------->SELECT * FROM product WHERE title LIKE 'Apple%'
# Product.objects.filter(title__isstartswith='Apple') ----->SELECT * FROM product WHERE title ILIKE 'Apple%'


# '%work' - заканчивается
# Product.objects.filter(title__endswith='GB') ------->SELECT * FROM product WHERE title LIKE '%CG'
# Product.objects.filter(title__iendwith='GB') ------->SELECT * FROM product WHERE title ILIKE '%GB'


# '%work%' - содержит строки
# Product.objects.filter(title__contains='Samsung') ------->SELECT * FROM product WHERE title LIKE '%Samsung%'
# Product.objects.filter(title__icontains='Samsung') ------->SELECT * FROM product WHERE title ILIKE '%Samsung%'


#'work' - есть слово(равно)
# Product.objects.filter(title__exact='Apple IPhone 12') ------->SELECT * FROM product WHERE title LIKE 'Apple IPhone 12'
# Product.objects.filter(title__iexact='Apple IPhone 12') ------->SELECT * FROM product WHERE title ILIKE 'Apple IPhone 12'


# ODRDER BY
# Product.objects.order_by('price') -------> SELECT * FROM product ORDER BY price ASC; (по возрастю)
# Product.objects.order_by('-price') -------> SELECT * FROM product ORDER BY price DESC; (по уменьшю)
# Product.objects.order_by('-price', 'title') -------> SELECT * FROM product ORDER BY price DESC, title ASC;


#LIMIT
# Product.objects.all()[:2] --------> SELECT * FROM product LIMIT 2;
# Product.objects.all()[3:6] --------> SELECT * FROM product LIMIT 3 OFFSET 3;
# Product.objects.first() --------> SELECT * FROM product LIMIT 1;


#get() - возращает один объект
# Product.objects.get(id=1) --------> SELECT * FROM product WHERE id=1;
# Если будут ошибки: DoesNotExcist - возникает, когда не найдет ни один объект
#                    MultiplyObjectsReturned - возникает, когда найдено больше одного объекта

#count() - возвращает кол-во результатов
# Product.objects.filter(условие).count() ----------> SELECT COUNT(*) FROM product;


# exclude()
# Product.objects.exclude(price__gt=10000) ------> SELECT * FROM product WHERE NOT price > 10000;


# QuerySet - список объектов модели

















