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
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('instructor_dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('course/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('course/<int:course_id>/create_lecture/', views.create_lecture, name='create_lecture'),
    path('create_course/', views.create_course, name='create_course'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/add_question/', views.add_question, name='add_question'),
    path('question/<int:question_id>/add_answers/', views.add_answers, name='add_answers'),
]