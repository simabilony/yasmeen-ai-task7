from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from blog.models import Category, Post, Comment, Favorite
from faker import Faker
import random

User = get_user_model()
fake = Faker(['ar_SA'])


class Command(BaseCommand):
    help = 'إنشاء بيانات تجريبية للمدونة'

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

    def handle(self, *args, **options):
        self.stdout.write('بدء إنشاء البيانات التجريبية...')
        
        # إنشاء التصنيفات
        categories = self.create_categories(options['categories'])
        
        # إنشاء المستخدمين
        users = self.create_users(options['users'])
        
        # إنشاء المقالات
        posts = self.create_posts(options['posts'], users, categories)
        
        # إنشاء التعليقات
        self.create_comments(posts, users)
        
        # إنشاء المفضلات
        self.create_favorites(posts, users)
        
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