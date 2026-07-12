# from django.contrib import admin
# from django.urls import path, include
# from django.http import HttpResponse

# # def home(request):
# #     return HttpResponse("ScholarStep API Running")

# def home(request):
#     return HttpResponse(request, "index.html")


# urlpatterns = [
    
#     path('api/', include('account.urls')),
#     path('admin/', admin.site.urls),
#     path('', home, name='home'),
# ]


from django.contrib import admin
from django.urls import path, include
from account import views
from django.shortcuts import render

def home(request):
    return render(request, "index.html")

urlpatterns = [
    path('api/', include('account.urls')),
    path('admin/', admin.site.urls),
    path('', home, name='home'),

   
    path('role/', views.role, name='role'),
    path('student-register/', views.student_register, name='student_register'),
    path('provider-register/', views.provider_register, name='provider_register'),
    path('admin-register/', views.admin_register, name='admin_register'),
    path('verification/', views.verification, name='verification'),
]
