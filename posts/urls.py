from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.list, name='list'),
    path('create/', views.create, name="create"),
    path('<int:id>/update/', views.update, name="update"),
    
]