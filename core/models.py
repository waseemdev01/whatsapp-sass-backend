from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    business_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True)
    plan_type = models.CharField(max_length=50, default='free')

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    tags = models.JSONField(default=list)

class MessageTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    content = models.TextField()  # e.g. "Hello {name}, your order is ready."

class ScheduledMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    template = models.ForeignKey(MessageTemplate, on_delete=models.SET_NULL, null=True)
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=20, default='pending')
    sent_at = models.DateTimeField(null=True, blank=True)
    delivery_status = models.CharField(max_length=20, null=True, blank=True)
