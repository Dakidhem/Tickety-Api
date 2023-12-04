from django.db import models

class Ticket(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    assigned_to = models.ForeignKey('authentification.CustomUser', blank=True, null=True, on_delete=models.CASCADE, related_name='assigned_tickets')
    created_by = models.ForeignKey('authentification.CustomUser', on_delete=models.CASCADE, related_name='created_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    finished= models.BooleanField(default=False)