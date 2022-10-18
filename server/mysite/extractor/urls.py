from django.urls import path
from .views import ExtractorView

urlpatterns = [
    path('parse-pdfs/', ExtractorView.as_view(), name="parse_pdf")
]
