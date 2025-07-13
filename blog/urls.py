from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, PostViewSet, CommentViewSet, FavoriteViewSet, DashboardViewSet,
    ProductViewSet, ReviewViewSet, ReviewInteractionViewSet, NotificationViewSet,
    AdminReportViewSet, BannedWordViewSet, ReviewReportViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')
router.register(r'products', ProductViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'review-interactions', ReviewInteractionViewSet, basename='review-interaction')
router.register(r'review-reports', ReviewReportViewSet, basename='review-report')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'admin-reports', AdminReportViewSet, basename='admin-report')
router.register(r'banned-words', BannedWordViewSet)

app_name = 'blog'

urlpatterns = [
    path('api/', include(router.urls)),
] 