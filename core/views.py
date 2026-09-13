from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from django.contrib.auth import logout
from .models import Patient,Doctor,DoctorSchedule,Appointment
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils import timezone


def home(request):
    return render(request, "home.html")

def patient_detail(request, patient_id):

    patient = Patient.objects.get(id=patient_id)

    return JsonResponse({
        "id": patient.id,
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender,
        "phone": patient.phone,
    })

def add_patient(request):

    if request.method == "POST":

        name = request.POST.get("name")
        age = request.POST.get("age")
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")

        Patient.objects.create(
            name=name,
            age=age,
            phone=phone,
            gender=gender
        )
        messages.success(request, "Patient added successfully!")
        return redirect("reception")

    return redirect("reception")

@login_required
def dashboard(request):

    if request.user.groups.filter(name="Reception").exists():
        return redirect("reception")

    elif request.user.groups.filter(name="Doctor").exists():
        return redirect("doctor")

    elif request.user.groups.filter(name="Laboratory").exists():
        return redirect("laboratory")

    elif request.user.groups.filter(name="Pharmacy").exists():
        return redirect("pharmacy")

    elif request.user.groups.filter(name="Billing").exists():
        return redirect("billing")

    elif request.user.groups.filter(name="Administrator").exists():
        return redirect("admin_dashboard")

    return render(request, "no_access.html")

@login_required
@role_required("Reception")
def reception(request):
    patients = Patient.objects.all()

    today = timezone.localdate()

    doctor_availability = []

    doctors = Doctor.objects.all()

    for doctor in doctors:
        schedule = DoctorSchedule.objects.filter(
            doctor=doctor,
            day_of_week=today.strftime("%A")
        ).first()

        if not schedule:
            continue

        all_slots, available_slots = get_available_slots(doctor, today)

        booked_count = Appointment.objects.filter(
            doctor=doctor,
            date=today
        ).count()

        total_slots = len(all_slots)
        remaining = len(available_slots)

        doctor_availability.append({
            "doctor": doctor,
            "total_slots": total_slots,
            "booked": booked_count,
            "remaining": remaining,
        })

    return render(request, "reception.html", {
        "patients": patients,
        "doctor_availability": doctor_availability,
    })

@login_required
@role_required("Doctor")
def doctor(request):
    return render(request, "doctor.html")

@login_required
@role_required("Laboratory")
def laboratory(request):
    return render(request, "laboratory.html")

@login_required
@role_required("Pharmacy")
def pharmacy(request):
    return render(request, "pharmacy.html")


def logout_view(request):
    logout(request)
    return redirect("home")

def get_available_slots(doctor, date):
    schedule = DoctorSchedule.objects.filter(
        doctor=doctor,
        day_of_week=date.strftime("%A")
    ).first()

    if not schedule:
        return [], []

    all_slots = []

    current_time = datetime.combine(date, schedule.start_time)
    end_time = datetime.combine(date, schedule.end_time)

    while current_time < end_time:
        all_slots.append(current_time.time())
        current_time += timedelta(minutes=schedule.slot_duration)

    booked_times = Appointment.objects.filter(
        doctor=doctor,
        date=date
    ).values_list("time", flat=True)

    available_slots = [
        slot for slot in all_slots
        if slot not in booked_times
    ]

    return all_slots, available_slots

def view_slots(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    today = timezone.localdate()

    all_slots, available_slots = get_available_slots(doctor, today)

    booked_times = Appointment.objects.filter(
        doctor=doctor,
        date=today
    ).values_list("time", flat=True)

    return render(request, "view_slots.html", {
        "doctor": doctor,
        "date": today,
        "all_slots": all_slots,
        "available_slots": available_slots,
        "booked_times": booked_times,
    })

def doctor_slots(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    today = timezone.localdate()

    all_slots, available_slots = get_available_slots(doctor, today)

    booked_times = Appointment.objects.filter(
        doctor=doctor,
        date=today
    ).values_list("time", flat=True)

    return JsonResponse({
        "doctor": doctor.name,
        "all_slots": [
            slot.strftime("%H:%M")
            for slot in all_slots
        ],
        "available_slots": [
            slot.strftime("%H:%M")
            for slot in available_slots
        ],
        "booked_slots": [
            slot.strftime("%H:%M")
            for slot in booked_times
        ],
    })

@login_required
@role_required("Reception")
def book_appointment(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Invalid request."
        }, status=400)

    patient_id = request.POST.get("patient_id")
    doctor_id = request.POST.get("doctor_id")
    time = request.POST.get("time")

    if not patient_id or not doctor_id or not time:
        return JsonResponse({
            "success": False,
            "message": "Missing appointment information."
        }, status=400)

    patient = get_object_or_404(Patient, id=patient_id)
    doctor = get_object_or_404(Doctor, id=doctor_id)

    today = timezone.localdate()

    # Check whether this slot is already booked
    already_booked = Appointment.objects.filter(
        doctor=doctor,
        date=today,
        time=time
    ).exists()

    if already_booked:
        return JsonResponse({
            "success": False,
            "message": "This slot has already been booked."
        }, status=400)

    Appointment.objects.create(
        patient=patient,
        doctor=doctor,
        date=today,
        time=time
    )

    return JsonResponse({
        "success": True,
        "message": "Appointment booked successfully."
    })

def test_slots(request):
    doctor = Doctor.objects.first()

    date = datetime.strptime("2026-09-14", "%Y-%m-%d").date()

    slots = get_available_slots(doctor, date)

    return JsonResponse({
        "doctor": doctor.name,
        "date": str(date),
        "available_slots": [slot.strftime("%H:%M") for slot in slots]
    })