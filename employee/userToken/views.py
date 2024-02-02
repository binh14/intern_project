from rest_framework.response import Response
from rest_framework import status, generics, exceptions
from django.contrib.auth import authenticate
from shared.utils import format_response, random_with_N_digits
from user.models import User
from userToken.serializers import UserTokenSerializer, CreateUserTokenSerializers
from userToken.models import UserToken
from django.utils import timezone

class CheckView(generics.GenericAPIView):
    serializer_class = CreateUserTokenSerializers 

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user_type = serializer.validated_data['user_type']

        user = User.objects.filter(
            email=email,
            user_type=user_type
        )
        if user is None:
            response_data = format_response(
                success=False,
                status=status.HTTP_400_BAD_REQUEST,
                message=f"User does not exist with email {email}",
            )
            return Response(response_data, status=response_data.get('status'))
        else:
            number = random_with_N_digits(6)
            user_token = UserToken(
                user=user.first(),
                user_token_id="exnodes",
                code=number,
                experied=timezone.now() + timezone.timedelta(minutes=15)
            )
            print("user:", user_token.user)
            print("user_id_token:", user_token.user_token_id)
            print("code:", user_token.code) #random
            print("experied:", user_token.experied)
            print("timezone.now():", timezone.now())
            print("timezone.now():", timezone.timedelta(minutes=15))
        
        response_data = format_response(
            success=True,
            status=status.HTTP_200_OK,
            message="User exists.",
            data=serializer.data
        )

        return Response(response_data, status=response_data.get('status'))
