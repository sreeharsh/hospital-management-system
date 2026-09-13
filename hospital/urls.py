from django.contrib import admin
from django.urls import path,include
from core import views
from core.views import (
    home,
    dashboard,
    reception,
    doctor,
    laboratory,
    pharmacy,
    logout_view,
    
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='home.html'
        ),
        name='login'
    ),

    path('reception/', reception, name='reception'),
    path('doctor/', doctor, name='doctor'),
    path('laboratory/', laboratory, name='laboratory'),
    path('pharmacy/', pharmacy, name='pharmacy'),
    path('dashboard/', dashboard, name='dashboard'),
    path("logout/", logout_view, name="logout"),
    path("add-patient/", views.add_patient, name="add_patient"),
    path(
    "patient/<int:patient_id>/",
    views.patient_detail,
    name="patient_detail"
        ),
    path("test-slots/", views.test_slots, name="test_slots"),
    path(
        "view-slots/<int:doctor_id>/",
        views.view_slots,
        name="view_slots"
    ),
    path(
    "doctor-slots/<int:doctor_id>/",
    views.doctor_slots,
    name="doctor_slots"
    ),
    path(
    "book-appointment/",
    views.book_appointment,
    name="book_appointment"
    ),
]