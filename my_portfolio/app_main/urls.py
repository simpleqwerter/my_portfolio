
from django.urls import path
from app_main.views import homepage, skillbox_lessons, update_lessons_info


urlpatterns = [
    path('', homepage,  name='homepage'),
    path('skillbox_lessons',  skillbox_lessons, name='skillbox_lessons'),
    path('update_lessons_info', update_lessons_info, name='update_lessons_info'),


]
