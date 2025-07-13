# مدونة تفاعلية متقدمة - تاسك 7

مشروع مدونة تفاعلية متكاملة مبني باستخدام Django REST Framework مع جميع الميزات المتقدمة المطلوبة.

## الميزات المطلوبة ✅

### 1. إنشاء مقال (Create Post)
- ✅ صفحة إنشاء مقال للمستخدم المسجل
- ✅ الحقول: title، body، category (Dropdown)، author (يُملأ تلقائياً)
- ✅ التخزين في قاعدة البيانات
- ✅ ظهور المقال في الصفحة الرئيسية

### 2. نظام التصفية والفرز
- ✅ تصفية المقالات حسب التصنيف
- ✅ تصفية المقالات حسب الكاتب
- ✅ فرز حسب الأحدث والأقدم
- ✅ فرز أبجدي
- ✅ بحث في المحتوى

### 3. لوحة تحكم المستخدم (Dashboard)
- ✅ إحصائيات المستخدم (عدد المقالات، المفضلات، التعليقات)
- ✅ عرض المقالات الحديثة
- ✅ إحصائيات التصنيفات
- ✅ إحصائيات شهرية
- ✅ إمكانية حذف وتعديل المقالات

### 4. نظام المصادقة المتقدم
- ✅ تسجيل مستخدمين جدد
- ✅ تسجيل الدخول والخروج
- ✅ JWT Authentication
- ✅ ملف شخصي قابل للتحديث

### 5. ميزات إضافية
- ✅ نظام الإعجابات
- ✅ نظام المفضلات
- ✅ نظام التعليقات
- ✅ إحصائيات المشاهدات
- ✅ دعم الصور

## التقنيات المستخدمة

- **Backend**: Django 4.2.7
- **API**: Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: SQLite (قابل للتغيير)
- **Image Processing**: Pillow
- **Data Generation**: Faker

## التثبيت والتشغيل

### 1. تثبيت المتطلبات
```bash
pip install -r requirements.txt
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

### 4. إنشاء بيانات تجريبية (اختياري)
```bash
python manage.py create_sample_data --users 10 --categories 5 --posts 50
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

## أمثلة الاستخدام

### تسجيل مستخدم جديد
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "password2": "password123",
    "first_name": "أحمد",
    "last_name": "محمد"
  }'
```

### تسجيل الدخول
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### إنشاء مقال جديد
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "مقال تجريبي",
    "content": "محتوى المقال هنا...",
    "excerpt": "ملخص المقال",
    "category_id": 1,
    "status": "published"
  }'
```

### تصفية وفرز المقالات
```bash
# تصفية حسب التصنيف
GET /api/posts/?category=1

# تصفية حسب الكاتب
GET /api/posts/?author=1

# فرز حسب الأحدث
GET /api/posts/?ordering=-created_at

# فرز حسب الأقدم
GET /api/posts/?ordering=created_at

# فرز أبجدي
GET /api/posts/?ordering=title

# بحث في المحتوى
GET /api/posts/?search=كلمة البحث
```

## هيكل المشروع

```
yasmeen-ai-task7/
├── blog_project/          # إعدادات المشروع الرئيسية
│   ├── settings.py       # إعدادات Django
│   ├── urls.py          # URLs الرئيسية
│   └── wsgi.py          # إعدادات WSGI
├── blog/                 # تطبيق المدونة
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

## الميزات الإضافية

### 1. نظام الإعجابات
- يمكن للمستخدمين الإعجاب بالمقالات
- عرض عدد الإعجابات لكل مقال
- إمكانية إلغاء الإعجاب

### 2. نظام المفضلات
- إضافة المقالات إلى المفضلة
- عرض قائمة المفضلات للمستخدم
- إزالة المقالات من المفضلة

### 3. نظام التعليقات
- إضافة تعليقات على المقالات
- دعم الردود على التعليقات
- نظام موافقة على التعليقات

### 4. إحصائيات متقدمة
- عدد المشاهدات لكل مقال
- إحصائيات التصنيفات
- إحصائيات شهرية للمقالات

### 5. أمان متقدم
- JWT Authentication
- صلاحيات مختلفة للمستخدمين
- حماية من CSRF
- CORS support

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