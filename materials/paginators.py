from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MaterialsPaginator(PageNumberPagination):
    # Размер страницы по умолчанию
    page_size = 10

    # Параметр запроса, который позволяет клиентам изменить размер страницы (например, ?page_size=20)
    page_size_query_param = 'page_size'

    # Максимальный размер страницы, чтобы предотвратить запросы с чрезмерно большим количеством элементов
    max_page_size = 100

    # Параметр запроса для указания номера страницы (например, ?page=2)
    page_query_param = 'page'

    # Переопределение метода для получения ответа с пагинацией
    def get_paginated_response(self, data):
        # Формирование ответа с метаданными пагинации и данными текущей страницы
        return Response({
            'links': {
                'next': self.get_next_link(),  # Ссылка на следующую страницу
                'previous': self.get_previous_link()  # Ссылка на предыдущую страницу
            },
            'total_results': self.page.paginator.count,  # Общее количество элементов
            'total_pages': self.page.paginator.num_pages,  # Общее количество страниц
            'current_page': self.page.number,  # Текущий номер страницы
            'results_per_page': self.get_page_size(self.request),  # Количество элементов на странице
            'results': data  # Сами данные текущей страницы
        })
