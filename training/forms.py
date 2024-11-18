from django import forms
from .models import Course, Lecture, Quiz, Question, Answer, LectureFile

class LectureFileForm(forms.ModelForm):
    class Meta:
        model = LectureFile
        fields = ['name', 'file']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']  # Указываем поля, которые будут в форме
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название курса'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание курса'}),
        }

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['title', 'content']  # Поля для заполнения
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название лекции'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Содержание лекции'}),
        }


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название теста'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        question = forms.CharField()

        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Текст вопроса'}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Вариант ответа'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }