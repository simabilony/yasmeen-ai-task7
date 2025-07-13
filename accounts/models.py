from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """نموذج المستخدم المخصص"""
    bio = models.TextField(max_length=500, blank=True, verbose_name="نبذة شخصية")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="الصورة الشخصية")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="تاريخ الميلاد")
    phone = models.CharField(max_length=15, blank=True, verbose_name="رقم الهاتف")
    
    class Meta:
        verbose_name = "مستخدم"
        verbose_name_plural = "المستخدمين"
    
    def __str__(self):
        return self.username
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
