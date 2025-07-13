# Swagger/OpenAPI Documentation - Task 7, 8 & 9

## نظرة عامة على API

هذا التوثيق يغطي جميع نقاط النهاية (endpoints) في نظام المدونة التفاعلية المتقدم مع نظام تحليل وتفاعل ذكي على مراجعات المنتجات وتحسينات عرض وتفاعل المراجعات.

**Base URL**: `http://localhost:8000/api/`

## المصادقة (Authentication)

### تسجيل مستخدم جديد
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "user123",
  "email": "user@example.com",
  "password": "password123",
  "first_name": "أحمد",
  "last_name": "محمد",
  "bio": "مطور ويب",
  "phone": "+966501234567"
}
```

### تسجيل الدخول
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "user123",
  "password": "password123"
}
```

### تسجيل الخروج
```http
POST /api/auth/logout/
Authorization: Bearer <access_token>
```

### عرض الملف الشخصي
```http
GET /api/auth/profile/
Authorization: Bearer <access_token>
```

### تحديث الملف الشخصي
```http
PUT /api/auth/profile/update/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "أحمد",
  "last_name": "محمد",
  "bio": "مطور ويب محترف",
  "phone": "+966501234567"
}
```

## المقالات (Posts)

### قائمة المقالات
```http
GET /api/posts/
```

**Query Parameters:**
- `category`: تصفية حسب التصنيف
- `author`: تصفية حسب الكاتب
- `status`: تصفية حسب الحالة (draft/published)
- `search`: بحث في العنوان والمحتوى
- `ordering`: ترتيب (-created_at, -views, -likes_count)

### إنشاء مقال جديد
```http
POST /api/posts/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "عنوان المقال",
  "content": "محتوى المقال...",
  "excerpt": "ملخص المقال",
  "category_id": 1,
  "status": "published"
}
```

### عرض مقال
```http
GET /api/posts/{id}/
```

### تحديث مقال
```http
PUT /api/posts/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "عنوان محدث",
  "content": "محتوى محدث...",
  "excerpt": "ملخص محدث",
  "category_id": 1,
  "status": "published"
}
```

### حذف مقال
```http
DELETE /api/posts/{id}/
Authorization: Bearer <access_token>
```

### إعجاب/إلغاء إعجاب
```http
POST /api/posts/{id}/like/
Authorization: Bearer <access_token>
```

### إضافة/إزالة من المفضلة
```http
POST /api/posts/{id}/favorite/
Authorization: Bearer <access_token>
```

### زيادة المشاهدات
```http
POST /api/posts/{id}/increment_views/
Authorization: Bearer <access_token>
```

## المنتجات (Products)

### قائمة المنتجات
```http
GET /api/products/
```

**Query Parameters:**
- `category`: تصفية حسب التصنيف
- `is_active`: تصفية حسب الحالة
- `search`: بحث في الاسم والوصف
- `ordering`: ترتيب (-created_at, name, price, average_rating)

### إنشاء منتج جديد
```http
POST /api/products/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "اسم المنتج",
  "description": "وصف المنتج...",
  "price": 99.99,
  "category_id": 1,
  "is_active": true
}
```

### عرض منتج
```http
GET /api/products/{id}/
```

### تحديث منتج
```http
PUT /api/products/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "اسم محدث",
  "description": "وصف محدث...",
  "price": 89.99,
  "category_id": 1,
  "is_active": true
}
```

### حذف منتج
```http
DELETE /api/products/{id}/
Authorization: Bearer <access_token>
```

### تحليلات المنتج
```http
GET /api/products/{id}/analytics/
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "product": {
    "id": 1,
    "name": "اسم المنتج",
    "average_rating": 4.5,
    "total_reviews": 25
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
  "top_reviews": [...],
  "recent_reviews": [...],
  "monthly_ratings": [...],
  "sentiment_analysis": {
    "positive": 15,
    "negative": 3,
    "neutral": 7
  }
}
```

