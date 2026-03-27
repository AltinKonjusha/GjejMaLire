from rest_framework.decorators import api_view
from rest_framework.response import Response
from scrapers.gjirafa50 import scrape_gjirafa50
from scrapers.foleja import scrape_foleja
from scrapers.neptun import scrape_neptun
from products.models import SearchLog

@api_view(['GET'])
def search_products(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return Response({'error': 'Please provide a search query'}, status=400)

    if len(query) < 2:
        return Response({'error': 'Query too short'}, status=400)

    results = []
    errors = []

    try:
        gjirafa_results = scrape_gjirafa50(query)
        results.extend(gjirafa_results)
    except Exception as e:
        errors.append(f"Gjirafa50 failed: {str(e)}")

    try:
        foleja_results = scrape_foleja(query)
        results.extend(foleja_results)
    except Exception as e:
        errors.append(f"Foleja failed: {str(e)}")

    try:
        neptun_results = scrape_neptun(query)
        results.extend(neptun_results)
    except Exception as e:
        errors.append(f"Neptun failed: {str(e)}")

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