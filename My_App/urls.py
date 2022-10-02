from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.homePage, name='home'),
    path('admin-home', views.adminPage, name='admin-page'),
    path('<str:pk>/my-boarding-house/', views.myBh, name='my-bh'),
    path('<str:pk>/boarding-house-detail/', views.bhDetail, name='bh-detail'),

    path('add-boarding-house/', views.addBH, name='add-bh'),
    path('<str:pk>/delete-boarding-house/', views.deleteBH, name='delete-bh'),
    path('<str:pk>/edit-boarding-house/', views.editBH, name='edit-bh'),
    path('<str:pk>/update-boarding-house/', views.updateBH, name='update-bh'),

    path('<str:pk>/admin-bh-detail/', views.adminBHDetail, name='admin-bh-detail'),
]