## المراجعات (Reviews) - محسنة (Task 9)

### قائمة المراجعات
```http
GET /api/reviews/
```

**Query Parameters (محسنة - Task 9):**
- `product`: تصفية حسب المنتج
- `user`: تصفية حسب المستخدم
- `rating`: تصفية حسب التقييم (1-5)
- `sentiment`: تصفية حسب الانطباع (positive/negative/neutral)
- `is_approved`: تصفية حسب حالة الموافقة
- `search`: بحث في العنوان والمحتوى
- `sort`: ترتيب مخصص (newest/highest_rating/most_helpful/most_viewed/most_interactive)
- `min_rating`: الحد الأدنى للتقييم
- `max_rating`: الحد الأقصى للتقييم
- `limit`: عدد النتائج

### إنشاء مراجعة جديدة (محسن - Task 9)
```http
POST /api/reviews/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "product_id": 1,
  "rating": 5,
  "title": "منتج ممتاز",
  "content": "هذا المنتج رائع جداً وأداؤه ممتاز"
}
```

**Response (محسن - Task 9):**
```json
{
  "message": "تم إرسال المراجعة بنجاح",
  "status": "pending_approval",
  "review_id": 123,
  "details": "سيتم مراجعة المراجعة من قبل الإدارة قبل النشر"
}
```

### عرض مراجعة
```http
GET /api/reviews/{id}/
```

**Response (محسن - Task 9):**
```json
{
  "id": 1,
  "product": {...},
  "user": {...},
  "rating": 5,
  "title": "منتج ممتاز",
  "content": "محتوى المراجعة...",
  "is_approved": true,
  "sentiment": "positive",
  "helpful_votes": 15,
  "unhelpful_votes": 2,
  "helpful_score": 88.24,
  "is_top_review": true,
  "views_count": 156,
  "total_interactions": 17,
  "user_interaction": "helpful",
  "has_user_reported": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### تحديث مراجعة
```http
PUT /api/reviews/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "rating": 4,
  "title": "عنوان محدث",
  "content": "محتوى محدث..."
}
```

### حذف مراجعة
```http
DELETE /api/reviews/{id}/
Authorization: Bearer <access_token>
```

### موافقة على المراجعة
```http
POST /api/reviews/{id}/approve/
Authorization: Bearer <access_token>
```

### رفض المراجعة
```http
POST /api/reviews/{id}/reject/
Authorization: Bearer <access_token>
```

### زيادة عداد المشاهدات (جديد - Task 9)
```http
POST /api/reviews/{id}/increment_views/
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "message": "تم تحديث عداد المشاهدات",
  "views_count": 157
}
```

### أفضل المراجعات
```http
GET /api/reviews/top_reviews/
```

### مراجعات مصفاة ومرتبة (جديد - Task 9)
```http
GET /api/reviews/filtered_reviews/
```

**Query Parameters:**
- `rating`: تصفية حسب التقييم
- `sentiment`: تصفية حسب الانطباع
- `min_rating`: الحد الأدنى للتقييم
- `max_rating`: الحد الأقصى للتقييم
- `sort`: ترتيب (newest/highest_rating/most_helpful/most_viewed/most_interactive)
- `limit`: عدد النتائج

## بلاغات المراجعات (Review Reports) - جديد (Task 9)

### قائمة البلاغات
```http
GET /api/review-reports/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `review`: تصفية حسب المراجعة
- `reason`: تصفية حسب السبب
- `is_resolved`: تصفية حسب حالة الحل
- `ordering`: ترتيب (-created_at)

### إنشاء بلاغ جديد
```http
POST /api/review-reports/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "review_id": 1,
  "reason": "inappropriate",
  "description": "هذه المراجعة تحتوي على محتوى غير مناسب"
}
```

**Response:**
```json
{
  "message": "تم إرسال البلاغ بنجاح",
  "report_id": 45,
  "status": "pending_review"
}
```

