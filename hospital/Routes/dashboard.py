# views.py
from django.shortcuts import render
from django.db.models import Count
from hospital.models import User, Patient, Hospital_Information, Notification

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
    }

    return render(request, 'dashboard/dashboard.html', context)
