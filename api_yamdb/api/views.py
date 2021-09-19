from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, generics, permissions, status, viewsets)
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken


from reviews.models import Category, Genre, Profile, Title
from .filters import TitlesFilter
from .permissions import (AdminOrReadOnly, IsOwnerModeratorAdminOrReadOnly,
                          IsRoleAdmin)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ProfileRegisterSerializer,
                          ProfileSerializer, ProfileSerializerAdmin,
                          ReviewSerializer, TitleSerializer,
                          TitleSerializerCreate, TokenRestoreSerializer,
                          TokenSerializer)
from .utils import mail


class CreateProfileView(generics.CreateAPIView):
    serializer_class = ProfileRegisterSerializer
    queryset = Profile.objects.all()
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ProfileRegisterSerializer(data=request.data)
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
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        profile = get_object_or_404(Profile,
                                    username=request.data.get('username'))
        confirmation_code = request.data.get('confirmation_code')
        if profile.confirmation_code != confirmation_code:
            return Response('Неверный код подтверждения',
                            status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(profile)
        token = str(refresh.access_token)
        return Response({'token': token}, status=status.HTTP_201_CREATED)


class RestoreConfCodeView(generics.CreateAPIView):
    serializer_class = TokenRestoreSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenRestoreSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        profile = get_object_or_404(Profile,
                                    username=request.data.get('username'))
        if not profile.email:
            profile.email = serializer.validated_data.get('email')
        profile.confirmation_code = mail(profile)
        profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializerAdmin
    permission_classes = (IsRoleAdmin,)
    filter_backends = (filters.SearchFilter,)
    filterset_fields = ('=username')

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        print(request)
        if request.method == 'GET':
            profile = get_object_or_404(Profile, username=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        profile = get_object_or_404(Profile, username=request.user)
        serializer = ProfileSerializer(profile,
                                       data=request.data,
                                       partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, **kwargs):
        profile = get_object_or_404(Profile, username=self.kwargs.get('pk'))
        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, username=self.kwargs.get('pk'))
        serializer = ProfileSerializerAdmin(profile,
                                            data=request.data,
                                            partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, username=self.kwargs.get('pk'))
        self.perform_destroy(profile)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        return title.reviews.all()

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
