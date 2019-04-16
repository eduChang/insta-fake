from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    
    path('user_page/<int:id>/', views.user_page, name="user_page" ),
    path('edit_profile/<int:id>/', views.edit_profile, name="edit_profile"),
    
    path('follow/<int:id>/', views.follow, name="follow"),
]