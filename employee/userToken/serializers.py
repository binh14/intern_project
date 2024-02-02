from rest_framework import serializers
from .models import UserToken
from userToken.models import UserToken
from user.models import User
from user.serializers import CustomTokenObtainSerializer, EmailValidator, CreateUserSerializers
from user.enum import UserType

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToken
        fields = ('user', 'user_token_id', 'code', 'experied')

class CreateUserTokenSerializers(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[EmailValidator()]
    )

    user_type = serializers.ChoiceField(
        required=True,
        choices=UserType.choices
    )
    
    def validate(self, data):
        email = data.get('email')
        user_type = data.get('user_type')

        if not User.objects.filter(email=email, user_type=user_type).exists():
            raise serializers.ValidationError("User with email and user_type does not exist.")
        
        return data
