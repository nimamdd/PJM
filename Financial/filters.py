from rest_framework import filters


class ListOfFinancialPerformanceFilterBackend(filters.BaseFilterBackend):
    """
    http://127.0.0.1:8000/financial/list-create/?kind=subtask&status=canceled&price_min=1&price_max=5000000
    """

    def filter_queryset(self, request, queryset, view):
        # Extract parameters from the request
        status = request.query_params.get('status')
        kind = request.query_params.get('kind')
        price_min = request.query_params.get('price_min')
        price_max = request.query_params.get('price_max')

        # Filter by status if provided
        if status:
            queryset = queryset.filter(status=status)

        # Filter by kind if provided
        if kind:
            queryset = queryset.filter(content_type__model=kind.lower())

        # Filter by minimum price if provided
        if price_min is not None:
            try:
                price_min = float(price_min)
                queryset = queryset.filter(price__gte=price_min)
            except ValueError:
                # Handle invalid input, if necessary
                pass

        # Filter by maximum price if provided
        if price_max is not None:
            try:
                price_max = float(price_max)
                queryset = queryset.filter(price__lte=price_max)
            except ValueError:
                # Handle invalid input, if necessary
                pass

        return queryset
