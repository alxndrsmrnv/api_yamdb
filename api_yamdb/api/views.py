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
<<<<<<< HEAD
from .utils import mail, get_user

from .serializers import (ProfileSerializer, CommentSerializer, ReviewSerializer,
                          CategoriesSerializer, GenresSerializer, TitlesSerializer, TokenRestoreSerializer, ProfileSerializerAdmin)
from api.permissions import IsOwnerModeratorAdminOrReadOnly
from reviews.models import Categories, Genres, Title
=======
from rest_framework.mixins import (CreateModelMixin,
                                   DestroyModelMixin,
                                   ListModelMixin)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


from .serializers import (ProfileSerializer,
                          CommentSerializer,
                          ReviewSerializer,
                          CategorySerializer,
                          GenreSerializer,
                          TitleSerializer, TitleSerializerCreate)
from .filters import TitlesFilter
from api.permissions import IsOwnerOrReadOnly, AdminOrReadOnly
from reviews.models import Category, Genre, Title
>>>>>>> cat-gen-tit.v2


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
<<<<<<< HEAD
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

=======
    serializer_class = ProfileSerializer
    # permission_classes = (permissions.IsAdminUser,
    #                       permissions.IsAuthenticatedOrReadOnly)
>>>>>>> cat-gen-tit.v2


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsOwnerModeratorAdminOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsOwnerModeratorAdminOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
<<<<<<< HEAD
        return title.reviews.all()
=======
        return title.reviews
>>>>>>> cat-gen-tit.v2

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CreateDestroyListViewSet(CreateModelMixin,
                               DestroyModelMixin,
                               ListModelMixin,
                               viewsets.GenericViewSet):
    pass


class GenresViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class CategoriesViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializer
        return TitleSerializerCreate
