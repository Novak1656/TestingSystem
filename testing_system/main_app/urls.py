from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import index, TestCreateView, QuestionsCreateView, AnswersCreateView

urlpatterns = [
    path('', index, name='main'),
    path('test/create/step1/', login_required(TestCreateView.as_view()), name='test_create'),
    path('test/create/step2/', login_required(QuestionsCreateView.as_view()), name='quest_create'),
    path('test/create/step3/', login_required(AnswersCreateView.as_view()), name='answer_create'),
]
