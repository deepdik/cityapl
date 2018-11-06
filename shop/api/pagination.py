from rest_framework.pagination import PageNumberPagination

class ShortPAginator(PageNumberPagination):
	page_size = 5