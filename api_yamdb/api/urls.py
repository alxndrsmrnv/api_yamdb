from rest_framework.routers import DefaultRouter
from django.urls import path, include
from api.views import CommentViewSet, ReviewViewSet
from .views import (CreateProfileView, ProfileViewSet, TokenView,
                    CategoriesViewSet, GenresViewSet, TitlesViewSet, RestoreConfCodeView)

router_v1 = DefaultRouter()
router_v1.register(r'users', ProfileViewSet)
router_v1.register(r'users/(?P<username>\d+)', ProfileViewSet)
router_v1.register(r'categories', CategoriesViewSet)
router_v1.register(r'genres', GenresViewSet)
router_v1.register(r'titles', TitlesViewSet)
router_v1.register(r'users', ProfileViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)


urlpatterns = [
    path('v1/auth/restore/', RestoreConfCodeView.as_view()),
    path('v1/auth/signup/', CreateProfileView.as_view()),
    path('v1/auth/token/', TokenView.as_view(), name='token_obtain_pair'),
    path('v1/', include(router_v1.urls))
]
