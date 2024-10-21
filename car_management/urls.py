from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from cars import views
from cars import views as car_views

router = DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('', views.CarListView.as_view(), name='car_list'),  
    path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),  
    path('cars/new/', views.CarCreateView.as_view(), name='car_create'), 
    path('cars/<int:pk>/edit/', views.CarUpdateView.as_view(), name='car_edit'),  
    path('cars/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete'), 
    path('cars/<int:pk>/comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('register/', car_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),  
    path('logout/', car_views.CustomLogoutView.as_view(), name='logout'),
]
 