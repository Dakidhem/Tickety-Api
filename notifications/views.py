from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notification

# Create your views here.
class NotificationsView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user  # Assuming the user is authenticated
        notifications = Notification.objects.filter(recipient=user)
        serialized_notifications = [{'id': notification.id, 'message': notification.message, 'is_read': notification.is_read} for notification in notifications]
        return Response(serialized_notifications, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user  # Assuming the user is authenticated
        Notification.objects.filter(recipient=user).update(is_read=True)
        return Response({'message': 'Notifications marked as seen.'}, status=status.HTTP_200_OK)