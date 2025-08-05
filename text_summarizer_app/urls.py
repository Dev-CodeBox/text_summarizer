from django.urls import path
from . import views

urlpatterns = [
    path("summarize_text/", views.summarize_text, name="summarize_text"),
]
