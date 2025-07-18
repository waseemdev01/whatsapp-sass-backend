from rest_framework import generics, permissions
from .models import Customer, MessageTemplate, ScheduledMessage
from .serializers import (
    RegisterSerializer, UserSerializer, CustomerSerializer,
    MessageTemplateSerializer, ScheduledMessageSerializer
)
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# from .models import Customer, MessageTemplate
from .utils import send_whatsapp_message

User = get_user_model()

# Registration view
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# Profile view
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# CRUD: Customers
class CustomerListCreate(generics.ListCreateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

# CRUD: Templates
class TemplateListCreate(generics.ListCreateAPIView):
    serializer_class = MessageTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MessageTemplate.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Schedule messages
class ScheduleMessageCreate(generics.CreateAPIView):
    serializer_class = ScheduledMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        customer_id = request.data.get("customer_id")
        template_id = request.data.get("template_id")
        context = request.data.get("context", {})

        try:
            customer = Customer.objects.get(id=customer_id, user=request.user)
            template = MessageTemplate.objects.get(id=template_id, user=request.user)
        except (Customer.DoesNotExist, MessageTemplate.DoesNotExist):
            return Response({"error": "Invalid customer or template"}, status=400)

        try:
            message_id = send_whatsapp_message(customer.phone, template.content, context)
            return Response({"success": True, "message_id": message_id})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
