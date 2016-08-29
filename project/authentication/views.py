from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from authentication.models import Account
from authentication.serializers import AccountSerializer
from authentication.permissions import IsAuthenticatedOrTokenHasReadWriteScope, IsOwnerOrReadOnly

from rest_framework.permissions import DjangoModelPermissions

class AccountViewSet(viewsets.ModelViewSet):
    """
    More information coming soon
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    permission_classes = [IsAuthenticatedOrTokenHasReadWriteScope, IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = ()
        return super(AccountViewSet, self).get_permissions()

    def update(self, request, *args, **kwargs):
        instance = request.user

        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

class CurrentUserView(APIView):
    def get(self, request):
        serializer = AccountSerializer(request.user, context={'request': request})
        return Response(serializer.data)
