from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, PostViewSet, CommentViewSet, FavoriteViewSet, DashboardViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

app_name = 'blog'

urlpatterns = [
    path('api/', include(router.urls)),
] 