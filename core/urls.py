from django.urls import path
from .views import (
    RegisterView, ProfileView, CustomerListCreate, CustomerDetail,
    TemplateListCreate, ScheduleMessageCreate,SendMessageView
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("customers/", CustomerListCreate.as_view()),
    path("customers/<int:pk>/", CustomerDetail.as_view()),
    path("templates/", TemplateListCreate.as_view()),
    path("schedule/", ScheduleMessageCreate.as_view()),
    path("send/", SendMessageView.as_view(), name="send-message"),

]
