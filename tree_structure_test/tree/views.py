from django.views.generic import View
from .models import Category
from .utils import CategoryMixin


class CategoriesData(CategoryMixin, View):
    model = Category
