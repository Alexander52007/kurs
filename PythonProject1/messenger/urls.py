from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='messenger/login.html',
        authentication_form=CustomAuthenticationForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('chats/', views.chats, name='chats'),
    path('chats/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('chats/create/<int:user_id>/', views.create_chat, name='create_chat'),

    path('profile/', views.profile, name='profile'),
]