from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 5  # сколько элементов по умолчанию
    page_size_query_param = 'page_size'  # параметр в query string, чтобы переопределить
    max_page_size = 50  # максимальное кол-во, чтобы не убить сервер
