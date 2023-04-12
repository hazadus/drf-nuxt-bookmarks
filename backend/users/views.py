from rest_framework import authentication, permissions
from rest_framework.generics import UpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CustomUserSerializer
from .models import CustomUser


class LoggedInUserDetailView(APIView):
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


class UserUpdateView(UpdateAPIView):
    """
    Partially update user info. Return updated data.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def put(self, request, *args, **kwargs):
        """
        PATCH method must be used to partially update user info.
        Return updated data.
        """
        return self.partial_update(request, *args, **kwargs)
