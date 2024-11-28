
from django.shortcuts import get_object_or_404
from .utils import role_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from django.shortcuts import render, redirect
from .models import Course, Profile, Quiz, Question, Answer, QuizResult, LectureFile, Lecture, CourseVisit, QuizCompletion
from django.contrib.auth.decorators import login_required, instructor_course_required
from django.contrib.auth.models import User
from .forms import CourseForm, LectureForm, QuizForm, QuestionForm, AnswerForm, LectureFileForm
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.utils import timezone
from .models import Lecture, LectureVisit
from django.db.models import Count
import json

def anonymous_required(function=None):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('course_list')
        return function(request, *args, **kwargs)
    return wrapper

@login_required
@role_required('instructor', 'admin')
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    return render(request, 'training/edit_course.html', {'form': form, 'course': course})


@login_required
@role_required('instructor', 'admin')
@csrf_exempt
def upload_lecture_file(request, lecture_id):
    if request.method == 'POST':
        try:
            lecture = Lecture.objects.get(id=lecture_id)
            file = request.FILES.get('file')
            file_name = request.POST.get('file_name', file.name)

            if not file:
                return JsonResponse({'status': 'error', 'message': 'Файл не указан.'}, status=400)

            lecture_file = LectureFile.objects.create(
                lecture=lecture,
                file=file,
                name=file_name
            )
            lecture_file.save()

            return JsonResponse({'status': 'success', 'message': 'Файл успешно загружен.'})
        except Lecture.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Лекция не найдена.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Ошибка: {str(e)}'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Метод не разрешён.'}, status=405)


@login_required
@role_required('instructor', 'admin')
@csrf_exempt
def delete_lecture_file(request, file_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            file_id = data.get("file_id")

            if not file_id:
                return JsonResponse({"status": "error", "message": "ID файла не указан."}, status=400)

            file = LectureFile.objects.get(id=file_id)
            file.delete()
            return JsonResponse({"status": "success", "message": "Файл удалён."})
        except LectureFile.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Файл не найден."}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Метод не разрешён."}, status=405)


@login_required
def user_settings(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        
        new_password = request.POST.get('new_password')
        if new_password:
            user.set_password(new_password)
            
        user.save()
        messages.success(request, 'Настройки успешно сохранены')
        return redirect('dashboard')
        
    return render(request, 'registration/user_settings.html')

@anonymous_required
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('course_list')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'registration/login.html')

@login_required
def submit_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        total_score = 0
        total_questions = quiz.questions.count()

        for question in quiz.questions.all():
            answer_text = request.POST.get(f'question_{question.id}')
            if answer_text:
                correct_answer = question.answers.filter(is_correct=True).first()
                if correct_answer and answer_text == correct_answer.text:
                    total_score += 1

        if total_questions > 0:
            percentage_score = (total_score / total_questions) * 100
            QuizResult.objects.create(
                user=request.user,
                quiz=quiz,
                score=percentage_score
            )
            return JsonResponse({
                'status': 'success',
                'score': f'{percentage_score:.1f}%'
            })
        
        return JsonResponse({
            'status': 'error',
            'message': 'В тесте нет вопросов'
        })


def calculate_quiz_score(quiz, answers):
    score = 0
    for question in quiz.questions.all():
        if question.id in answers and answers[question.id] == question.correct_answer:
            score += 1
    return score


@login_required
@role_required('instructor', 'admin')
def add_quiz(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = QuizForm()

    return render(request, 'quiz/add_quiz.html', {'form': form, 'course': course})

@login_required
@role_required('instructor', 'admin')
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('course_detail', course_id=quiz.course.id)
    else:
        form = QuizForm(instance=quiz)

    return render(request, 'quiz/edit_quiz.html', {'form': form, 'quiz': quiz})

@login_required
def delete_answer(answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    quiz_id = answer.question.quiz.id
    answer.delete()
    return redirect('edit_quiz', quiz_id=quiz_id)

@login_required
def delete_question(question_id):
    question = get_object_or_404(Question, id=question_id)
    quiz_id = question.quiz.id
    question.delete()
    return redirect('edit_quiz', quiz_id=quiz_id)


@login_required
@role_required('instructor', 'admin')
def add_answers(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.question = question
            answer.save()

            return redirect('add_answers', question_id=question.id)
    else:
        answer_form = AnswerForm()

    return render(request, 'quiz/add_answer.html', {'question': question, 'answer_form': answer_form})

@login_required
@role_required('instructor', 'admin')
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
@role_required('instructor', 'admin')
def create_quiz(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save()

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
        
        # Record completion
        QuizCompletion.objects.create(
            quiz=quiz,
            user=request.user,
            score=percentage_score
        )
        
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
@role_required('instructor', 'admin')
def instructor_dashboard(request):
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'training/instructor_dashboard.html', {"courses": courses})

@login_required
@role_required('instructor', 'admin')
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('course_detail', course.id)
    else:
        form = CourseForm()
    return render(request, 'training/create_course.html', {'form': form})


@login_required
def dashboard(request):
    from django.db.models import Count, Min

    user = request.user
    profile = request.user.profile
    courses = Course.objects.all()
    user_results = QuizResult.objects.filter(user=user)
    progress_data = {result.quiz.id: result.score for result in user_results}

    courses = Course.objects.annotate(
        total_visits=Count('coursevisit'),
        unique_visitors=Count('coursevisit__user', distinct=True)
    ).prefetch_related('coursevisit_set')
    
    course_visitors = CourseVisit.objects.values(
        'course__title', 
        'user__username'
    ).distinct()
    
    unique_visits = CourseVisit.objects.select_related('course', 'user').values(
            'course__title', 
            'user__username'
        ).annotate(
            first_visit=Min('visit_date')
        ).order_by('course__title', 'user__username')
    context = {
        'user': user,
        'total_visits': CourseVisit.objects.count(),
        'profile': profile,
        'courses': courses,
        'progress_data': progress_data,
        'course_visits': course_visitors,
        'unique_visits': unique_visits,
        'instructor_courses': Course.objects.filter(instructor=request.user)
    }

    return render(request, 'training/dashboard.html', context)


@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'training/course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    profile = request.user.profile 
    lectures = course.lectures.all() 

    CourseVisit.objects.create(
        course=course,
        user=request.user
    )

    context = {
        'course': course,
        'lectures': lectures,
        'profile': profile,
    }
    return render(request, 'training/course_detail.html', context)

@role_required('admin', 'instructor')
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    course_id = quiz.course.id
    quiz.delete()
    return redirect('course_detail', course_id=course_id)

@anonymous_required
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
@role_required('admin')
def users_progress(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'training/user_progress.html', context)

@login_required
@instructor_course_required
def edit_lecture(request,course_id, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    course_id = lecture.course.id
    if request.method == 'POST':
        form = LectureForm(request.POST, instance=lecture)
        if form.is_valid():
            lecture = form.save()
            return redirect('course_detail', course_id=lecture.course.id)
    else:
        form = LectureForm(instance=lecture)
    return render(request, 'training/edit_lecture.html', {
        'form': form,
        'lecture': lecture,
        'course_id': lecture.course.id
    })


@login_required
@instructor_course_required
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

def lecture_detail(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    # Create visit record
    LectureVisit.objects.create(
        lecture=lecture,
        user=request.user
    )
    visit_count = LectureVisit.objects.filter(lecture=lecture).count()
    # Rest of your view logic
