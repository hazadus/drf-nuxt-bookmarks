from rest_framework import authentication, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CustomUserSerializer
from .models import CustomUser


class UserDetailView(APIView):
    """
    Return logged in user's detailed info.
    NB: Djoser's "/users/me" somehow doesn't work for me with tokens, so we got to use our own
    view for user details.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request: Request) -> Response:
        """
        Return logged in user's detailed info.
        """
        user = CustomUser.objects.filter(pk=request.user.pk).first()
        serializer = CustomUserSerializer(user, many=False)
        return Response(serializer.data)
