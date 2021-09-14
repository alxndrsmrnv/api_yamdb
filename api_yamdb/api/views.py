from functools import partial
from django.utils.functional import empty
from .permissions import IsRoleAdmin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import views, filters
from rest_framework.views import APIView
from .serializers import ProfileRegisterSerializer, TokenSerializer
from reviews.models import Profile
from rest_framework import serializers, viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication, JWTTokenUserAuthentication
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .utils import mail, get_user

from .serializers import (ProfileSerializer, CommentSerializer, ReviewSerializer,
                          CategoriesSerializer, GenresSerializer, TitlesSerializer, TokenRestoreSerializer, ProfileSerializerAdmin)
from api.permissions import IsOwnerModeratorAdminOrReadOnly
from reviews.models import Categories, Genres, Titles


class CreateProfileView(generics.CreateAPIView):
    serializer_class = ProfileRegisterSerializer
    queryset = Profile.objects.all()
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ProfileRegisterSerializer(data=request.data)
        if request.data.get('username') == 'me':
            return Response('Нельзя брать имя me',
                            status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            profile = get_object_or_404(Profile,
                                        username=request.data.get('username'))
            profile.confirmation_code = mail(profile)
            profile.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(generics.CreateAPIView):
    serializer_class = TokenSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid() is not True:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        profile = Profile.objects.filter(username=request.data.get('username'))
        if len(profile) == 0:
            return Response('Пользователя с таким username не существует',
                            status=status.HTTP_404_NOT_FOUND)
        confirmation_code = request.data.get('confirmation_code')
        if profile[0].confirmation_code != confirmation_code:
            return Response('Неверный код подтверждения',
                            status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(profile[0])
        token = str(refresh.access_token)
        return Response({'token': token}, status=status.HTTP_201_CREATED)

class RestoreConfCodeView(generics.CreateAPIView):
    serializer_class = TokenRestoreSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = TokenRestoreSerializer(data=request.data)
        if serializer.is_valid() is not True:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        profile = get_object_or_404(Profile,
                                    username=request.data.get('username'))
        if profile.email is not True:
            profile.email = serializer.validated_data.get('email')
        profile.confirmation_code = mail(profile)
        profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializerAdmin
    permission_classes = (IsRoleAdmin,)
    filter_backends = (filters.SearchFilter,)
    filterset_fields =  ('=username')
    def retrieve(self, request, **kwargs):
        if self.kwargs.get('pk') == 'me':
            profile = get_object_or_404(Profile, username=get_user(request))
            serializer = self.get_serializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        profile = get_object_or_404(Profile, username=self.kwargs.get('pk'))
        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def partial_update(self, request, *args, **kwargs):
        if self.kwargs.get('pk') == 'me':
            profile = get_object_or_404(Profile, username=get_user(request))
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        profile = get_object_or_404(Profile, username=self.kwargs.get('pk'))
        serializer = ProfileSerializerAdmin(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
        if self.kwargs.get('pk') == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        profile = get_object_or_404(Profile, username=self.kwargs.get('pk'))
        self.perform_destroy(profile)
        return Response(status=status.HTTP_204_NO_CONTENT)



class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsOwnerModeratorAdminOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsOwnerModeratorAdminOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
