from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count, Q, Avg, Sum
from django.utils import timezone
from datetime import datetime, timedelta
import re
from .models import (
    Category, Post, Comment, Favorite, Product, Review, 
    ReviewInteraction, Notification, BannedWord, ReviewReport
)
from .serializers import (
    CategorySerializer, PostSerializer, PostCreateSerializer,
    CommentSerializer, FavoriteSerializer, DashboardSerializer,
    ProductSerializer, ReviewSerializer, ReviewInteractionSerializer,
    NotificationSerializer, ProductAnalyticsSerializer, AdminReportSerializer,
    BannedWordSerializer, ReviewReportSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet للتصنيفات"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet للمنتجات"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at', 'average_rating']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Product.objects.select_related('category').prefetch_related('reviews')
    
    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        """تحليلات المنتج"""
        product = self.get_object()
        
        # إحصائيات أساسية
        reviews = product.reviews.filter(is_approved=True)
        average_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        total_reviews = reviews.count()
        
        # توزيع التقييمات
        rating_distribution = {}
        for i in range(1, 6):
            rating_distribution[i] = reviews.filter(rating=i).count()
        
        # أفضل المراجعات
        top_reviews = reviews.filter(helpful_votes__gt=0).order_by('-helpful_votes')[:5]
        
        # المراجعات الحديثة
        recent_reviews = reviews.order_by('-created_at')[:10]
        
        # إحصائيات شهرية
        monthly_ratings = []
        for i in range(6):
            date = timezone.now() - timedelta(days=30*i)
            month_start = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
            
            month_reviews = reviews.filter(created_at__range=(month_start, month_end))
            avg_rating = month_reviews.aggregate(avg=Avg('rating'))['avg'] or 0
            
            monthly_ratings.append({
                'month': month_start.strftime('%Y-%m'),
                'average_rating': round(avg_rating, 2),
                'reviews_count': month_reviews.count()
            })
        
        # تحليل الانطباع
        sentiment_analysis = {
            'positive': reviews.filter(sentiment='positive').count(),
            'negative': reviews.filter(sentiment='negative').count(),
            'neutral': reviews.filter(sentiment='neutral').count(),
        }
        
        data = {
            'product': ProductSerializer(product).data,
            'average_rating': round(average_rating, 2),
            'total_reviews': total_reviews,
            'rating_distribution': rating_distribution,
            'top_reviews': ReviewSerializer(top_reviews, many=True).data,
            'recent_reviews': ReviewSerializer(recent_reviews, many=True).data,
            'monthly_ratings': monthly_ratings,
            'sentiment_analysis': sentiment_analysis
        }
        
        serializer = ProductAnalyticsSerializer(data)
        return Response(serializer.data)


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


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet للمراجعات"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product', 'user', 'rating', 'is_approved', 'sentiment']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'rating', 'helpful_votes', 'helpful_score', 'views_count', 'total_interactions']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Review.objects.select_related('user', 'product').prefetch_related('interactions', 'reports')
        
        # تصفية حسب عدد النجوم
        rating_filter = self.request.query_params.get('rating', None)
        if rating_filter:
            try:
                rating = int(rating_filter)
                if 1 <= rating <= 5:
                    queryset = queryset.filter(rating=rating)
            except ValueError:
                pass
        
        # تصفية حسب الانطباع
        sentiment_filter = self.request.query_params.get('sentiment', None)
        if sentiment_filter in ['positive', 'negative', 'neutral']:
            queryset = queryset.filter(sentiment=sentiment_filter)
        
        # ترتيب مخصص
        sort_by = self.request.query_params.get('sort', None)
        if sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'highest_rating':
            queryset = queryset.order_by('-rating', '-created_at')
        elif sort_by == 'most_helpful':
            queryset = queryset.order_by('-helpful_votes', '-created_at')
        elif sort_by == 'most_viewed':
            queryset = queryset.order_by('-views_count', '-created_at')
        elif sort_by == 'most_interactive':
            queryset = queryset.annotate(
                total_interactions=Count('interactions')
            ).order_by('-total_interactions', '-created_at')
        
        return queryset
    
    def perform_create(self, serializer):
        review = serializer.save()
        # تحليل الانطباع البسيط
        self.analyze_sentiment(review)
        # فحص الكلمات المحظورة
        self.check_banned_words(review)
        
        # إرسال رد واضح
        return Response({
            'message': 'تم إرسال المراجعة بنجاح',
            'status': 'pending_approval',
            'review_id': review.id,
            'details': 'سيتم مراجعة المراجعة من قبل الإدارة قبل النشر'
        }, status=status.HTTP_201_CREATED)
    
    def analyze_sentiment(self, review):
        """تحليل انطباع المراجعة"""
        positive_words = ['ممتاز', 'رائع', 'جيد', 'مفيد', 'مقترح', 'أفضل', 'ممتازة', 'جيدة']
        negative_words = ['سيء', 'رديء', 'مخيب', 'غير مفيد', 'مرفوض', 'أسوأ', 'سيئة', 'رديئة']
        
        content = review.content.lower()
        positive_count = sum(1 for word in positive_words if word in content)
        negative_count = sum(1 for word in negative_words if word in content)
        
        if positive_count > negative_count:
            review.sentiment = 'positive'
        elif negative_count > positive_count:
            review.sentiment = 'negative'
        else:
            review.sentiment = 'neutral'
        
        review.save()
    
    def check_banned_words(self, review):
        """فحص الكلمات المحظورة"""
        banned_words = BannedWord.objects.values_list('word', flat=True)
        content = review.content.lower()
        
        for word in banned_words:
            if word.lower() in content:
                review.is_rejected = True
                review.save()
                break
    
    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        """زيادة عداد مشاهدات المراجعة"""
        review = self.get_object()
        review.increment_views()
        return Response({
            'message': 'تم تحديث عداد المشاهدات',
            'views_count': review.views_count
        })
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """موافقة على المراجعة"""
        review = self.get_object()
        review.is_approved = True
        review.is_rejected = False
        review.save()
        
        # إرسال إشعار للمستخدم
        Notification.objects.create(
            user=review.user,
            notification_type='review_approved',
            title='تمت الموافقة على مراجعتك',
            message=f'تمت الموافقة على مراجعتك للمنتج "{review.product.name}"',
            related_object_id=review.id
        )
        
        return Response({'message': 'تمت الموافقة على المراجعة'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """رفض المراجعة"""
        review = self.get_object()
        review.is_approved = False
        review.is_rejected = True
        review.save()
        
        # إرسال إشعار للمستخدم
        Notification.objects.create(
            user=review.user,
            notification_type='review_rejected',
            title='تم رفض مراجعتك',
            message=f'تم رفض مراجعتك للمنتج "{review.product.name}"',
            related_object_id=review.id
        )
        
        return Response({'message': 'تم رفض المراجعة'})
    
    @action(detail=False, methods=['get'])
    def top_reviews(self, request):
        """أفضل المراجعات"""
        reviews = Review.objects.filter(
            is_approved=True,
            helpful_score__gte=80,
            rating__gte=4
        ).order_by('-helpful_score', '-rating')[:10]
        
        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def filtered_reviews(self, request):
        """مراجعات مصفاة ومرتبة"""
        queryset = self.get_queryset()
        
        # تطبيق المزيد من الفلاتر
        min_rating = request.query_params.get('min_rating', None)
        if min_rating:
            try:
                min_rating = int(min_rating)
                if 1 <= min_rating <= 5:
                    queryset = queryset.filter(rating__gte=min_rating)
            except ValueError:
                pass
        
        max_rating = request.query_params.get('max_rating', None)
        if max_rating:
            try:
                max_rating = int(max_rating)
                if 1 <= max_rating <= 5:
                    queryset = queryset.filter(rating__lte=max_rating)
            except ValueError:
                pass
        
        # تحديد عدد النتائج
        limit = request.query_params.get('limit', 20)
        try:
            limit = int(limit)
            if limit > 0:
                queryset = queryset[:limit]
        except ValueError:
            queryset = queryset[:20]
        
        serializer = ReviewSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class ReviewReportViewSet(viewsets.ModelViewSet):
    """ViewSet لبلاغات المراجعات"""
    serializer_class = ReviewReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['review', 'reason', 'is_resolved']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return ReviewReport.objects.select_related('review', 'reporter')
        return ReviewReport.objects.filter(reporter=self.request.user).select_related('review')
    
    def perform_create(self, serializer):
        report = serializer.save()
        
        # إرسال إشعار للإدارة
        if self.request.user.is_staff:
            Notification.objects.create(
                user=self.request.user,
                notification_type='review_reported',
                title='بلاغ جديد عن مراجعة',
                message=f'تم الإبلاغ عن مراجعة للمنتج "{report.review.product.name}"',
                related_object_id=report.id
            )
        
        return Response({
            'message': 'تم إرسال البلاغ بنجاح',
            'report_id': report.id,
            'status': 'pending_review'
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """حل البلاغ"""
        if not request.user.is_staff:
            return Response({'error': 'غير مصرح لك بحل البلاغات'}, status=status.HTTP_403_FORBIDDEN)
        
        report = self.get_object()
        report.is_resolved = True
        report.resolved_at = timezone.now()
        report.admin_notes = request.data.get('admin_notes', '')
        report.save()
        
        return Response({'message': 'تم حل البلاغ بنجاح'})


class ReviewInteractionViewSet(viewsets.ModelViewSet):
    """ViewSet لتفاعلات المراجعات"""
    serializer_class = ReviewInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ReviewInteraction.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        interaction = serializer.save()
        review = interaction.review
        
        # تحديث إحصائيات المراجعة
        if interaction.interaction_type == 'helpful':
            review.helpful_votes += 1
        else:
            review.unhelpful_votes += 1
        
        review.save()
    
    def perform_update(self, serializer):
        old_interaction = self.get_object()
        new_interaction = serializer.save()
        review = new_interaction.review
        
        # تحديث الإحصائيات
        if old_interaction.interaction_type == 'helpful':
            review.helpful_votes -= 1
        else:
            review.unhelpful_votes -= 1
        
        if new_interaction.interaction_type == 'helpful':
            review.helpful_votes += 1
        else:
            review.unhelpful_votes += 1
        
        review.save()


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet للإشعارات"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """تحديد الإشعار كمقروء"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'message': 'تم تحديد الإشعار كمقروء'})
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """تحديد جميع الإشعارات كمقروءة"""
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'message': 'تم تحديد جميع الإشعارات كمقروءة'})


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
        total_reviews = Review.objects.filter(user=user).count()
        
        # المقالات الحديثة
        recent_posts = Post.objects.filter(author=user).order_by('-created_at')[:5]
        
        # المراجعات الحديثة
        recent_reviews = Review.objects.filter(user=user).order_by('-created_at')[:5]
        
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
            'total_reviews': total_reviews,
            'recent_posts': PostSerializer(recent_posts, many=True).data,
            'recent_reviews': ReviewSerializer(recent_reviews, many=True).data,
            'category_stats': list(category_stats),
            'monthly_posts': monthly_posts
        }
        
        serializer = DashboardSerializer(data)
        return Response(serializer.data)


class AdminReportViewSet(viewsets.ViewSet):
    """ViewSet لتقارير الإدارة"""
    permission_classes = [permissions.IsAdminUser]
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """نظرة عامة على النظام"""
        # المراجعات المعلقة
        pending_reviews = Review.objects.filter(is_approved=False, is_rejected=False).count()
        
        # المراجعات المرفوضة
        rejected_reviews = Review.objects.filter(is_rejected=True).count()
        
        # المراجعات منخفضة التقييم
        low_rated_reviews = Review.objects.filter(rating__lte=2).count()
        
        # المراجعات المبلغ عنها
        reported_reviews_count = ReviewReport.objects.filter(is_resolved=False).count()
        
        # أفضل المنتجات
        top_products = Product.objects.annotate(
            avg_rating=Avg('reviews__rating')
        ).filter(avg_rating__isnull=False).order_by('-avg_rating')[:5]
        
        # أكثر المستخدمين كتابة للمراجعات
        top_reviewers = User.objects.annotate(
            reviews_count=Count('reviews')
        ).filter(reviews_count__gt=0).order_by('-reviews_count')[:5]
        
        # عدد الكلمات المحظورة
        banned_words_count = BannedWord.objects.count()
        
        # إجمالي الإشعارات
        total_notifications = Notification.objects.count()
        
        data = {
            'pending_reviews': pending_reviews,
            'rejected_reviews': rejected_reviews,
            'low_rated_reviews': low_rated_reviews,
            'reported_reviews_count': reported_reviews_count,
            'top_products': ProductSerializer(top_products, many=True).data,
            'top_reviewers': UserSerializer(top_reviewers, many=True).data,
            'banned_words_count': banned_words_count,
            'total_notifications': total_notifications
        }
        
        serializer = AdminReportSerializer(data)
        return Response(serializer.data)


class BannedWordViewSet(viewsets.ModelViewSet):
    """ViewSet للكلمات المحظورة"""
    queryset = BannedWord.objects.all()
    serializer_class = BannedWordSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ['word']
    ordering = ['word'] 