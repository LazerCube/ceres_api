from rest_framework import permissions, viewsets

from authentication.models import Account
from authentication.serializers import AccountSerializer

from authentication.permissions import IsAccountOwner


class AccountViewSet(viewsets.ModelViewSet):
    """
    More information coming soon
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAccountOwner)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)
