from django import template
from training.models import QuizResult

register = template.Library()

@register.filter
def filter_by_user(queryset, user):
    return queryset.filter(user=user).first()


@register.filter
def has_quiz_result(quiz, user):
    return QuizResult.objects.filter(quiz=quiz, user=user).exists()


@register.filter
def get_quiz_score(quiz, user):
    result = QuizResult.objects.filter(quiz=quiz, user=user).first()
    if result:
        return f"{result.score:.1f}%"
    return "0%"

