from django.urls import path
from .views import (
    UserRegisterViewAPIView,
    VerifyEmailAPIView,
    LoginAPIView,    
    TodoAddAPIView, 
    TodoAPIView, 
    TodoUpdateAPIView,   
    DeleteCustomerAPIView
    )

urlpatterns = [
    path('register', UserRegisterViewAPIView.as_view()),
    path('verify_email', VerifyEmailAPIView.as_view(), name='verify_email'),
    path('login', LoginAPIView.as_view(), name='user_login'),
    path('add_todo', TodoAddAPIView.as_view(), name='add_todo'),
    path('update_todo', TodoUpdateAPIView.as_view(), name='update_todo'),
    path('update_todo', DeleteCustomerAPIView.as_view(), name='update_todo'),
    path('todo', TodoAPIView.as_view(), name='get_todo'),
    
    ]
