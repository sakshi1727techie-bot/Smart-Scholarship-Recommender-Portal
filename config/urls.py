from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("ScholarStep API Running")

urlpatterns = [
    path('', home),
    path('api/', include('account.urls')),
    path('admin/', admin.site.urls),
]