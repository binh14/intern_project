from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, generics, exceptions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from leaveRequest.models import LeaveRequest
from leaveRequest.serializers import LeaveRequestSerializer, CreateLeaveRequestSerializers, GetDetailLeaveRequestSerializer
from shared.utils import format_response
from rest_framework.response import Response
from rest_framework.views import APIView


# class LeaveRequestView()

class ListCreateLeaveRequestView(ListCreateAPIView):
    model = LeaveRequest
    serializer_class = LeaveRequestSerializer
    def list(self, request, *args, **kwargs):
        leave_request = LeaveRequest.objects.filter() #filter: dk lay data
        serializer = LeaveRequestSerializer(leave_request, many = True)
        response = format_response(
            success=True,
            status = status.HTTP_200_OK,
            message = "Get succses",
            data = serializer.data
        )
        return Response(response, status = response.get('status'))

    def create(self, request, *args, **kwargs):
        serializer = LeaveRequestSerializer(data=request.data) #get data from body
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'message': 'Create a new LeaveRequest successful!'
            }, status=status.HTTP_201_CREATED)
        return JsonResponse({
            'message': 'Create a new LeaveRequest unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

class CreateLeaveRequestView(generics.CreateAPIView):

    serializer_class = CreateLeaveRequestSerializers
    def post(self, request, *args, **kwargs):
        data = request.data #body
        print("data: ")
        print(data) #json body
        print("request: ")
        print(request.user)
        print(LeaveRequest.objects.filter())
        serializer = CreateLeaveRequestSerializers(data = data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = format_response(
            success = True,
            status = status.HTTP_201_CREATED,
            message = "create success",
        )
        return Response(response, status=response.get('status'))

class GetUpdateDeleteLeaveRequestView(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, *args, **kwargs):
        id = kwargs.pop('leave_request_id')
        try:
            leave_request = LeaveRequest.objects.get(
                id = id,
                user = request.user
            )
            print("id:", id) #id leave request
            print("user:", request.user)
        except:
            raise exceptions.NotFound()
        serializer = GetDetailLeaveRequestSerializer(leave_request)
        response = format_response(
            success = True,
            status = status.HTTP_201_CREATED,
            message = "get success",
            data = serializer.data
        )
        print("serializer.data:")
        print(serializer.data)
        return Response(response, status=response.get('status'))