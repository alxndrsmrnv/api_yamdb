from rest_framework.views import APIView
from .serializers import ProfileRegisterSerializer, TokenSerializer
from reviews.models import Profile
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .serializers import (ProfileSerializer, CommentSerializer, ReviewSerializer,
                          CategoriesSerializer, GenresSerializer, TitlesSerializer)
from api.permissions import IsOwnerModeratorAdminOrReadOnly
from reviews.models import Categories, Genres, Titles




class CreateProfileView(generics.CreateAPIView):
    serializer_class = ProfileRegisterSerializer
    permission_classes = permissions.AllowAny


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
