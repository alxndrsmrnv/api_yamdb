from rest_framework.views import APIView
from .serializers import ProfileRegisterSerializer, TokenSerializer
from reviews.models import Profile
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import ProfileSerializer




class CreateProfileView(generics.CreateAPIView):
    serializer_class = ProfileRegisterSerializer


class TokenView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        refresh = RefreshToken.for_user(request.user)
        token = str(refresh.access_token)
        if serializer.is_valid():
            print(token)
            return Response({'token': token})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer = ProfileSerializer
    permission_classes = (permissions.IsAdminUser,
                          permissions.IsAuthenticatedOrReadOnly)



