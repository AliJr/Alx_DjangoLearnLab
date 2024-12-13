from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from psycopg2 import Timestamp
# Create your models here.
class Notification(models.Model):
    recipient = models.ForeignKey('accounts.User',related_name='recipient', on_delete=models.CASCADE)
    actor = models.ForeignKey('accounts.User',related_name='actor', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
# For generic relations to post, comment, or follow actions
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.actor.username} {self.verb} {self.target}"
    
    class Meta:
        ordering = ['-timestamp']