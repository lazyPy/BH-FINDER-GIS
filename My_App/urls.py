from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.registerUser, name='register-page'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('login-admin/', views.loginAdmin, name='login-admin-page'),
    path('login/', views.loginUser, name='login-page'),
    path('logout/', views.logoutUser, name='logout-page'),

    path('', views.userPage, name='user-page'),
    path('admin-page', views.adminPage, name='admin-page'),
    path('boarding-house-owner/', views.ownerPage, name='bh-owner'),

    path('<str:pk>/admin-boarding-house-detail/', views.adminBHDetail, name='admin-bh-detail'),
    path('<str:pk>/boarding-house-detail/', views.bhDetail, name='bh-detail'),

    path('add-boarding-house/', views.addBH, name='add-bh'),
    path('<str:pk>/edit-boarding-house/', views.editBH, name='edit-bh'),
    path('<str:pk>/update-boarding-house/', views.updateBH, name='update-bh'),
    path('<str:pk>/delete-boarding-house/', views.deleteBH, name='delete-bh'),
]
