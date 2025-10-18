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

        required_fields = ['sku', 'name', 'brand', 'mrp', 'price']

        for i, row in enumerate(reader, start=1):
            try:
                # Check for missing required fields
                if not all(field in row and row[field].strip() for field in required_fields):
                    failed.append({'row': i, 'reason': 'Missing required fields'})
                    continue

                sku = row['sku'].strip()
                name = row['name'].strip()
                brand = row['brand'].strip()
                color = row.get('color', '').strip()
                size = row.get('size', '').strip() 
                mrp = float(row['mrp'])
                price = float(row['price'])
                quantity = int(row.get('quantity', 0)) if row.get('quantity') else 0


                # Validation rules
                if price > mrp:
                    failed.append({'row': i, 'sku': sku, 'reason': 'Price exceeds MRP'})
                    continue
                if quantity < 0:
                    failed.append({'row': i, 'sku': sku, 'reason': 'Quantity cannot be negative'})
                    continue

                # If valid, create or update
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

            except ValueError as ve:
                failed.append({'row': i, 'reason': f'Invalid data type - {ve}'})
            except Exception as e:
                failed.append({'row': i, 'reason': f'Unexpected error - {e}'})

        return JsonResponse({
            'stored': stored,
            'failed_count': len(failed),
            'failed_rows': failed
        })

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
