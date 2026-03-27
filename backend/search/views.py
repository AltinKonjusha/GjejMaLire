from rest_framework.decorators import api_view
from rest_framework.response import Response
from scrapers.gjirafa50 import scrape_gjirafa50
from scrapers.foleja import scrape_foleja
from scrapers.neptun import scrape_neptun
from products.models import SearchLog
from concurrent.futures import ThreadPoolExecutor, as_completed

@api_view(['GET'])
def search_products(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return Response({'error': 'Please provide a search query'}, status=400)

    if len(query) < 2:
        return Response({'error': 'Query too short'}, status=400)

    results = []
    errors = []

    scrapers = {
        'gjirafa50': scrape_gjirafa50,
        'foleja': scrape_foleja,
        'neptun': scrape_neptun,
    }

    # Run all scrapers at the same time
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(fn, query): name
            for name, fn in scrapers.items()
        }

        for future in as_completed(futures):
            name = futures[future]
            try:
                data = future.result(timeout=20)
                results.extend(data)
            except Exception as e:
                errors.append(f"{name} failed: {str(e)}")

    results.sort(key=lambda x: x['price'] or 999999)

    SearchLog.objects.create(
        query=query,
        results_count=len(results)
    )

    return Response({
        'query': query,
        'count': len(results),
        'results': results,
        'errors': errors,
    })