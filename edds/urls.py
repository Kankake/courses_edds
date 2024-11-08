from django.contrib import admin
from django.urls import path
from training import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registeration/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('settings/', views.user_settings, name='user_settings'),
    # Курсы
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('course/<int:course_id>/create_lecture/', views.create_lecture, name='create_lecture'),
    path('create_course/', views.create_course, name='create_course'),
    # Дэшборды
    path('', views.dashboard, name='dashboard'),
    path('users-progress/', views.users_progress, name='users_progress'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('instructor_dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    # Тесты
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:course_id>/add_quiz', views.add_quiz, name='add_quiz'),
    path('quiz/<int:quiz_id>/edit', views.edit_quiz, name='edit_quiz'),
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/add_question/', views.add_question, name='add_question'),
    path('question/<int:question_id>/add_answers/', views.add_answers, name='add_answers'),
    path('answer/<int:answer_id>/delete/', views.delete_answer, name='delete_answer'),
    path('question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('delete_quiz/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),
]
