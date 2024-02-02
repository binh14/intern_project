from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from user.models import User
from user.serializers import UserSerializer, CustomTokenObtainSerializer, CreateUserSerializers
from shared.utils import format_response
from rest_framework.response import Response
class ListCreateUserView(ListCreateAPIView):
    model = User
    serializer_class = UserSerializer
    def list(self, request, *args, **kwargs):
        users = User.objects.filter()
        serializer = UserSerializer(users, many = True)
        response = format_response(
            success=True,
            status = status.HTTP_200_OK,
            message = "Get succses",
            data = serializer.data
        )
        return Response(response, status = response.get('status'))
    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data) #get data from body
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'message': 'Create a new User successful!'
            }, status=status.HTTP_201_CREATED)
        return JsonResponse({
            'message': 'Create a new User unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)
class UpdateDeleteUserView(RetrieveUpdateDestroyAPIView):
    model = User
    serializer_class = UserSerializer
    def put(self, request, *args, **kwargs):
        User = get_object_or_404(User, id=kwargs.get('pk'))
        serializer = UserSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'message': 'Update User successful!'
            }, status=status.HTTP_200_OK)
        return JsonResponse({
            'message': 'Update User unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs.get('pk'))
        user.delete()
        return JsonResponse({
            'message': 'Delete User successful!'
        }, status=status.HTTP_200_OK)
class LoginView(generics.CreateAPIView):
    serializer_class = CustomTokenObtainSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializers = self.get_serializer(data = data)
        serializers.is_valid(raise_exception=True)
        response = format_response(
            success = True,
            status = status.HTTP_201_CREATED,
            message = "Login success",
            data = serializers.validated_data
        )
        return Response(response, status=response.get('status'))
class LogoutView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        response = format_response(
            success=True,
            status=status.HTTP_200_OK,
            message="Logout success",
            data={}
        )
        return Response(response, status=response.get('status'))
class CreateUserView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CreateUserSerializers(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = format_response(
            success = True,
            status = status.HTTP_201_CREATED,
            message = "create success",
        )
        return Response(response, status=response.get('status'))