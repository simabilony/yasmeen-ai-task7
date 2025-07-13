from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

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
