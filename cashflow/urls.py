from django.urls import path

from . import views

app_name = "cashflow"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("categories", views.CategoriesView.as_view(), name="categories"),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    path("upload", views.simple_upload, name="simple_upload"),
]
