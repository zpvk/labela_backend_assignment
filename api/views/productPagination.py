from rest_framework.pagination import PageNumberPagination

class ProductPagination(PageNumberPagination):
    default_page_size = 5

    def get_page_size(self, request):
        page_size = request.query_params.get('page_size')
        if page_size:
            return page_size
        return self.default_page_size