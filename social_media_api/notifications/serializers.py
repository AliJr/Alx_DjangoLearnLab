from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from notifications.models import Notification
from .serializers import NotificationSerializer

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get unread notifications for the current user
        notifications = Notification.objects.filter(recipient=request.user, read=False)

        # Mark notifications as read
        notifications.update(read=True)

        # Serialize and return notifications
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
