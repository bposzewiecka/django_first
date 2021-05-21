
from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('name_form', views.get_name, name='name_form'),
    path('contact_form', views.get_contact, name='contact_form'),
    path('question_create', views.question_create, name='question_create'),
    path('question_edit/<int:question_id>', views.question_edit, name='question_edit'),
    path('question_delete/<int:question_id>', views.question_delete, name='question_delete'),
]