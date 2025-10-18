import csv
from io import TextIOWrapper
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file or not file.name.endswith('.csv'):
            return JsonResponse({'error': 'Please upload a valid CSV file.'}, status=400)

        data = TextIOWrapper(file.file, encoding='utf-8')
        reader = csv.DictReader(data)
        stored, failed = 0, []

        for row in reader:
            try:
                sku = row['sku']
                name = row['name']
                brand = row['brand']
                mrp = float(row['mrp'])
                price = float(row['price'])
                quantity = int(row['quantity'])
                color = row.get('color', '')
                size = row.get('size', '')

                if price > mrp or quantity < 0:
                    failed.append(sku)
                    continue

                Product.objects.update_or_create(
                    sku=sku,
                    defaults={
                        'name': name,
                        'brand': brand,
                        'color': color,
                        'size': size,
                        'mrp': mrp,
                        'price': price,
                        'quantity': quantity,
                    },
                )
                stored += 1
            except Exception:
                failed.append(row.get('sku', 'unknown'))

        return JsonResponse({'stored': stored, 'failed': failed})

    return JsonResponse({'error': 'Use POST method'}, status=405)


def list_products(request):
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    products = Product.objects.all().order_by('id')
    paginator = Paginator(products, limit)
    data = list(paginator.get_page(page).object_list.values())
    return JsonResponse(data, safe=False)


def search_products(request):
    brand = request.GET.get('brand')
    color = request.GET.get('color')
    min_price = request.GET.get('minPrice')
    max_price = request.GET.get('maxPrice')

    filters = Q()
    if brand:
        filters &= Q(brand__icontains=brand)
    if color:
        filters &= Q(color__icontains=color)
    if min_price:
        filters &= Q(price__gte=min_price)
    if max_price:
        filters &= Q(price__lte=max_price)

    products = Product.objects.filter(filters).order_by('id')
    data = list(products.values())
    return JsonResponse(data, safe=False)
