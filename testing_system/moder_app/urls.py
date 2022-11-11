from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import ModerPanelView, ModerTestCategoriesView, test_category_delete

urlpatterns = [
    path('', login_required(ModerPanelView.as_view()), name='moder_panel'),

    path('categories/', login_required(ModerTestCategoriesView.as_view()), name='moder_categories'),
    path('categories/delete/', test_category_delete, name='category_delete'),

]
