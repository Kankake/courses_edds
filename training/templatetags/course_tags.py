from django import template

register = template.Library()

@register.filter
def quiz_completion_count(quiz_set):
    total_completions = 0
    for quiz in quiz_set:
        total_completions += quiz.quizcompletion_set.count()
    return total_completions
