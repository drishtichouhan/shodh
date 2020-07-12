from django.urls import path

from . import views

urlpatterns = [
  # /
  # path('', views.home, name='home'),
  # TEMPORARY
  path('signins', views.sign_in_s, name='signins'),
  path('signinp', views.sign_in_p, name='signinp'),
  path('callback', views.callback, name='callback'),
  path('signout', views.sign_out, name='signout'),
  path('calendar', views.calendar, name='calendar'),
  path('createvacancy', views.create_vacancy, name='createvacancy'),
  path('deletevacancy/<int:id>/', views.delete_vacancy, name='deletevacancy'),
  path('togglevacancy/<int:id>/', views.toggle_vacancy, name='togglevacancy'),
]
