import re
from .models import Notification
from . serializers import NotificationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class NotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # get unread notifications order by timestamp
        notifications = Notification.objects.filter(recipient=request.user, read=False).order_by('-timestamp')
        notifications.update(read=True) #mark notifications as read
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)