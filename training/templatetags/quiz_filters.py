from django import template

register = template.Library()

@register.filter
def filter_by_user(queryset, user):
    return queryset.filter(user=user).first()

@register.filter
def has_quiz_result(quiz, user):
    return quiz.quizresult_set.filter(user=user).exists()


@register.filter
def get_quiz_score(quiz, user):
    try:
        return quiz.quizresult_set.get(user=user).score
    except:
        return 0
