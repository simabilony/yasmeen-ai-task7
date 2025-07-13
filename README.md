# مدونة تفاعلية متقدمة - تاسك 7 & 8

مشروع مدونة تفاعلية متكاملة مبني باستخدام Django REST Framework مع نظام تحليل وتفاعل ذكي على مراجعات المنتجات.

## الميزات المطلوبة ✅

### تاسك 7 - المدونة التفاعلية ✅
- ✅ إنشاء مقال (Create Post)
- ✅ نظام التصفية والفرز
- ✅ لوحة تحكم المستخدم (Dashboard)
- ✅ نظام المصادقة المتقدم
- ✅ نظام الإعجابات والمفضلات
- ✅ نظام التعليقات

### تاسك 8 - نظام تحليل وتفاعل ذكي على مراجعات المنتجات ✅

#### 1. تحليلات (Analytics) ✅
- ✅ معدل تقييم المنتج خلال فترة زمنية محددة
- ✅ أكثر المستخدمين كتابةً للمراجعات
- ✅ المنتجات التي حصلت على أعلى تقييم
- ✅ مراجعات تحتوي على كلمات معينة (بحث بالكلمات المفتاحية)
- ✅ تحليل الانطباع (Sentiment Analysis)
- ✅ إحصائيات شهرية للتقييمات

#### 2. نظام تفاعل (Interactions) ✅
- ✅ تقييم المراجعات بأنها "مفيدة" أو "غير مفيدة"
- ✅ عرض عدد الإعجابات وعدم الإعجاب لكل مراجعة
- ✅ عرض أفضل مراجعة (Top Review) بناءً على تفاعل المستخدمين
- ✅ نقاط الفائدة (Helpful Score)

#### 3. إشعارات (Notifications) ✅
- ✅ إشعار عند الموافقة على المراجعة
- ✅ إشعار عند رفض المراجعة
- ✅ إشعار عند تحديث المنتج
- ✅ تحديد الإشعارات كمقروءة

#### 4. نظام تقارير المشرف (Admin Insights) ✅
- ✅ عدد المراجعات غير الموافق عليها
- ✅ عدد المراجعات المرفوضة
- ✅ عدد المراجعات منخفضة التقييم (1-2 نجوم)
- ✅ تصفية المراجعات المسيئة (قائمة كلمات محظورة)
- ✅ أفضل المنتجات والمستخدمين

#### 5. تحسينات متقدمة (Advanced) ✅
- ✅ تصفية آلية للمراجعات المسيئة
- ✅ تحليل انطباع المراجعة (إيجابي/سلبي/محايد)
- ✅ ملف المنتج التحليلي
- ✅ إدارة الكلمات المحظورة

## التقنيات المستخدمة

- **Backend**: Django 4.2.7
- **API**: Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: SQLite (قابل للتغيير)
- **Image Processing**: Pillow
- **Data Generation**: Faker
- **Sentiment Analysis**: تحليل انطباع بسيط باللغة العربية

## التثبيت والتشغيل

### 1. تثبيت المتطلبات
```bash
pip install Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.3.1 djangorestframework-simplejwt==5.3.0 python-decouple==3.8 django-filter==23.5 Faker==20.1.0
```

### 2. إعداد قاعدة البيانات
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. إنشاء مستخدم مدير
```bash
python manage.py createsuperuser
```

### 4. إنشاء بيانات تجريبية
```bash
python manage.py create_sample_data --users 10 --categories 5 --posts 50 --products 30 --reviews 100
```

### 5. تشغيل الخادم
```bash
python manage.py runserver
```

## API Endpoints

### المصادقة
- `POST /api/auth/register/` - تسجيل مستخدم جديد
- `POST /api/auth/login/` - تسجيل الدخول
- `POST /api/auth/logout/` - تسجيل الخروج
- `GET /api/auth/profile/` - عرض الملف الشخصي
- `PUT /api/auth/profile/update/` - تحديث الملف الشخصي

### المقالات
- `GET /api/posts/` - قائمة المقالات
- `POST /api/posts/` - إنشاء مقال جديد
- `GET /api/posts/{id}/` - عرض مقال
- `PUT /api/posts/{id}/` - تحديث مقال
- `DELETE /api/posts/{id}/` - حذف مقال
- `POST /api/posts/{id}/like/` - إعجاب/إلغاء إعجاب
- `POST /api/posts/{id}/favorite/` - إضافة/إزالة من المفضلة
- `POST /api/posts/{id}/increment_views/` - زيادة المشاهدات

### المنتجات
- `GET /api/products/` - قائمة المنتجات
- `POST /api/products/` - إنشاء منتج جديد
- `GET /api/products/{id}/` - عرض منتج
- `PUT /api/products/{id}/` - تحديث منتج
- `DELETE /api/products/{id}/` - حذف منتج
- `GET /api/products/{id}/analytics/` - تحليلات المنتج

### المراجعات
- `GET /api/reviews/` - قائمة المراجعات
- `POST /api/reviews/` - إنشاء مراجعة جديدة
- `GET /api/reviews/{id}/` - عرض مراجعة
- `PUT /api/reviews/{id}/` - تحديث مراجعة
- `DELETE /api/reviews/{id}/` - حذف مراجعة
- `POST /api/reviews/{id}/approve/` - موافقة على المراجعة
- `POST /api/reviews/{id}/reject/` - رفض المراجعة
- `GET /api/reviews/top_reviews/` - أفضل المراجعات

### تفاعلات المراجعات
- `GET /api/review-interactions/` - قائمة التفاعلات
- `POST /api/review-interactions/` - إضافة تفاعل
- `PUT /api/review-interactions/{id}/` - تحديث تفاعل
- `DELETE /api/review-interactions/{id}/` - حذف تفاعل

