from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import CreateProfileView, ProfileViewSet, TokenView

router = DefaultRouter()
router.register(r'users', ProfileViewSet, basename='users')

urlpatterns = [
    path('auth/token/', TokenView.as_view(), name='token_obtain_pair'),
    path('auth/signup/', CreateProfileView.as_view()),
    path('', include(router.urls))
]