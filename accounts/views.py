from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User
from .serializers import UserSerializer


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """تسجيل مستخدم جديد"""
    data = request.data
    
    # التحقق من البيانات المطلوبة
    required_fields = ['username', 'email', 'password', 'password2']
    for field in required_fields:
        if field not in data:
            return Response(
                {'error': f'الحقل {field} مطلوب'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # التحقق من تطابق كلمات المرور
    if data['password'] != data['password2']:
        return Response(
            {'error': 'كلمات المرور غير متطابقة'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # التحقق من صحة كلمة المرور
    try:
        validate_password(data['password'])
    except ValidationError as e:
        return Response(
            {'error': e.messages[0]},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # التحقق من عدم وجود المستخدم
    if User.objects.filter(username=data['username']).exists():
        return Response(
            {'error': 'اسم المستخدم موجود مسبقاً'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(email=data['email']).exists():
        return Response(
            {'error': 'البريد الإلكتروني موجود مسبقاً'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # إنشاء المستخدم
    try:
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )
        
        # إنشاء tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'تم التسجيل بنجاح',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': 'حدث خطأ أثناء التسجيل'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    """تسجيل الدخول"""
    data = request.data
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'اسم المستخدم وكلمة المرور مطلوبان'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # التحقق من صحة البيانات
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response(
            {'error': 'بيانات الدخول غير صحيحة'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # إنشاء tokens
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'message': 'تم تسجيل الدخول بنجاح',
        'user': UserSerializer(user).data,
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile(request):
    """ملف المستخدم الشخصي"""
    return Response({
        'user': UserSerializer(request.user).data
    })


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    """تحديث ملف المستخدم الشخصي"""
    user = request.user
    data = request.data
    
    # تحديث البيانات المسموح بها
    allowed_fields = ['first_name', 'last_name', 'email', 'bio', 'phone']
    for field in allowed_fields:
        if field in data:
            setattr(user, field, data[field])
    
    # حفظ التغييرات
    user.save()
    
    return Response({
        'message': 'تم تحديث الملف الشخصي بنجاح',
        'user': UserSerializer(user).data
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    """تسجيل الخروج"""
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'message': 'تم تسجيل الخروج بنجاح'
        })
    except Exception:
        return Response({
            'message': 'تم تسجيل الخروج بنجاح'
        })
