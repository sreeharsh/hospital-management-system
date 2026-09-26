# Hospital Management System

A Django-based hospital management system focused on patient management,
doctor scheduling, appointment availability, and appointment booking.

## Project Overview

This project is being developed as a practical Python and Django
application to model common hospital reception and appointment
management workflows.

The system currently focuses on the reception side of the hospital,
including patient registration, patient selection, doctor availability,
appointment-slot generation, and appointment booking.

## Features

### Patient Management
- Register new patients
- View registered patients
- Search patients
- Select a patient and view patient information

### Doctor Management
- Manage doctors
- Associate doctors with departments
- Define doctor working schedules

### Appointment Management
- Generate appointment slots from doctor schedules
- Display available and booked slots
- Book appointments for selected patients
- Prevent duplicate bookings for the same doctor, date, and time
- Refresh slot availability after a booking

### Authentication and Authorization
- User authentication
- Role-based access control
- Reception-specific access to the reception dashboard
- CSRF protection for appointment booking

### Dynamic Interface
- JavaScript-based patient selection
- Dynamic doctor-slot loading
- Fetch API communication with Django JSON endpoints
- Dynamic appointment booking without a full page refresh

## Technologies

- Python
- Django
- Django ORM
- JavaScript
- HTML
- CSS
- SQL
- Git
- GitHub

## Project Architecture

The main data relationships currently include:

Patient
- Appointments

Doctor
- Doctor Schedule
- Appointments

Doctor Schedule
- Defines the working period and slot duration

Appointment
- Connects a patient, doctor, date, and time

## Example Workflow

1. Receptionist selects a patient.
2. Receptionist views doctor availability.
3. Django generates appointment slots from the doctor's schedule.
4. Previously booked slots are identified.
5. Available slots are displayed in the browser.
6. Receptionist selects an available slot.
7. JavaScript sends the booking request to Django.
8. Django validates the request and creates the appointment.
9. The updated slot availability is returned to the interface.

## Project Status

The project is actively under development.

Planned areas include:

- Patient history
- Today's appointments
- Appointment status
- Future appointment dates
- Consultation records
- Prescriptions
- Lab and scan reports
- Billing and payments
- Automated testing
- Production database and deployment

## Author

**Sreeharsh Manas M M**

Python / Django Developer

GitHub:
https://github.com/sreeharsh/hospital-management-system