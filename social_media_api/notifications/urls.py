from django.urls import path
from .views import NotificationListView, MarkAsReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification_list'),
    path('read/<int:notification_id>/', MarkAsReadView.as_view(), name='mark_as_read'),
]
