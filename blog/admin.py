from django.contrib import admin
from .models import (
    Category, Post, Comment, Favorite, Product, Review, 
    ReviewInteraction, Notification, BannedWord
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at', 'posts_count', 'products_count']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def posts_count(self, obj):
        return obj.posts.count()
    posts_count.short_description = 'عدد المقالات'
    
    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'عدد المنتجات'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_active', 'average_rating', 'total_reviews', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'price']
    
    def average_rating(self, obj):
        return f"{obj.average_rating:.1f}"
    average_rating.short_description = 'متوسط التقييم'
    
    def total_reviews(self, obj):
        return obj.total_reviews
    total_reviews.short_description = 'عدد المراجعات'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'title', 'is_approved', 'is_rejected', 'sentiment', 'helpful_score', 'created_at']
    list_filter = ['rating', 'is_approved', 'is_rejected', 'sentiment', 'created_at']
    search_fields = ['title', 'content', 'user__username', 'product__name']
    list_editable = ['is_approved', 'is_rejected', 'sentiment']
    readonly_fields = ['helpful_votes', 'unhelpful_votes', 'helpful_score']
    
    def helpful_score(self, obj):
        return f"{obj.helpful_score:.1f}%"
    helpful_score.short_description = 'نقاط الفائدة'


@admin.register(ReviewInteraction)
class ReviewInteractionAdmin(admin.ModelAdmin):
    list_display = ['user', 'review', 'interaction_type', 'created_at']
    list_filter = ['interaction_type', 'created_at']
    search_fields = ['user__username', 'review__title']
    readonly_fields = ['created_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']


@admin.register(BannedWord)
class BannedWordAdmin(admin.ModelAdmin):
    list_display = ['word', 'created_at']
    search_fields = ['word']
    readonly_fields = ['created_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at', 'views', 'likes_count', 'comments_count']
    list_filter = ['status', 'category', 'created_at', 'author']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    list_editable = ['status']
    
    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = 'الإعجابات'
    
    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = 'التعليقات'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'content_preview', 'is_approved', 'created_at', 'is_reply']
    list_filter = ['is_approved', 'created_at', 'author']
    search_fields = ['content', 'author__username', 'post__title']
    list_editable = ['is_approved']
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'محتوى التعليق'
    
    def is_reply(self, obj):
        return obj.parent is not None
    is_reply.boolean = True
    is_reply.short_description = 'رد'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__title']
    date_hierarchy = 'created_at' 