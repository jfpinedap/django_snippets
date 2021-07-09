"""Snippet URLS"""

# Dajngo imports
from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

# App imports
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(template_name = "login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path(
        'snippets/language/<slug:lang_slug>/',
        views.SnippetByLangView.as_view(),
        name='language'
    ),
    path(
        'snippets/user/<username>/',
        views.SnippetByUserView.as_view(),
        name='user_snippets'
    ),
    path('snippets/snippet/<int:pk>', views.SnippetDetailView.as_view(), name='snippet'),
    path(
        'snippets/add/',
        views.SnippetAddView.as_view(success_url=reverse_lazy('index')),
        name='snippet_add'
    ),
    path(
        'snippets/<int:pk>/edit/',
        views.SnippetEditView.as_view(success_url=reverse_lazy('index')),
        name='snippet_edit'
    ),
    path(
        'snippets/<int:pk>/delete/',
        views.SnippetDeleteView.as_view(success_url=reverse_lazy('index')),
        name='snippet_delete'
    ),
]
