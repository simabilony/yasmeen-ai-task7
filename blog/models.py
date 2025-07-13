from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime, timedelta

User = get_user_model()


class Category(models.Model):
    """نموذج التصنيف"""
    name = models.CharField(max_length=100, verbose_name="اسم التصنيف")
    slug = models.SlugField(unique=True, blank=True, verbose_name="الرابط المختصر")
    description = models.TextField(blank=True, verbose_name="وصف التصنيف")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    
    class Meta:
        verbose_name = "تصنيف"
        verbose_name_plural = "التصنيفات"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    """نموذج المنتج"""
    name = models.CharField(max_length=200, verbose_name="اسم المنتج")
    slug = models.SlugField(unique=True, blank=True, verbose_name="الرابط المختصر")
    description = models.TextField(verbose_name="وصف المنتج")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="التصنيف")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="صورة المنتج")
    is_active = models.BooleanField(default=True, verbose_name="متاح للبيع")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    class Meta:
        verbose_name = "منتج"
        verbose_name_plural = "المنتجات"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def average_rating(self):
        """متوسط تقييم المنتج"""
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return reviews.aggregate(avg=models.Avg('rating'))['avg']
        return 0
    
    @property
    def total_reviews(self):
        """إجمالي عدد المراجعات"""
        return self.reviews.filter(is_approved=True).count()
    
    @property
    def rating_distribution(self):
        """توزيع التقييمات"""
        reviews = self.reviews.filter(is_approved=True)
        distribution = {}
        for i in range(1, 6):
            distribution[i] = reviews.filter(rating=i).count()
        return distribution


class Post(models.Model):
    """نموذج المقال"""
    STATUS_CHOICES = [
        ('draft', 'مسودة'),
        ('published', 'منشور'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="عنوان المقال")
    slug = models.SlugField(unique=True, blank=True, verbose_name="الرابط المختصر")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="الكاتب")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', verbose_name="التصنيف")
    content = models.TextField(verbose_name="محتوى المقال")
    excerpt = models.TextField(max_length=500, blank=True, verbose_name="ملخص المقال")
    featured_image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name="الصورة المميزة")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="الحالة")
    views = models.PositiveIntegerField(default=0, verbose_name="عدد المشاهدات")
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True, verbose_name="الإعجابات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="تاريخ النشر")
    
    class Meta:
        verbose_name = "مقال"
        verbose_name_plural = "المقالات"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    @property
    def likes_count(self):
        return self.likes.count()
    
    @property
    def comments_count(self):
        return self.comments.count()


class Review(models.Model):
    """نموذج المراجعة"""
    SENTIMENT_CHOICES = [
        ('positive', 'إيجابي'),
        ('negative', 'سلبي'),
        ('neutral', 'محايد'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="المنتج")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="المستخدم")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="التقييم"
    )
    title = models.CharField(max_length=200, verbose_name="عنوان المراجعة")
    content = models.TextField(verbose_name="محتوى المراجعة")
    is_approved = models.BooleanField(default=False, verbose_name="موافق عليه")
    is_rejected = models.BooleanField(default=False, verbose_name="مرفوض")
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES, blank=True, verbose_name="الانطباع")
    helpful_votes = models.PositiveIntegerField(default=0, verbose_name="أصوات مفيدة")
    unhelpful_votes = models.PositiveIntegerField(default=0, verbose_name="أصوات غير مفيدة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    class Meta:
        verbose_name = "مراجعة"
        verbose_name_plural = "المراجعات"
        ordering = ['-created_at']
        unique_together = ['product', 'user']  # مراجعة واحدة لكل مستخدم لكل منتج
    
    def __str__(self):
        return f'مراجعة {self.user.username} على {self.product.name}'
    
    @property
    def helpful_score(self):
        """نقاط الفائدة"""
        total = self.helpful_votes + self.unhelpful_votes
        if total == 0:
            return 0
        return (self.helpful_votes / total) * 100
    
    @property
    def is_top_review(self):
        """هل هي أفضل مراجعة؟"""
        return self.helpful_score >= 80 and self.rating >= 4


class ReviewInteraction(models.Model):
    """نموذج تفاعل المستخدم مع المراجعة"""
    INTERACTION_CHOICES = [
        ('helpful', 'مفيدة'),
        ('unhelpful', 'غير مفيدة'),
    ]
    
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='interactions', verbose_name="المراجعة")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_interactions', verbose_name="المستخدم")
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_CHOICES, verbose_name="نوع التفاعل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التفاعل")
    
    class Meta:
        verbose_name = "تفاعل المراجعة"
        verbose_name_plural = "تفاعلات المراجعات"
        unique_together = ['review', 'user']  # تفاعل واحد لكل مستخدم مع كل مراجعة
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.interaction_type} - {self.review}'


class Notification(models.Model):
    """نموذج الإشعارات"""
    NOTIFICATION_TYPES = [
        ('review_approved', 'موافقة على المراجعة'),
        ('review_rejected', 'رفض المراجعة'),
        ('review_reply', 'رد على المراجعة'),
        ('product_update', 'تحديث المنتج'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name="المستخدم")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, verbose_name="نوع الإشعار")
    title = models.CharField(max_length=200, verbose_name="عنوان الإشعار")
    message = models.TextField(verbose_name="رسالة الإشعار")
    is_read = models.BooleanField(default=False, verbose_name="مقروء")
    related_object_id = models.PositiveIntegerField(blank=True, null=True, verbose_name="معرف الكائن المرتبط")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    
    class Meta:
        verbose_name = "إشعار"
        verbose_name_plural = "الإشعارات"
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.title}'


class Comment(models.Model):
    """نموذج التعليق"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="المقال")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="الكاتب")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name="التعليق الأب")
    content = models.TextField(verbose_name="محتوى التعليق")
    is_approved = models.BooleanField(default=False, verbose_name="موافق عليه")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    class Meta:
        verbose_name = "تعليق"
        verbose_name_plural = "التعليقات"
        ordering = ['-created_at']
    
    def __str__(self):
        return f'تعليق من {self.author.username} على {self.post.title}'
    
    @property
    def is_reply(self):
        return self.parent is not None


class Favorite(models.Model):
    """نموذج المفضلة"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name="المستخدم")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorited_by', verbose_name="المقال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")
    
    class Meta:
        verbose_name = "مفضلة"
        verbose_name_plural = "المفضلات"
        unique_together = ['user', 'post']
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} أضاف {self.post.title} إلى المفضلة'


class BannedWord(models.Model):
    """نموذج الكلمات المحظورة"""
    word = models.CharField(max_length=100, unique=True, verbose_name="الكلمة المحظورة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")
    
    class Meta:
        verbose_name = "كلمة محظورة"
        verbose_name_plural = "الكلمات المحظورة"
        ordering = ['word']
    
    def __str__(self):
        return self.word
