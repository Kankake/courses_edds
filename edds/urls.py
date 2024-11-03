from django.contrib import admin
from django.urls import path
from training import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users-progress/', views.users_progress, name='users_progress'),
]

