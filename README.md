# مدونة تفاعلية متقدمة - تاسك 7, 8 & 9

مشروع مدونة تفاعلية متكاملة مبني باستخدام Django REST Framework مع نظام تحليل وتفاعل ذكي على مراجعات المنتجات وتحسينات متقدمة لعرض وتفاعل المراجعات.

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

### تاسك 9 - تحسين عرض وتفاعل المراجعات ✅

#### 1. دعم الترتيب والتصفية المتقدم ✅
- ✅ ترتيب المراجعات حسب الأحدث (`sort=newest`)
- ✅ ترتيب المراجعات حسب الأعلى تقييم (`sort=highest_rating`)
- ✅ ترتيب المراجعات حسب الأكثر تفاعلاً (`sort=most_helpful`)
- ✅ ترتيب المراجعات حسب الأكثر مشاهدة (`sort=most_viewed`)
- ✅ ترتيب المراجعات حسب الأكثر تفاعلاً (`sort=most_interactive`)
- ✅ تصفية المراجعات حسب عدد النجوم (`rating=5`)
- ✅ تصفية المراجعات حسب الانطباع (`sentiment=positive`)
- ✅ تصفية المراجعات حسب نطاق التقييم (`min_rating=4&max_rating=5`)

#### 2. عداد المشاهدات ✅
- ✅ تسجيل عدد مرات قراءة كل مراجعة
- ✅ API لزيادة عداد المشاهدات (`POST /api/reviews/{id}/increment_views/`)
- ✅ عرض عدد المشاهدات في بيانات المراجعة

#### 3. نظام الإبلاغ عن المراجعات ✅
- ✅ نموذج ReviewReport للإبلاغ عن المراجعات
- ✅ أسباب الإبلاغ: محتوى غير مناسب، رسائل مزعجة، مراجعة مزيفة، محتوى مسيء
- ✅ API لإنشاء بلاغ (`POST /api/review-reports/`)
- ✅ API لحل البلاغات (`POST /api/review-reports/{id}/resolve/`)
- ✅ إشعارات للإدارة عند الإبلاغ عن مراجعة

#### 4. تحسين الرد عند إرسال مراجعة ✅
- ✅ رد واضح من السيرفر عند نشر مراجعة جديدة
- ✅ معلومات الحالة: نجاح/فشل + تفاصيل
- ✅ معرف المراجعة وحالة الموافقة

#### 5. تحسين شكل بيانات المراجعة ✅
- ✅ عدد مرات المشاهدة (`views_count`)
- ✅ عدد الإعجابات وعدم الإعجاب (`helpful_votes`, `unhelpful_votes`)
- ✅ إجمالي التفاعلات (`total_interactions`)
- ✅ هل سبق أن قام المستخدم بالتفاعل مع المراجعة؟ (`user_interaction`)
- ✅ هل على المراجعة بلاغ؟ (`has_user_reported`)

## التقنيات المستخدمة

- **Backend**: Django 4.2.7
- **API**: Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: SQLite (قابل للتغيير)
- **Image Processing**: Pillow
- **Data Generation**: Faker
- **Sentiment Analysis**: تحليل انطباع بسيط باللغة العربية
- **Filtering & Sorting**: Django Filter Backend

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
python manage.py create_sample_data --users 10 --categories 5 --posts 50 --products 30 --reviews 100 --reports 20
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

### المراجعات (محسنة - تاسك 9)
- `GET /api/reviews/` - قائمة المراجعات
- `POST /api/reviews/` - إنشاء مراجعة جديدة
- `GET /api/reviews/{id}/` - عرض مراجعة
- `PUT /api/reviews/{id}/` - تحديث مراجعة
- `DELETE /api/reviews/{id}/` - حذف مراجعة
- `POST /api/reviews/{id}/approve/` - موافقة على المراجعة
- `POST /api/reviews/{id}/reject/` - رفض المراجعة
- `POST /api/reviews/{id}/increment_views/` - زيادة عداد المشاهدات
- `GET /api/reviews/top_reviews/` - أفضل المراجعات
- `GET /api/reviews/filtered_reviews/` - مراجعات مصفاة ومرتبة

### بلاغات المراجعات (جديد - تاسك 9)
- `GET /api/review-reports/` - قائمة البلاغات
- `POST /api/review-reports/` - إنشاء بلاغ جديد
- `GET /api/review-reports/{id}/` - عرض بلاغ
- `PUT /api/review-reports/{id}/` - تحديث بلاغ
- `DELETE /api/review-reports/{id}/` - حذف بلاغ
- `POST /api/review-reports/{id}/resolve/` - حل البلاغ

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

### إنشاء مراجعة جديدة (محسن - تاسك 9)
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

# الرد المحسن:
{
  "message": "تم إرسال المراجعة بنجاح",
  "status": "pending_approval",
  "review_id": 123,
  "details": "سيتم مراجعة المراجعة من قبل الإدارة قبل النشر"
}
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

### زيادة عداد مشاهدات المراجعة (جديد - تاسك 9)
```bash
curl -X POST http://localhost:8000/api/reviews/1/increment_views/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# الرد:
{
  "message": "تم تحديث عداد المشاهدات",
  "views_count": 156
}
```

