from .models import Category

def base_get_categories(request):
    categories = {}
    for category in Category.objects.filter(parent=None):
        subcategories = category.get_all_children()
        categories[category] = subcategories

    return {'base_categories':categories}
 