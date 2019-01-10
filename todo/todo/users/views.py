from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_404_NOT_FOUND

from todo.users.models import User
from todo.users.filters import UserFilter, UserBornAfterFilterBackend
from todo.users.serializers import UserSerializer
from todo.users.serializers import UserWithTasksSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
        UserBornAfterFilterBackend,
        DjangoFilterBackend,
    ]
    filterset_class = UserFilter
    search_fields = ['email', 'full_name']
    ordering_fields = ['email', 'full_name']
    ordering = ['email']


class UserWithTasksView(APIView):

    def get(self, request, pk, *args, **kw):
        try:
            user = User.objects.get(id=pk)
            return Response(UserWithTasksSerializer(instance=user, context={'request': request}).data)
        except:
            return Response(status=HTTP_404_NOT_FOUND)