### إنشاء بلاغ عن مراجعة (جديد - تاسك 9)
```bash
curl -X POST http://localhost:8000/api/review-reports/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "review_id": 1,
    "reason": "inappropriate",
    "description": "هذه المراجعة تحتوي على محتوى غير مناسب"
  }'

# الرد:
{
  "message": "تم إرسال البلاغ بنجاح",
  "report_id": 45,
  "status": "pending_review"
}
```

### حل بلاغ (جديد - تاسك 9)
```bash
curl -X POST http://localhost:8000/api/review-reports/45/resolve/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "admin_notes": "تم فحص البلاغ واتخاذ الإجراء المناسب"
  }'
```

### تصفية وفرز المراجعات المتقدم (محسن - تاسك 9)
```bash
# تصفية حسب المنتج
GET /api/reviews/?product=1

# تصفية حسب التقييم
GET /api/reviews/?rating=5

# تصفية حسب الانطباع
GET /api/reviews/?sentiment=positive

# تصفية حسب نطاق التقييم
GET /api/reviews/?min_rating=4&max_rating=5

# ترتيب حسب الأحدث
GET /api/reviews/?sort=newest

# ترتيب حسب الأعلى تقييم
GET /api/reviews/?sort=highest_rating

# ترتيب حسب الأكثر تفاعلاً
GET /api/reviews/?sort=most_helpful

# ترتيب حسب الأكثر مشاهدة
GET /api/reviews/?sort=most_viewed

# ترتيب حسب الأكثر تفاعلاً
GET /api/reviews/?sort=most_interactive

# تحديد عدد النتائج
GET /api/reviews/?limit=10

# فرز حسب نقاط الفائدة
GET /api/reviews/?ordering=-helpful_votes

# بحث في المحتوى
GET /api/reviews/?search=ممتاز

# مراجعات مصفاة ومرتبة
GET /api/reviews/filtered_reviews/?rating=5&sort=highest_rating&limit=20
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

## النماذج الجديدة (تاسك 8 & 9)

### Product (المنتج)
- معلومات المنتج الأساسية
- التصنيف والسعر
- متوسط التقييم وعدد المراجعات
- توزيع التقييمات

### Review (المراجعة) - محسن (تاسك 9)
- تقييم المستخدم (1-5 نجوم)
- عنوان ومحتوى المراجعة
- حالة الموافقة/الرفض
- تحليل الانطباع
- نقاط الفائدة
- **عداد المشاهدات** (`views_count`)
- **إجمالي التفاعلات** (`total_interactions`)

### ReviewReport (بلاغ المراجعة) - جديد (تاسك 9)
- ربط المراجعة بالمبلغ
- سبب البلاغ (محتوى غير مناسب، رسائل مزعجة، مراجعة مزيفة، محتوى مسيء)
- وصف إضافي للبلاغ
- حالة الحل
- ملاحظات الإدارة
- تواريخ الإنشاء والحل

### ReviewInteraction (تفاعل المراجعة)
- تقييم المراجعة كمفيدة/غير مفيدة
- ربط المستخدم بالمراجعة

### Notification (الإشعارات) - محسن (تاسك 9)
- أنواع مختلفة من الإشعارات
- حالة القراءة
- ربط بالكائنات المرتبطة
- **إشعارات البلاغات** (`review_reported`)

### BannedWord (الكلمات المحظورة)
- قائمة الكلمات المحظورة
- فحص تلقائي للمراجعات

## الميزات الإضافية (تاسك 9)

### 1. نظام الترتيب والتصفية المتقدم
- **ترتيب متعدد الخيارات**: الأحدث، الأعلى تقييم، الأكثر تفاعلاً، الأكثر مشاهدة
- **تصفية دقيقة**: حسب التقييم، الانطباع، نطاق التقييم
- **حد النتائج**: تحديد عدد النتائج المرجعة
- **بحث متقدم**: في العنوان والمحتوى

### 2. عداد المشاهدات الذكي
- **تتبع المشاهدات**: لكل مراجعة بشكل منفصل
- **API مخصص**: لزيادة العداد
- **عرض في البيانات**: عدد المشاهدات في استجابة API

### 3. نظام الإبلاغ المحسن
- **أسباب متعددة**: 5 أسباب مختلفة للإبلاغ
- **إدارة البلاغات**: حل وتتبع البلاغات
- **إشعارات تلقائية**: للإدارة عند الإبلاغ
- **منع التكرار**: بلاغ واحد لكل مستخدم لكل مراجعة

### 4. تحسين استجابة API
- **رد واضح**: عند إنشاء مراجعة جديدة
- **معلومات مفصلة**: حالة المراجعة ومعرفها
- **رسائل واضحة**: للنجاح والفشل

### 5. بيانات مراجعة محسنة
- **معلومات إضافية**: عداد المشاهدات، التفاعلات
- **حالة التفاعل**: هل تفاعل المستخدم مع المراجعة؟
- **حالة البلاغ**: هل أبلغ المستخدم عن المراجعة؟

### 6. تحسينات الإدارة
- **إدارة البلاغات**: عرض وحل البلاغات
- **إحصائيات إضافية**: عدد المراجعات المبلغ عنها
- **واجهة محسنة**: في Django Admin

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