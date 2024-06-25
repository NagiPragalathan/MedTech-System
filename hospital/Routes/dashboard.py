# views.py
from django.shortcuts import render
from django.db.models import Count
from hospital.models import User, Patient, Hospital_Information, Notification
import random

def dashboard_view(request):
    # Query data
    num_users = User.objects.count()
    num_patients = Patient.objects.count()
    num_hospitals = Hospital_Information.objects.count()
    num_notifications = Notification.objects.count()

    # Data for charts (example: number of patients per hospital type)
    hospital_types = Hospital_Information.objects.values('hospital_type').annotate(count=Count('hospital_id'))
    hospital_type_labels = [ht['hospital_type'] for ht in hospital_types]
    hospital_type_data = [ht['count'] for ht in hospital_types]

    # Number of patients per blood group
    blood_groups = Patient.objects.values('blood_group').annotate(count=Count('patient_id'))
    blood_group_labels = [bg['blood_group'] for bg in blood_groups]
    blood_group_data = [bg['count'] for bg in blood_groups]

    # Number of notifications over time
    notifications_over_time = Notification.objects.extra(select={'day': "DATE(notify_time)"}).values('day').annotate(count=Count('id')).order_by('day')
    notification_dates = [n['day'] for n in notifications_over_time]
    notification_counts = [n['count'] for n in notifications_over_time]

    # Number of users by type
    user_types = {
        'Patients': Patient.objects.count(),
        'Doctors': User.objects.filter(is_doctor=True).count(),
        'Hospital Admins': User.objects.filter(is_hospital_admin=True).count(),
        'Lab Workers': User.objects.filter(is_labworker=True).count(),
        'Pharmacists': User.objects.filter(is_pharmacist=True).count(),
    }
    user_type_labels = list(user_types.keys())
    user_type_data = list(user_types.values())

    # Random data for additional charts
    cities = ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem"]
    random_data = {
        "cities": cities,
        "hospitals": [random.randint(10, 50) for _ in cities],
        "doctors": [random.randint(50, 300) for _ in cities],
        "patients": [random.randint(100, 1000) for _ in cities],
    }
    bubble_chart_data = [{"city": city, "patients": patients, "index": index, "radius": patients // 10} for index, (city, patients) in enumerate(zip(cities, random_data["patients"]))]
    line_chart_data = [{"date": f"2023-06-{day}", "value": random.randint(20, 100)} for day in range(1, 31)]

    # Debugging: print the data
    print("Random Data:", random_data)
    print("Bubble Chart Data:", bubble_chart_data)
    print("Line Chart Data:", line_chart_data)

    context = {
        'num_users': num_users,
        'num_patients': num_patients,
        'num_hospitals': num_hospitals,
        'num_notifications': num_notifications,
        'hospital_type_labels': hospital_type_labels,
        'hospital_type_data': hospital_type_data,
        'blood_group_labels': blood_group_labels,
        'blood_group_data': blood_group_data,
        'notification_dates': notification_dates,
        'notification_counts': notification_counts,
        'user_type_labels': user_type_labels,
        'user_type_data': user_type_data,
        'random_data': random_data,
        'bubble_chart_data': bubble_chart_data,
        'line_chart_data': line_chart_data,
    }

    return render(request, 'dashboard/dashboard.html', context)
