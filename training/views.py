
from .models import Course
from django.shortcuts import get_object_or_404
from .utils import role_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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

