from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
class ProductPagination(PageNumberPagination):
    default_page_size = 5

    def get_page_size(self, request):
        page_size = request.query_params.get('page_size')
        
        # Validate that page_size is a positive integer
        if page_size is not None:
            try:
                page_size = int(page_size)
                if page_size <= 0:
                    return self.default_page_size
            except ValueError:
                return self.default_page_size
            
        return page_size or self.default_page_size
