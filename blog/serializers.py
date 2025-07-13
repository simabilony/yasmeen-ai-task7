from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Post, Comment, Favorite, Product, Review, ReviewInteraction, Notification, BannedWord

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer للمستخدم"""
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'bio', 'avatar', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer للتصنيف"""
    posts_count = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'posts_count', 'products_count']
        read_only_fields = ['id', 'slug', 'created_at']
    
    def get_posts_count(self, obj):
        return obj.posts.filter(status='published').count()
    
    def get_products_count(self, obj):
        return obj.products.filter(is_active=True).count()


class ProductSerializer(serializers.ModelSerializer):
    """Serializer للمنتج"""
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    average_rating = serializers.ReadOnlyField()
    total_reviews = serializers.ReadOnlyField()
    rating_distribution = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'category', 'category_id',
            'image', 'is_active', 'created_at', 'updated_at', 'average_rating',
            'total_reviews', 'rating_distribution'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer للمراجعة"""
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    helpful_score = serializers.ReadOnlyField()
    is_top_review = serializers.ReadOnlyField()
    user_interaction = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = [
            'id', 'product', 'product_id', 'user', 'rating', 'title', 'content',
            'is_approved', 'is_rejected', 'sentiment', 'helpful_votes', 'unhelpful_votes',
            'helpful_score', 'is_top_review', 'created_at', 'updated_at', 'user_interaction'
        ]
        read_only_fields = ['id', 'user', 'is_approved', 'is_rejected', 'sentiment', 'helpful_votes', 'unhelpful_votes', 'created_at', 'updated_at']
    
    def get_user_interaction(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            interaction = obj.interactions.filter(user=user).first()
            if interaction:
                return interaction.interaction_type
        return None
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ReviewInteractionSerializer(serializers.ModelSerializer):
    """Serializer لتفاعل المراجعة"""
    user = UserSerializer(read_only=True)
    review = ReviewSerializer(read_only=True)
    review_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ReviewInteraction
        fields = ['id', 'review', 'review_id', 'user', 'interaction_type', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer للإشعارات"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'user', 'notification_type', 'title', 'message', 'is_read', 'related_object_id', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer للتعليق"""
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    is_reply = serializers.ReadOnlyField()
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'parent', 'content', 'is_approved', 'created_at', 'updated_at', 'replies', 'is_reply']
        read_only_fields = ['id', 'author', 'is_approved', 'created_at', 'updated_at']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    """Serializer للمقال"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'category', 'category_id', 'content', 'excerpt',
            'featured_image', 'status', 'views', 'likes_count', 'comments_count',
            'created_at', 'updated_at', 'published_at', 'comments', 'is_liked', 'is_favorited'
        ]
        read_only_fields = ['id', 'slug', 'author', 'views', 'likes_count', 'comments_count', 'created_at', 'updated_at']
    
    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.likes.filter(id=user.id).exists()
        return False
    
    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.favorited_by.filter(user=user).exists()
        return False
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostCreateSerializer(serializers.ModelSerializer):
    """Serializer لإنشاء مقال جديد"""
    category_id = serializers.IntegerField()
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'featured_image', 'status', 'category_id']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer للمفضلة"""
    post = PostSerializer(read_only=True)
    post_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'post', 'post_id', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class DashboardSerializer(serializers.Serializer):
    """Serializer للوحة التحكم"""
    total_posts = serializers.IntegerField()
    total_favorites = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    total_reviews = serializers.IntegerField()
    recent_posts = PostSerializer(many=True)
    recent_reviews = ReviewSerializer(many=True)
    category_stats = serializers.ListField()
    monthly_posts = serializers.ListField()


class ProductAnalyticsSerializer(serializers.Serializer):
    """Serializer لتحليلات المنتج"""
    product = ProductSerializer()
    average_rating = serializers.FloatField()
    total_reviews = serializers.IntegerField()
    rating_distribution = serializers.DictField()
    top_reviews = ReviewSerializer(many=True)
    recent_reviews = ReviewSerializer(many=True)
    monthly_ratings = serializers.ListField()
    sentiment_analysis = serializers.DictField()


class AdminReportSerializer(serializers.Serializer):
    """Serializer لتقارير الإدارة"""
    pending_reviews = serializers.IntegerField()
    rejected_reviews = serializers.IntegerField()
    low_rated_reviews = serializers.IntegerField()
    top_products = ProductSerializer(many=True)
    top_reviewers = UserSerializer(many=True)
    banned_words_count = serializers.IntegerField()
    total_notifications = serializers.IntegerField()


class BannedWordSerializer(serializers.ModelSerializer):
    """Serializer للكلمات المحظورة"""
    
    class Meta:
        model = BannedWord
        fields = ['id', 'word', 'created_at']
        read_only_fields = ['id', 'created_at'] 