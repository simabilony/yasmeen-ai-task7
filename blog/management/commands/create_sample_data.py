from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from blog.models import Category, Post, Comment, Favorite, Product, Review, ReviewInteraction, Notification, BannedWord
from faker import Faker
import random

User = get_user_model()
fake = Faker(['ar_SA'])


class Command(BaseCommand):
    help = 'إنشاء بيانات تجريبية للمدونة والمنتجات'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='عدد المستخدمين المراد إنشاؤهم'
        )
        parser.add_argument(
            '--categories',
            type=int,
            default=5,
            help='عدد التصنيفات المراد إنشاؤها'
        )
        parser.add_argument(
            '--posts',
            type=int,
            default=50,
            help='عدد المقالات المراد إنشاؤها'
        )
        parser.add_argument(
            '--products',
            type=int,
            default=30,
            help='عدد المنتجات المراد إنشاؤها'
        )
        parser.add_argument(
            '--reviews',
            type=int,
            default=100,
            help='عدد المراجعات المراد إنشاؤها'
        )

    def handle(self, *args, **options):
        self.stdout.write('بدء إنشاء البيانات التجريبية...')
        
        # إنشاء التصنيفات
        categories = self.create_categories(options['categories'])
        
        # إنشاء المستخدمين
        users = self.create_users(options['users'])
        
        # إنشاء المقالات
        posts = self.create_posts(options['posts'], users, categories)
        
        # إنشاء المنتجات
        products = self.create_products(options['products'], categories)
        
        # إنشاء المراجعات
        reviews = self.create_reviews(options['reviews'], users, products)
        
        # إنشاء التفاعلات
        self.create_review_interactions(reviews, users)
        
        # إنشاء التعليقات
        self.create_comments(posts, users)
        
        # إنشاء المفضلات
        self.create_favorites(posts, users)
        
        # إنشاء الكلمات المحظورة
        self.create_banned_words()
        
        # إنشاء الإشعارات
        self.create_notifications(users, reviews)
        
        self.stdout.write(
            self.style.SUCCESS('تم إنشاء البيانات التجريبية بنجاح!')
        )

    def create_categories(self, count):
        categories = []
        category_names = [
            'تقنية', 'برمجة', 'تطوير الويب', 'الذكاء الاصطناعي', 'الأمن السيبراني',
            'قواعد البيانات', 'تطوير التطبيقات', 'تعلم الآلة', 'بلوكتشين', 'الحوسبة السحابية'
        ]
        
        for i in range(min(count, len(category_names))):
            category = Category.objects.create(
                name=category_names[i],
                description=fake.text(max_nb_chars=200)
            )
            categories.append(category)
            self.stdout.write(f'تم إنشاء التصنيف: {category.name}')
        
        return categories

    def create_users(self, count):
        users = []
        for i in range(count):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                bio=fake.text(max_nb_chars=300),
                phone=fake.phone_number()
            )
            users.append(user)
            self.stdout.write(f'تم إنشاء المستخدم: {user.username}')
        
        return users

    def create_posts(self, count, users, categories):
        posts = []
        for i in range(count):
            post = Post.objects.create(
                title=fake.sentence(nb_words=6),
                content=fake.text(max_nb_chars=2000),
                excerpt=fake.text(max_nb_chars=300),
                author=random.choice(users),
                category=random.choice(categories),
                status=random.choice(['draft', 'published']),
                views=random.randint(0, 1000)
            )
            posts.append(post)
            self.stdout.write(f'تم إنشاء المقال: {post.title}')
        
        return posts

    def create_products(self, count, categories):
        products = []
        product_names = [
            'لابتوب HP Pavilion', 'هاتف Samsung Galaxy', 'سماعات AirPods', 'ساعة Apple Watch',
            'كاميرا Canon EOS', 'طابعة HP LaserJet', 'شاشة LG UltraWide', 'لوحة مفاتيح Logitech',
            'ماوس Razer DeathAdder', 'ميكروفون Blue Yeti', 'مكبر صوت JBL', 'قارئ Kindle',
            'جهاز iPad Pro', 'كاميرا GoPro Hero', 'سماعات Sony WH-1000XM4'
        ]
        
        for i in range(count):
            product = Product.objects.create(
                name=random.choice(product_names) + f' {fake.word()}',
                description=fake.text(max_nb_chars=500),
                price=random.uniform(50, 2000),
                category=random.choice(categories),
                is_active=random.choice([True, True, True, False])  # 75% نشط
            )
            products.append(product)
            self.stdout.write(f'تم إنشاء المنتج: {product.name}')
        
        return products

    def create_reviews(self, count, users, products):
        reviews = []
        review_titles = [
            'منتج ممتاز', 'جودة عالية', 'سعر مناسب', 'أداء رائع', 'تصميم جميل',
            'منتج جيد', 'مقترح للشراء', 'منتج عادي', 'جودة متوسطة', 'سعر مرتفع'
        ]
        
        for i in range(count):
            review = Review.objects.create(
                product=random.choice(products),
                user=random.choice(users),
                rating=random.randint(1, 5),
                title=random.choice(review_titles),
                content=fake.text(max_nb_chars=300),
                is_approved=random.choice([True, True, True, False]),  # 75% موافق عليه
                helpful_votes=random.randint(0, 50),
                unhelpful_votes=random.randint(0, 10)
            )
            reviews.append(review)
            self.stdout.write(f'تم إنشاء المراجعة: {review.title}')
        
        return reviews

    def create_review_interactions(self, reviews, users):
        for review in reviews:
            # إنشاء 5-15 تفاعل لكل مراجعة
            for _ in range(random.randint(5, 15)):
                user = random.choice(users)
                # تجنب تكرار نفس المستخدم
                if not review.interactions.filter(user=user).exists():
                    ReviewInteraction.objects.create(
                        review=review,
                        user=user,
                        interaction_type=random.choice(['helpful', 'unhelpful'])
                    )
                    self.stdout.write(f'تم إنشاء تفاعل على: {review.title}')

    def create_comments(self, posts, users):
        for post in posts:
            # إنشاء 2-5 تعليقات لكل مقال
            for _ in range(random.randint(2, 5)):
                comment = Comment.objects.create(
                    post=post,
                    author=random.choice(users),
                    content=fake.text(max_nb_chars=200),
                    is_approved=random.choice([True, False])
                )
                self.stdout.write(f'تم إنشاء تعليق على: {post.title}')

    def create_favorites(self, posts, users):
        for user in users:
            # إضافة 3-8 مقالات للمفضلة لكل مستخدم
            favorite_posts = random.sample(posts, min(random.randint(3, 8), len(posts)))
            for post in favorite_posts:
                Favorite.objects.create(user=user, post=post)
                self.stdout.write(f'تم إضافة {post.title} إلى مفضلة {user.username}')

    def create_banned_words(self):
        banned_words = [
            'سيء', 'رديء', 'مخيب', 'مرفوض', 'أسوأ', 'غير مفيد', 'مخيب للآمال',
            'مخيب', 'مخيب', 'مخيب', 'مخيب', 'مخيب', 'مخيب', 'مخيب', 'مخيب'
        ]
        
        for word in banned_words:
            BannedWord.objects.get_or_create(word=word)
            self.stdout.write(f'تم إضافة الكلمة المحظورة: {word}')

    def create_notifications(self, users, reviews):
        for user in users:
            # إنشاء 2-5 إشعارات لكل مستخدم
            for _ in range(random.randint(2, 5)):
                review = random.choice(reviews)
                notification_type = random.choice([
                    'review_approved', 'review_rejected', 'product_update'
                ])
                
                if notification_type == 'review_approved':
                    title = 'تمت الموافقة على مراجعتك'
                    message = f'تمت الموافقة على مراجعتك للمنتج "{review.product.name}"'
                elif notification_type == 'review_rejected':
                    title = 'تم رفض مراجعتك'
                    message = f'تم رفض مراجعتك للمنتج "{review.product.name}"'
                else:
                    title = 'تحديث المنتج'
                    message = f'تم تحديث المنتج "{review.product.name}"'
                
                Notification.objects.create(
                    user=user,
                    notification_type=notification_type,
                    title=title,
                    message=message,
                    related_object_id=review.id
                )
                self.stdout.write(f'تم إنشاء إشعار لـ: {user.username}') 