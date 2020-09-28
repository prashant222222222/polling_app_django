
from django.urls import path, include
from main import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    #path('question/<int:pk>', views.Qusetion.as_view(), name="question"),
    path('question/<slug>', login_required(views.Question.as_view()), name="question"),

]
