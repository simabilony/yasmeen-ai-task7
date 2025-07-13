# توثيق API - Swagger/OpenAPI

## نظرة عامة

هذا التوثيق يغطي جميع endpoints في نظام المدونة التفاعلية مع نظام تحليل وتفاعل ذكي على مراجعات المنتجات.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
جميع الـ endpoints تتطلب JWT Authentication باستثناء التسجيل وتسجيل الدخول.

### Header المطلوب:
```
Authorization: Bearer <access_token>
```

---

## 1. المصادقة (Authentication)

### تسجيل مستخدم جديد
```http
POST /api/auth/register/
```

**Request Body:**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123",
  "password2": "password123",
  "first_name": "أحمد",
  "last_name": "محمد"
}
```

**Response (201):**
```json
{
  "message": "تم التسجيل بنجاح",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "أحمد",
    "last_name": "محمد",
    "full_name": "أحمد محمد",
    "bio": "",
    "avatar": null,
    "date_joined": "2024-01-01T00:00:00Z"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

### تسجيل الدخول
```http
POST /api/auth/login/
```

**Request Body:**
```json
{
  "username": "testuser",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "message": "تم تسجيل الدخول بنجاح",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "أحمد",
    "last_name": "محمد",
    "full_name": "أحمد محمد",
    "bio": "",
    "avatar": null,
    "date_joined": "2024-01-01T00:00:00Z"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

### تسجيل الخروج
```http
POST /api/auth/logout/
```

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200):**
```json
{
  "message": "تم تسجيل الخروج بنجاح"
}
```

### عرض الملف الشخصي
```http
GET /api/auth/profile/
```

**Response (200):**
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "أحمد",
    "last_name": "محمد",
    "full_name": "أحمد محمد",
    "bio": "نبذة شخصية",
    "avatar": "/media/avatars/user.jpg",
    "phone": "+966501234567",
    "date_joined": "2024-01-01T00:00:00Z"
  }
}
```

### تحديث الملف الشخصي
```http
PUT /api/auth/profile/update/
```

**Request Body:**
```json
{
  "first_name": "أحمد",
  "last_name": "محمد",
  "email": "ahmed@example.com",
  "bio": "نبذة شخصية محدثة",
  "phone": "+966501234567"
}
```

**Response (200):**
```json
{
  "message": "تم تحديث الملف الشخصي بنجاح",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "ahmed@example.com",
    "first_name": "أحمد",
    "last_name": "محمد",
    "full_name": "أحمد محمد",
    "bio": "نبذة شخصية محدثة",
    "avatar": "/media/avatars/user.jpg",
    "phone": "+966501234567",
    "date_joined": "2024-01-01T00:00:00Z"
  }
}
```

---

## 2. المنتجات (Products)

### قائمة المنتجات
```http
GET /api/products/
```

**Query Parameters:**
- `category`: تصفية حسب التصنيف
- `is_active`: تصفية حسب الحالة (true/false)
- `search`: بحث في الاسم والوصف
- `ordering`: فرز (name, price, created_at, average_rating)

**Response (200):**
```json
{
  "count": 30,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "لابتوب HP Pavilion",
      "slug": "laptop-hp-pavilion",
      "description": "لابتوب ممتاز للأعمال والألعاب",
      "price": "1500.00",
      "category": {
        "id": 1,
        "name": "تقنية",
        "slug": "technology"
      },
      "image": "/media/products/laptop.jpg",
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "average_rating": 4.5,
      "total_reviews": 25,
      "rating_distribution": {
        "1": 2,
        "2": 1,
        "3": 3,
        "4": 8,
        "5": 11
      }
    }
  ]
}
```

### إنشاء منتج جديد
```http
POST /api/products/
```

**Request Body:**
```json
{
  "name": "منتج جديد",
  "description": "وصف المنتج",
  "price": "100.00",
  "category_id": 1,
  "image": null,
  "is_active": true
}
```

**Response (201):**
```json
{
  "id": 2,
  "name": "منتج جديد",
  "slug": "product-jadid",
  "description": "وصف المنتج",
  "price": "100.00",
  "category": {
    "id": 1,
    "name": "تقنية"
  },
  "image": null,
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "average_rating": 0,
  "total_reviews": 0,
  "rating_distribution": {
    "1": 0,
    "2": 0,
    "3": 0,
    "4": 0,
    "5": 0
  }
}
```

### تحليلات المنتج
```http
GET /api/products/{id}/analytics/
```

**Response (200):**
```json
{
  "product": {
    "id": 1,
    "name": "لابتوب HP Pavilion",
    "slug": "laptop-hp-pavilion",
    "description": "لابتوب ممتاز للأعمال والألعاب",
    "price": "1500.00",
    "category": {
      "id": 1,
      "name": "تقنية"
    },
    "image": "/media/products/laptop.jpg",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "average_rating": 4.5,
    "total_reviews": 25,
    "rating_distribution": {
      "1": 2,
      "2": 1,
      "3": 3,
      "4": 8,
      "5": 11
    }
  },
  "average_rating": 4.5,
  "total_reviews": 25,
  "rating_distribution": {
    "1": 2,
    "2": 1,
    "3": 3,
    "4": 8,
    "5": 11
  },
  "top_reviews": [
    {
      "id": 1,
      "user": {
        "id": 1,
        "username": "user1",
        "full_name": "أحمد محمد"
      },
      "rating": 5,
      "title": "منتج ممتاز",
      "content": "منتج رائع جداً",
      "helpful_votes": 15,
      "unhelpful_votes": 1,
      "helpful_score": 93.75,
      "is_top_review": true,
      "sentiment": "positive",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "recent_reviews": [
    {
      "id": 2,
      "user": {
        "id": 2,
        "username": "user2",
        "full_name": "فاطمة علي"
      },
      "rating": 4,
      "title": "منتج جيد",
      "content": "منتج جيد وسعر مناسب",
      "helpful_votes": 8,
      "unhelpful_votes": 2,
      "helpful_score": 80.0,
      "is_top_review": false,
      "sentiment": "positive",
      "created_at": "2024-01-02T00:00:00Z"
    }
  ],
  "monthly_ratings": [
    {
      "month": "2024-01",
      "average_rating": 4.5,
      "reviews_count": 25
    },
    {
      "month": "2023-12",
      "average_rating": 4.2,
      "reviews_count": 18
    }
  ],
  "sentiment_analysis": {
    "positive": 18,
    "negative": 3,
    "neutral": 4
  }
}
```

---

## 3. المراجعات (Reviews)

### قائمة المراجعات
```http
GET /api/reviews/
```

**Query Parameters:**
- `product`: تصفية حسب المنتج
- `user`: تصفية حسب المستخدم
- `rating`: تصفية حسب التقييم (1-5)
- `is_approved`: تصفية حسب حالة الموافقة
- `sentiment`: تصفية حسب الانطباع (positive/negative/neutral)
- `search`: بحث في العنوان والمحتوى
- `ordering`: فرز (created_at, rating, helpful_votes, helpful_score)

**Response (200):**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/reviews/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "لابتوب HP Pavilion"
      },
      "user": {
        "id": 1,
        "username": "user1",
        "full_name": "أحمد محمد"
      },
      "rating": 5,
      "title": "منتج ممتاز",
      "content": "منتج رائع جداً وأداؤه ممتاز",
      "is_approved": true,
      "is_rejected": false,
      "sentiment": "positive",
      "helpful_votes": 15,
      "unhelpful_votes": 1,
      "helpful_score": 93.75,
      "is_top_review": true,
      "user_interaction": "helpful",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### إنشاء مراجعة جديدة