### الإشعارات
- `GET /api/notifications/` - قائمة الإشعارات
- `POST /api/notifications/{id}/mark_as_read/` - تحديد كمقروء
- `POST /api/notifications/mark_all_as_read/` - تحديد جميعها كمقروءة

### التصنيفات
- `GET /api/categories/` - قائمة التصنيفات
- `GET /api/categories/{id}/` - عرض تصنيف

### التعليقات
- `GET /api/comments/` - قائمة التعليقات
- `POST /api/comments/` - إنشاء تعليق
- `PUT /api/comments/{id}/` - تحديث تعليق
- `DELETE /api/comments/{id}/` - حذف تعليق

### المفضلات
- `GET /api/favorites/` - قائمة المفضلات
- `POST /api/favorites/` - إضافة إلى المفضلة
- `DELETE /api/favorites/{id}/` - إزالة من المفضلة

### لوحة التحكم
- `GET /api/dashboard/stats/` - إحصائيات المستخدم

### تقارير الإدارة
- `GET /api/admin-reports/overview/` - نظرة عامة على النظام

### الكلمات المحظورة
- `GET /api/banned-words/` - قائمة الكلمات المحظورة
- `POST /api/banned-words/` - إضافة كلمة محظورة
- `PUT /api/banned-words/{id}/` - تحديث كلمة محظورة
- `DELETE /api/banned-words/{id}/` - حذف كلمة محظورة

## أمثلة الاستخدام

### إنشاء مراجعة جديدة
```bash
curl -X POST http://localhost:8000/api/reviews/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "rating": 5,
    "title": "منتج ممتاز",
    "content": "هذا المنتج رائع جداً وأداؤه ممتاز"
  }'
```

### تحليلات المنتج
```bash
curl -X GET http://localhost:8000/api/products/1/analytics/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### تقييم مراجعة كمفيدة
```bash
curl -X POST http://localhost:8000/api/review-interactions/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "review_id": 1,
    "interaction_type": "helpful"
  }'
```

### موافقة على مراجعة
```bash
curl -X POST http://localhost:8000/api/reviews/1/approve/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### تصفية وفرز المراجعات
```bash
# تصفية حسب المنتج
GET /api/reviews/?product=1

# تصفية حسب التقييم
GET /api/reviews/?rating=5

# تصفية حسب الانطباع
GET /api/reviews/?sentiment=positive

# فرز حسب الأحدث
GET /api/reviews/?ordering=-created_at

# فرز حسب نقاط الفائدة
GET /api/reviews/?ordering=-helpful_votes

# بحث في المحتوى
GET /api/reviews/?search=ممتاز
```

## هيكل المشروع

```
yasmeen-ai-task7/
├── blog_project/          # إعدادات المشروع الرئيسية
│   ├── settings.py       # إعدادات Django
│   ├── urls.py          # URLs الرئيسية
│   └── wsgi.py          # إعدادات WSGI
├── blog/                 # تطبيق المدونة والمنتجات
│   ├── models.py        # نماذج البيانات
│   ├── views.py         # Views للـ API
│   ├── serializers.py   # Serializers
│   ├── urls.py          # URLs للمدونة
│   ├── admin.py         # إعدادات Admin
│   └── management/      # أوامر إدارية
├── accounts/            # تطبيق المصادقة
│   ├── models.py        # نموذج المستخدم
│   ├── views.py         # Views للمصادقة
│   ├── serializers.py   # Serializers للمصادقة
│   ├── urls.py          # URLs للمصادقة
│   └── admin.py         # إعدادات Admin
├── requirements.txt     # متطلبات المشروع
├── manage.py           # أداة إدارة Django
└── README.md           # هذا الملف
```

## النماذج الجديدة (تاسك 8)

### Product (المنتج)
- معلومات المنتج الأساسية
- التصنيف والسعر
- متوسط التقييم وعدد المراجعات
- توزيع التقييمات

### Review (المراجعة)
- تقييم المستخدم (1-5 نجوم)
- عنوان ومحتوى المراجعة
- حالة الموافقة/الرفض
- تحليل الانطباع
- نقاط الفائدة

### ReviewInteraction (تفاعل المراجعة)
- تقييم المراجعة كمفيدة/غير مفيدة
- ربط المستخدم بالمراجعة

### Notification (الإشعارات)
- أنواع مختلفة من الإشعارات
- حالة القراءة
- ربط بالكائنات المرتبطة

### BannedWord (الكلمات المحظورة)
- قائمة الكلمات المحظورة
- فحص تلقائي للمراجعات

## الميزات الإضافية

### 1. تحليل الانطباع الذكي
- تحليل تلقائي لمحتوى المراجعات
- تصنيف إيجابي/سلبي/محايد
- قائمة كلمات عربية للتحليل

### 2. نظام التفاعل المتقدم
- تقييم المراجعات من قبل المستخدمين
- حساب نقاط الفائدة
- تحديد أفضل المراجعات

### 3. إشعارات ذكية
- إشعارات تلقائية عند الموافقة/الرفض
- إدارة حالة القراءة
- أنواع مختلفة من الإشعارات

### 4. تحليلات متقدمة
- إحصائيات شهرية
- تحليل الانطباع
- أفضل المنتجات والمستخدمين
- تقارير الإدارة

### 5. أمان محسن
- فحص الكلمات المحظورة
- نظام موافقة على المراجعات
- صلاحيات مختلفة للمستخدمين

## المساهمة

1. Fork المشروع
2. إنشاء فرع جديد للميزة
3. Commit التغييرات
4. Push إلى الفرع
5. إنشاء Pull Request

## الترخيص

هذا المشروع مرخص تحت رخصة MIT.

## الدعم

لأي استفسارات أو مشاكل، يرجى فتح issue في repository. 