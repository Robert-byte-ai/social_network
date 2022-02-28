from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .views import UserViewSet, PostViewSet, FollowViewSet

router_1 = DefaultRouter()

router_1.register(
    r'user',
    UserViewSet,
    basename='create'
)
router_1.register(
    'posts',
    PostViewSet,
    basename='posts'
)
router_1.register(
    'follow',
    FollowViewSet,
    basename='follow'
)

urlpatterns = [
    path('', include(router_1.urls)),
    path('create/', views.obtain_auth_token),
]
