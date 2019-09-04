from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Category


class CategoryMixin:
    model = None

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryMixin, self).dispatch(request, *args, **kwargs)

    def _get_serializable_node(self, node):
        s_node = {"id": node.id, "name": node.name}
        return s_node

    def _load_catalog(self, data, parent):
        category, created = Category.objects.get_or_create(name=data.get('name'))
        try:
            category.parent = category
        except ValueError:
            error = {'error': 'invalid data, must be "Category" instance'}
            return JsonResponse(error, json_dumps_params={"indent": 4}, status=201, safe=False)

        parent = category
        children = data.get('children')
        if children:
            [self._load_catalog(child, parent) for child in children]
        category.save()

    def get_ancestors(self, obj):
        ancestors = []
        ancestor = obj
        while ancestor:
            parent = ancestor.parent
            ancestors.insert(0, parent)
            ancestor = parent
        return ancestors

    def get_children(self, obj):
        children = self.model.objects.filter(parent=obj)
        return children

    def get_siblings(self, obj):
        siblings = self.model.objects.filter(parent=obj.parent).exclude(id=obj.id)
        return siblings

    def get(self, request, id):
        obj = get_object_or_404(self.model, id__iexact=id)
        parents = [self._get_serializable_node(node) for node in self.get_ancestors(obj) if node]
        children = [self._get_serializable_node(node) for node in self.get_children(obj)]
        siblings = [self._get_serializable_node(node) for node in self.get_siblings(obj)]
        data = {"id": obj.id, "name": obj.name,
                "parents": parents, "children": children, "siblings": siblings}
        return JsonResponse(data, json_dumps_params={"indent": 4}, status=200)

    def post(self, request):
        data = JSONParser().parse(request)
        self._load_catalog(data, parent=None)
        return JsonResponse(data, json_dumps_params={"indent": 4}, status=201, safe=False)
