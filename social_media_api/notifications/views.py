from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
        notifications_data = [
            {
                'actor': notification.actor.username,
                'verb': notification.verb,
                'target': str(notification.target),
                'timestamp': notification.timestamp,
                'is_read': notification.is_read,
            }
            for notification in notifications
        ]
        return Response(notifications_data)

class MarkAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, recipient=request.user)
        except Notification.DoesNotExist:
            return Response({"detail": "Notification not found."}, status=404)

        notification.is_read = True
        notification.save()

        return Response({"detail": "Notification marked as read."})
