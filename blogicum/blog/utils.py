from django.core.paginator import Paginator


OBJECTS_NUMBER = 10


def paginator_func(request, objects):
    paginator = Paginator(objects, OBJECTS_NUMBER)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