```http
POST /api/reviews/
```

**Request Body:**
```json
{
  "product_id": 1,
  "rating": 5,
  "title": "منتج ممتاز",
  "content": "هذا المنتج رائع جداً وأداؤه ممتاز"
}
```

**Response (201):**
```json
{
  "id": 2,
  "product": {
    "id": 1,
    "name": "لابتوب HP Pavilion"
  },
  "user": {
    "id": 1,
    "username": "user1",
    "full_name": "أحمد محمد"
  },
  "rating": 5,
  "title": "منتج ممتاز",
  "content": "هذا المنتج رائع جداً وأداؤه ممتاز",
  "is_approved": false,
  "is_rejected": false,
  "sentiment": "positive",
  "helpful_votes": 0,
  "unhelpful_votes": 0,
  "helpful_score": 0,
  "is_top_review": false,
  "user_interaction": null,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### موافقة على المراجعة
```http
POST /api/reviews/{id}/approve/
```

**Response (200):**
```json
{
  "message": "تمت الموافقة على المراجعة"
}
```

### رفض المراجعة
```http
POST /api/reviews/{id}/reject/
```

**Response (200):**
```json
{
  "message": "تم رفض المراجعة"
}
```

### أفضل المراجعات
```http
GET /api/reviews/top_reviews/
```

**Response (200):**
```json
[
  {
    "id": 1,
    "product": {
      "id": 1,
      "name": "لابتوب HP Pavilion"
    },
    "user": {
      "id": 1,
      "username": "user1",
      "full_name": "أحمد محمد"
    },
    "rating": 5,
    "title": "منتج ممتاز",
    "content": "منتج رائع جداً وأداؤه ممتاز",
    "helpful_votes": 15,
    "unhelpful_votes": 1,
    "helpful_score": 93.75,
    "is_top_review": true,
    "sentiment": "positive",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

---

## 4. تفاعلات المراجعات (Review Interactions)

### قائمة التفاعلات
```http
GET /api/review-interactions/
```

**Response (200):**
```json
[
  {
    "id": 1,
    "review": {
      "id": 1,
      "title": "منتج ممتاز"
    },
    "user": {
      "id": 1,
      "username": "user1",
      "full_name": "أحمد محمد"
    },
    "interaction_type": "helpful",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### إضافة تفاعل
```http
POST /api/review-interactions/
```

**Request Body:**
```json
{
  "review_id": 1,
  "interaction_type": "helpful"
}
```

**Response (201):**
```json
{
  "id": 2,
  "review": {
    "id": 1,
    "title": "منتج ممتاز"
  },
  "user": {
    "id": 1,
    "username": "user1",
    "full_name": "أحمد محمد"
  },
  "interaction_type": "helpful",
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

## 5. الإشعارات (Notifications)

### قائمة الإشعارات
```http
GET /api/notifications/
```

**Response (200):**
```json
[
  {
    "id": 1,
    "user": {
      "id": 1,
      "username": "user1",
      "full_name": "أحمد محمد"
    },
    "notification_type": "review_approved",
    "title": "تمت الموافقة على مراجعتك",
    "message": "تمت الموافقة على مراجعتك للمنتج \"لابتوب HP Pavilion\"",
    "is_read": false,
    "related_object_id": 1,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### تحديد الإشعار كمقروء
```http
POST /api/notifications/{id}/mark_as_read/
```

**Response (200):**
```json
{
  "message": "تم تحديد الإشعار كمقروء"
}
```

### تحديد جميع الإشعارات كمقروءة
```http
POST /api/notifications/mark_all_as_read/
```

**Response (200):**
```json
{
  "message": "تم تحديد جميع الإشعارات كمقروءة"
}
```

---

## 6. تقارير الإدارة (Admin Reports)

### نظرة عامة على النظام
```http
GET /api/admin-reports/overview/
```

**Response (200):**
```json
{
  "pending_reviews": 15,
  "rejected_reviews": 5,
  "low_rated_reviews": 8,
  "top_products": [
    {
      "id": 1,
      "name": "لابتوب HP Pavilion",
      "average_rating": 4.5,
      "total_reviews": 25
    }
  ],
  "top_reviewers": [
    {
      "id": 1,
      "username": "user1",
      "full_name": "أحمد محمد",
      "reviews_count": 10
    }
  ],
  "banned_words_count": 20,
  "total_notifications": 150
}
```

---

## 7. الكلمات المحظورة (Banned Words)

### قائمة الكلمات المحظورة
```http
GET /api/banned-words/
```

**Response (200):**
```json
[
  {
    "id": 1,
    "word": "سيء",
    "created_at": "2024-01-01T00:00:00Z"
  },
  {
    "id": 2,
    "word": "رديء",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### إضافة كلمة محظورة
```http
POST /api/banned-words/
```

**Request Body:**
```json
{
  "word": "كلمة محظورة"
}
```

**Response (201):**
```json
{
  "id": 3,
  "word": "كلمة محظورة",
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

## 8. المقالات (Posts)

### قائمة المقالات
```http
GET /api/posts/
```

**Query Parameters:**
- `category`: تصفية حسب التصنيف
- `author`: تصفية حسب الكاتب
- `status`: تصفية حسب الحالة (draft/published)
- `search`: بحث في العنوان والمحتوى
- `ordering`: فرز (created_at, updated_at, title, views, likes_count)

**Response (200):**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "مقال تجريبي",
      "slug": "maqal-tajribi",
      "author": {
        "id": 1,
        "username": "user1",
        "full_name": "أحمد محمد"
      },
      "category": {
        "id": 1,
        "name": "تقنية"
      },
      "content": "محتوى المقال...",
      "excerpt": "ملخص المقال",
      "featured_image": "/media/posts/image.jpg",
      "status": "published",
      "views": 150,
      "likes_count": 25,
      "comments_count": 10,
      "is_liked": false,
      "is_favorited": false,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "published_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

---

## 9. لوحة التحكم (Dashboard)

### إحصائيات المستخدم
```http
GET /api/dashboard/stats/
```

**Response (200):**
```json
{
  "total_posts": 15,
  "total_favorites": 8,
  "total_comments": 25,
  "total_reviews": 12,
  "recent_posts": [
    {
      "id": 1,
      "title": "مقال حديث",
      "status": "published",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "recent_reviews": [
    {
      "id": 1,
      "title": "مراجعة حديثة",
      "rating": 5,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "category_stats": [
    {
      "category__name": "تقنية",
      "count": 8
    }
  ],
  "monthly_posts": [
    {
      "month": "2024-01",
      "count": 5
    }
  ]
}
```

---

## رموز الحالة (Status Codes)

- `200`: نجح الطلب
- `201`: تم إنشاء المورد بنجاح
- `400`: خطأ في البيانات المرسلة
- `401`: غير مصرح (يحتاج تسجيل دخول)
- `403`: محظور (يحتاج صلاحيات)
- `404`: المورد غير موجود
- `500`: خطأ في الخادم

## أخطاء شائعة

### خطأ في المصادقة
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### خطأ في الصلاحيات
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### خطأ في البيانات
```json
{
  "error": "بيانات الدخول غير صحيحة"
}
```

### خطأ في التحقق
```json
{
  "rating": ["تأكد من أن هذه القيمة أقل من أو تساوي 5."]
}
``` 