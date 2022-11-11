from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import ModerPanelView, ModerTestCategoriesView, test_category_delete, ModerTestTagsView, test_tag_delete

urlpatterns = [
    path('', login_required(ModerPanelView.as_view()), name='moder_panel'),

    path('categories/', login_required(ModerTestCategoriesView.as_view()), name='moder_categories'),
    path('categories/delete/', test_category_delete, name='category_delete'),

    path('tags/', login_required(ModerTestTagsView.as_view()), name='moder_tags'),
    path('tags/delete/', test_tag_delete, name='tag_delete'),

]
