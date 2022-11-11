from django.contrib import admin
from .models import Category, Tag, TestAnswers, TestQuestions, Test, TestResults


@admin.register(Category, Tag)
class CatTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'title', 'created_at']
    list_display_links = ['id', 'slug']
    list_filter = ['created_at']
    search_fields = ['title']
    save_as = True


@admin.register(TestAnswers)
class TestAnswersAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'answer', 'is_right']
    list_display_links = ['id', 'question']
    list_filter = ['is_right']
    search_fields = ['answer']
    save_as = True


@admin.register(TestQuestions)
class TestQuestionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'test', 'question', 'image', 'answers_type']
    list_display_links = ['id', 'test']
    list_filter = ['answers_type']
    search_fields = ['question']
    save_as = True


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title', 'author', 'category', 'passed_times', 'is_published', 'published_at', 'created_at']
    list_display_links = ['slug']
    list_filter = ['author', 'category', 'is_published']
    search_fields = ['title']
    save_as = True


@admin.register(TestResults)
class TestResultsAdmin(admin.ModelAdmin):
    list_display = ['id', 'test', 'user', 'score', 'completed_at']
    list_display_links = ['id', 'test']
    list_filter = ['score']
    search_fields = ['test', 'user']
    save_as = True
