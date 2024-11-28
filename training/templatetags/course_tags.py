from django import template

register = template.Library()

@register.filter
def quiz_completion_count(quiz_set):
    total_completions = 0
    for quiz in quiz_set:
        total_completions += quiz.quizcompletion_set.count()
    return total_completions

@register.filter
def quiz_average_score(quizzes):
    total_score = 0
    completed_count = 0
    for quiz in quizzes:
        quiz_attempts = quiz.quizattempt_set.all()
        if quiz_attempts:
            total_score += sum(attempt.score for attempt in quiz_attempts)
            completed_count += quiz_attempts.count()
    
    # Add return statement to calculate average
    return total_score / completed_count if completed_count > 0 else 0

@register.filter
def total_course_attempts(course):
    total = 0
    for quiz in course.quizzes.all():
        total += quiz.attempts.count()
    return total


@register.filter
def count_quizzes(course):
    return course.quizzes.count()

@register.filter
def count_attempts(quiz):
    return quiz.attempts.count()


@register.filter
def quiz_completion_count(quizzes):
    return sum(quiz.quizattempt_set.count() for quiz in quizzes)
