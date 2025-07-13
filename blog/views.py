from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Category, Post, Comment, Favorite
from .serializers import (
    CategorySerializer, PostSerializer, PostCreateSerializer,
    CommentSerializer, FavoriteSerializer, DashboardSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet للتصنيفات"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet للمقالات"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'author', 'status']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'updated_at', 'title', 'views', 'likes_count']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Post.objects.select_related('author', 'category').prefetch_related('likes', 'comments')
        if not self.request.user.is_authenticated:
            return queryset.filter(status='published')
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        post = serializer.save()
        if post.status == 'published':
            post.published_at = timezone.now()
            post.save()
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """إضافة أو إزالة الإعجاب"""
        post = self.get_object()
        user = request.user
        
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            return Response({'message': 'تم إزالة الإعجاب'})
        else:
            post.likes.add(user)
            return Response({'message': 'تم الإعجاب بالمقال'})
    
    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        """إضافة أو إزالة من المفضلة"""
        post = self.get_object()
        user = request.user
        
        favorite, created = Favorite.objects.get_or_create(user=user, post=post)
        if not created:
            favorite.delete()
            return Response({'message': 'تم إزالة المقال من المفضلة'})
        
        return Response({'message': 'تم إضافة المقال إلى المفضلة'})
    
    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        """زيادة عدد المشاهدات"""
        post = self.get_object()
        post.views += 1
        post.save()
        return Response({'views': post.views})


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet للتعليقات"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['post', 'author', 'is_approved']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Comment.objects.select_related('author', 'post').prefetch_related('replies')
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoriteViewSet(viewsets.ModelViewSet):
    """ViewSet للمفضلات"""
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('post', 'post__author', 'post__category')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DashboardViewSet(viewsets.ViewSet):
    """ViewSet للوحة التحكم"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """إحصائيات المستخدم"""
        user = request.user
        
        # إحصائيات أساسية
        total_posts = Post.objects.filter(author=user).count()
        total_favorites = Favorite.objects.filter(user=user).count()
        total_comments = Comment.objects.filter(author=user).count()
        
        # المقالات الحديثة
        recent_posts = Post.objects.filter(author=user).order_by('-created_at')[:5]
        
        # إحصائيات التصنيفات
        category_stats = Post.objects.filter(author=user).values('category__name').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # إحصائيات شهرية
        monthly_posts = []
        for i in range(6):
            date = timezone.now() - timedelta(days=30*i)
            month_start = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
            
            count = Post.objects.filter(
                author=user,
                created_at__range=(month_start, month_end)
            ).count()
            
            monthly_posts.append({
                'month': month_start.strftime('%Y-%m'),
                'count': count
            })
        
        data = {
            'total_posts': total_posts,
            'total_favorites': total_favorites,
            'total_comments': total_comments,
            'recent_posts': PostSerializer(recent_posts, many=True).data,
            'category_stats': list(category_stats),
            'monthly_posts': monthly_posts
        }
        
        serializer = DashboardSerializer(data)
        return Response(serializer.data) 