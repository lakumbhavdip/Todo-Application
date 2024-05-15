from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'todoapp'

urlpatterns = [
    path('index', views.tododetails, name='index'),
    path('', views.register, name='register'),
    path('login', views.login, name='login'),
    path('save_todo', views.save_todo, name='save_todo'),
    
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('edit/<int:todo_id>/', views.edit_todo, name='edit_todo'),
    path('logout/', views.logout_view, name='logout'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



