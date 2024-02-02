from django.forms import ValidationError
from rest_framework  import serializers
from django.core.validators import RegexValidator, MaxLengthValidator, MinLengthValidator
from user.enum import UserType
from user.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password','first_name','last_name','email','phone_number')

class EmailValidator(RegexValidator):
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' #{2,}  means that the domain must have at least two characters
    message = 'Invalid email format'

class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("style", {}) #thiết lập thuọc tính style là 1 dict 
        kwargs["style"]["input_type"] = "password" #đầu vào là pw
        kwargs["write_only"] = True #ko trả về
        kwargs["validators"] = [MinLengthValidator(8), MaxLengthValidator(100)]
        super().__init__(*args, **kwargs) #gọi phương thức lớp cha để hoàn thành việc khởi tạo
class CustomTokenObtainSerializer(serializers.Serializer):
    # contructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Thêm các trường vào serializer
        self.fields["email"] = serializers.CharField(
            required=True,
            validators=[MinLengthValidator(2), MaxLengthValidator(150)]
        )
        self.fields["password"] = PasswordField()
        self.fields['user_type'] = serializers.ChoiceField(
            choices=UserType.choices
        )
        #chua hieu
    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        # RefreshToken.set_exp()
        # Add custom claims
        token['username'] = user.username
        token['user_type'] = user.user_type
        return token
    default_error_messages = {
        "no_active_account": "No active account found with the given credentials"
    }
    def authenticate(self, login_field=None, password=None, user_type=None):
        try:
            user = get_user_model().objects.get( #lấy user hiện tại
                email=login_field,
                user_type=user_type
            )
        except User.DoesNotExist:
            return
        if user.check_password(password):
            return user
    def validate(self, attrs):
        email = attrs.get('email')
        user_type = attrs.get('user_type')
        user = self.authenticate(
           
            login_field=email, password=attrs["password"], user_type=user_type
        )
        if user is None:
            raise exceptions.AuthenticationFailed()
        data = {}
        # Check first time
        refresh_token: RefreshToken = self.get_token(user)
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)
        access_token = str(refresh_token.access_token)
        refresh_token = str(refresh_token)
        # organ = OrganizationUser.objects.prefetch_related(
        #     'organization').filter(user=user)
        # list_organ = list(organ)
        data['access_token'] = access_token
        data['refresh_token'] = refresh_token
        data['info'] = {
            'id': user.id,
            'phone_number': user.phone_number,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': user.user_type,
        }
        # if user.user_type != UserType.ADMIN:
        #     data['organization_owner'] = format_organ(list_organ, True)
        #     data['organization_ref'] = format_organ(list_organ, None)
        return data
class CreateUserSerializers(serializers.Serializer):

    username = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(limit_value=3),
            RegexValidator(
                regex=r'^\w+$',
                message='Username must contain only letters, numbers, and underscores'
            )
        ]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[
            MinLengthValidator(limit_value=8),
            RegexValidator(
                regex=r'^(?=.*[\w@$!%*?&#_])(?=.*[A-Z])[A-Za-z\d@$!%*?&#_]+$',
                message='Password must contain at least one special character and start with an uppercase letter'
            )
        ]
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(
        required=True,
        max_length=11,
        validators=[
            MinLengthValidator(limit_value=10),
            RegexValidator(regex=r'^\d+$', message='Phone number must contain only digits')
        ]
    )
    email = serializers.EmailField(
        required=True,
        max_length=64,
        validators=[
            MinLengthValidator(limit_value=8),
            EmailValidator(),
            UniqueValidator(queryset=User.objects.all(), message='Email is unique')
        ]
    )
    user_type = serializers.ChoiceField(
        # required=True,
        choices=UserType.choices
    )

    def validate_email(self, value):
        # Kiểm tra có ký tự '@' xuất hiện giữa username và domain
        if '@' not in value:
            raise ValidationError('The email must contain "@" between username and domain.')

        # Tách username và domain
        username, domain = value.split('@', 1)

        # Kiểm tra username có độ dài từ 1 đến 64 ký tự
        if not (1 <= len(username) <= 64):
            raise ValidationError('Username must be between 1 and 64 characters.')

        # Kiểm tra định dạng của username
        username_validator = RegexValidator(
            regex=r'^[\w@$!%*?&#_]+$',
            message='Username must contain only letters, numbers, and special characters @$!%*?&'
        )
        username_validator(username)

        # Kiểm tra định dạng của domain
        domain_validator = RegexValidator(
            regex=r'^[A-Za-z0-9.-]+$',
            message='Invalid domain format'
        )
        domain_validator(domain)

        return value

    def save(self):
        user = User(
            username=self.validated_data.get('username'),
            first_name=self.validated_data.get('first_name'),
            last_name=self.validated_data.get('last_name'),
            phone_number=self.validated_data.get('phone_number'),
            email=self.validated_data.get('email'),
            user_type=self.validated_data.get('user_type'),
        )
        user.set_password(self.validated_data.get('password'))
        user.save()
        return user