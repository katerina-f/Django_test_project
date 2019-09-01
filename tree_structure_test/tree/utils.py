from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Category
from .serializers import CategorySerializer


class CategoryMixin:
    model = None

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryMixin, self).dispatch(request, *args, **kwargs)

    def _get_serializable_node(self, node):
        s_node = {"id": node.id, "name": node.name}
        return s_node

    def get(self, request, id):
        obj = get_object_or_404(Category, id__iexact=id)
        children = [self._get_serializable_node(node) for node in obj.get_children()]
        siblings = [self._get_serializable_node(node) for node in obj.get_siblings()]
        parents = [self._get_serializable_node(node) for node in obj.get_ancestors()]
        data = {"id": obj.id, "name": obj.name,
                "parents": parents, "children": children, "siblings": siblings}
        return JsonResponse(data, json_dumps_params={"indent": 4}, status=200)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, json_dumps_params={"indent": 4}, status=201)
        return JsonResponse(serializer.errors, json_dumps_params={"indent": 4}, status=400)
