from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import (TestCreateView, QuestionsCreateView, AnswersCreateView, TestsListView, TestDetailView,
                    testing_finishing_view, TestingBeginningView)

urlpatterns = [
    path('', TestsListView.as_view(), name='main'),
    path('test/create/step1/', login_required(TestCreateView.as_view()), name='test_create'),
    path('test/create/step2/', login_required(QuestionsCreateView.as_view()), name='quest_create'),
    path('test/create/step3/', login_required(AnswersCreateView.as_view()), name='answer_create'),

    path('tests/<str:slug>/', login_required(TestDetailView.as_view()), name='test_detail'),

    path('tests/start/<int:test_pk>/', login_required(TestingBeginningView.as_view()), name='test_start'),
    path('tests/finish/<int:test_pk>/', testing_finishing_view, name='test_finish'),
]
