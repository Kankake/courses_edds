
from .models import Course
from django.shortcuts import get_object_or_404
from .utils import role_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import Course, Lecture, Test, Profile, Quiz, Answer, Question, Answer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CourseForm, LectureForm, QuizForm, QuestionForm, AnswerForm

@login_required
@role_required('admin')
def add_answers(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.question = question
            answer.save()

            # Перенаправляем обратно к добавлению ответов, чтобы можно было добавить несколько вариантов
            return redirect('add_answers', question_id=question.id)
    else:
        answer_form = AnswerForm()

    return render(request, 'quiz/add_answer.html', {'question': question, 'answer_form': answer_form})

@login_required
@role_required('admin') 
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()
            
            return redirect('add_answers', question_id=question.id)
    else:
        question_form = QuestionForm()

    return render(request, 'quiz/add_question.html', {'quiz': quiz, 'question_form': question_form})

@login_required
@role_required('admin')  # Или укажи 'instructor' если инструкторам разрешено создавать тесты
def create_quiz(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save()

            # Редирект на страницу добавления вопросов к созданному тесту
            return redirect('add_question', quiz_id=quiz.id)
    else:
        quiz_form = QuizForm()

    return render(request, 'quiz/create_quiz.html', {'quiz_form': quiz_form})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        score = 0
        total_questions = quiz.questions.count()
        
        for question in quiz.questions.all():
            selected_answer_id = request.POST.get(str(question.id))
            if selected_answer_id:
                selected_answer = Answer.objects.get(id=selected_answer_id)
                if selected_answer.is_correct:
                    score += 1

        percentage_score = (score / total_questions) * 100
        return render(request, 'quiz/quiz_result.html', {
            'quiz': quiz,
            'score': score,
            'total_questions': total_questions,
            'percentage_score': percentage_score
        })

    return render(request, 'quiz/take_quiz.html', {'quiz': quiz})

@login_required
@role_required('admin')
def admin_dashboard(request):
    courses = Course.objects.all()
    users = Profile.objects.all()
    return render(request, 'training/admin_dashboard.html', {"courses": courses, "users": users})

@login_required
@role_required('instructor')
def instructor_dashboard(request):
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'training/instructor_dashboard.html', {"courses": courses})

@login_required
@role_required('admin')
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CourseForm()
    return render(request, 'training/create_course.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    profile = request.user.profile
    courses = Course.objects.filter()
    context = {
                'user': user,
                'profile': profile,
                'courses': courses
            }
    return render(request, 'training/dashboard.html', context)


@role_required('instructor')
def instructor_dashboard(request):
    courses = Course.objects.all()
    return render(request, 'training/instructor_dashboard.html', {'courses': courses})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'training/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lectures = course.lectures.all()
    return render(request, 'training/course_detail.html', {'course': course, 'lectures': lectures})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('course_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@role_required('admin')
def users_progress(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'training/user_progress.html', context)

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Возвращаемся на панель администратора после сохранения
    else:
        form = CourseForm(instance=course)
    return render(request, 'training/edit_course.html', {'form': form})

def create_lecture(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = LectureForm(request.POST)
        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.course = course  # Привязываем лекцию к курсу
            lecture.save()
            return redirect('instructor_dashboard')  # Перенаправление на панель инструктора
    else:
        form = LectureForm()
    return render(request, 'training/create_lecture.html', {'form': form, 'course': course})