### عرض بلاغ
```http
GET /api/review-reports/{id}/
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": 45,
  "review": {...},
  "reporter": {...},
  "reason": "inappropriate",
  "description": "وصف البلاغ...",
  "is_resolved": false,
  "admin_notes": "",
  "created_at": "2024-01-15T10:30:00Z",
  "resolved_at": null
}
```

### تحديث بلاغ
```http
PUT /api/review-reports/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "reason": "spam",
  "description": "وصف محدث..."
}
```

### حذف بلاغ
```http
DELETE /api/review-reports/{id}/
Authorization: Bearer <access_token>
```

### حل البلاغ
```http
POST /api/review-reports/{id}/resolve/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "admin_notes": "تم فحص البلاغ واتخاذ الإجراء المناسب"
}
```

**Response:**
```json
{
  "message": "تم حل البلاغ بنجاح"
}
```

## تفاعلات المراجعات (Review Interactions)

### قائمة التفاعلات
```http
GET /api/review-interactions/
Authorization: Bearer <access_token>
```

### إضافة تفاعل
```http
POST /api/review-interactions/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "review_id": 1,
  "interaction_type": "helpful"
}
```

### تحديث تفاعل
```http
PUT /api/review-interactions/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "interaction_type": "unhelpful"
}
```

### حذف تفاعل
```http
DELETE /api/review-interactions/{id}/
Authorization: Bearer <access_token>
```

## الإشعارات (Notifications)

### قائمة الإشعارات
```http
GET /api/notifications/
Authorization: Bearer <access_token>
```

### تحديد إشعار كمقروء
```http
POST /api/notifications/{id}/mark_as_read/
Authorization: Bearer <access_token>
```

### تحديد جميع الإشعارات كمقروءة
```http
POST /api/notifications/mark_all_as_read/
Authorization: Bearer <access_token>
```

## التصنيفات (Categories)

### قائمة التصنيفات
```http
GET /api/categories/
```

**Query Parameters:**
- `search`: بحث في الاسم والوصف

### عرض تصنيف
```http
GET /api/categories/{id}/
```

## التعليقات (Comments)

### قائمة التعليقات
```http
GET /api/comments/
```

**Query Parameters:**
- `post`: تصفية حسب المقال
- `author`: تصفية حسب الكاتب
- `is_approved`: تصفية حسب حالة الموافقة
- `ordering`: ترتيب (-created_at)

### إنشاء تعليق
```http
POST /api/comments/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "post": 1,
  "parent": null,
  "content": "محتوى التعليق..."
}
```

### تحديث تعليق
```http
PUT /api/comments/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "content": "محتوى محدث..."
}
```

### حذف تعليق
```http
DELETE /api/comments/{id}/
Authorization: Bearer <access_token>
```

## المفضلات (Favorites)

### قائمة المفضلات
```http
GET /api/favorites/
Authorization: Bearer <access_token>
```

### إضافة إلى المفضلة
```http
POST /api/favorites/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "post_id": 1
}
```

### إزالة من المفضلة
```http
DELETE /api/favorites/{id}/
Authorization: Bearer <access_token>
```

## لوحة التحكم (Dashboard)

### إحصائيات المستخدم
```http
GET /api/dashboard/stats/
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "total_posts": 15,
  "total_favorites": 8,
  "total_comments": 25,
  "total_reviews": 12,
  "recent_posts": [...],
  "recent_reviews": [...],
  "category_stats": [...],
  "monthly_posts": [...]
}
```

## تقارير الإدارة (Admin Reports)

### نظرة عامة على النظام
```http
GET /api/admin-reports/overview/
Authorization: Bearer <access_token>
```

**Response (محسن - Task 9):**
```json
{
  "pending_reviews": 5,
  "rejected_reviews": 3,
  "low_rated_reviews": 8,
  "reported_reviews_count": 12,
  "top_products": [...],
  "top_reviewers": [...],
  "banned_words_count": 15,
  "total_notifications": 45
}
```

## الكلمات المحظورة (Banned Words)

