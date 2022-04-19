from django.shortcuts import render
from app_main.parser_skillbox import Parser
from app_main.models import Lesson, Theme
from django.http import HttpResponseRedirect
from django.contrib import messages


# Create your views here.
def homepage(request):
    return render(request, 'app_main/portfolio.html', {})


def skillbox_lessons(request):
    themes = Theme.objects.all()
    all_lessons = {}
    for theme in themes:
        lessons = Lesson.objects.filter(theme=theme)
        all_lessons[theme.name] = [(f'{lesson.name}', f'{lesson.status}') for lesson in lessons]
    print(all_lessons)
    return render(request, 'app_main/skillbox_lessons.html', {'lessons': all_lessons})


def update_lessons_info(request):
    parser = Parser()
    lessons = parser.go()
    for theme in lessons:
        t = Theme(name=theme)
        t.save()
        for lesson in lessons[theme]:
            status = True if lesson[1] else False
            l = Lesson(theme=t, name=lesson[0], status=status)
            l.save()
    messages.info(request, 'updated')
    return HttpResponseRedirect(request.META.HTTP_REFERER)