### قائمة الكلمات المحظورة
```http
GET /api/banned-words/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `search`: بحث في الكلمة

### إضافة كلمة محظورة
```http
POST /api/banned-words/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "word": "كلمة محظورة"
}
```

### تحديث كلمة محظورة
```http
PUT /api/banned-words/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "word": "كلمة محدثة"
}
```

### حذف كلمة محظورة
```http
DELETE /api/banned-words/{id}/
Authorization: Bearer <access_token>
```

## أمثلة الاستخدام المتقدمة (Task 9)

### تصفية وفرز المراجعات المتقدم
```http
# تصفية حسب التقييم والانطباع مع ترتيب
GET /api/reviews/?rating=5&sentiment=positive&sort=highest_rating&limit=10

# تصفية حسب نطاق التقييم
GET /api/reviews/?min_rating=4&max_rating=5&sort=most_helpful

# ترتيب حسب الأكثر مشاهدة
GET /api/reviews/?sort=most_viewed&limit=20

# ترتيب حسب الأكثر تفاعلاً
GET /api/reviews/?sort=most_interactive&rating=4
```

### مراجعات مصفاة ومرتبة
```http
# مراجعات 5 نجوم مرتبة حسب الأحدث
GET /api/reviews/filtered_reviews/?rating=5&sort=newest&limit=15

# مراجعات إيجابية مرتبة حسب الأكثر مفيدة
GET /api/reviews/filtered_reviews/?sentiment=positive&sort=most_helpful&limit=10
```

### إدارة البلاغات
```http
# إنشاء بلاغ
POST /api/review-reports/
{
  "review_id": 1,
  "reason": "fake",
  "description": "هذه مراجعة مزيفة"
}

# حل البلاغ
POST /api/review-reports/45/resolve/
{
  "admin_notes": "تم فحص البلاغ واتخاذ الإجراء المناسب"
}
```

## رموز الحالة (Status Codes)

- `200 OK`: نجح الطلب
- `201 Created`: تم إنشاء المورد بنجاح
- `400 Bad Request`: بيانات غير صحيحة
- `401 Unauthorized`: غير مصرح
- `403 Forbidden`: محظور
- `404 Not Found`: غير موجود
- `500 Internal Server Error`: خطأ في الخادم

## أنواع البيانات (Data Types)

### ReviewReport Reasons
- `inappropriate`: محتوى غير مناسب
- `spam`: رسائل مزعجة
- `fake`: مراجعة مزيفة
- `offensive`: محتوى مسيء
- `other`: أخرى

### Review Sentiments
- `positive`: إيجابي
- `negative`: سلبي
- `neutral`: محايد

### Interaction Types
- `helpful`: مفيدة
- `unhelpful`: غير مفيدة

### Notification Types
- `review_approved`: موافقة على المراجعة
- `review_rejected`: رفض المراجعة
- `review_reply`: رد على المراجعة
- `product_update`: تحديث المنتج
- `review_reported`: إبلاغ عن مراجعة

### Sort Options (Task 9)
- `newest`: الأحدث
- `highest_rating`: الأعلى تقييم
- `most_helpful`: الأكثر مفيدة
- `most_viewed`: الأكثر مشاهدة
- `most_interactive`: الأكثر تفاعلاً

## ملاحظات مهمة

1. **المصادقة**: معظم نقاط النهاية تتطلب مصادقة باستخدام JWT token
2. **الصلاحيات**: بعض العمليات تتطلب صلاحيات مدير
3. **التصفية**: جميع نقاط النهاية تدعم التصفية والفرز
4. **الحدود**: يمكن تحديد عدد النتائج باستخدام `limit`
5. **البحث**: معظم نقاط النهاية تدعم البحث النصي
6. **الترتيب**: يمكن ترتيب النتائج بطرق مختلفة
7. **الاستجابة**: جميع الاستجابات بتنسيق JSON
8. **التواريخ**: جميع التواريخ بتنسيق ISO 8601 