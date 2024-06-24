from unicodedata import name
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .pres_pdf import prescription_pdf

from hospital.Routes.Ocr import *
from hospital.Routes.Notify import *
from hospital.Routes.CareTaker import *
from hospital.Routes.HeartRate import *
from hospital.Routes.VideoConf import *

# from . --> same directory
# Views functions and urls must be linked. # of views == # of urls
# App URL file - urls related to hospital

urlpatterns = []
custom_urls = [
    path('show_doc', show_doc, name='show_doc'),
    path('file_to_txt', upload_image_view, name='file_to_txt'),
    path('get_bot_response', get_bot_response, name='get_bot_response'),
]
hospital_urls = [
    path('', views.hospital_home, name='hospital_home'),
    path('search/', views.search, name='search'),
    path('change-password/<int:pk>', views.change_password, name='change-password'),
    path('add-billing/', views.add_billing, name='add-billing'),
    path('appointments/', views.appointments, name='appointments'),
    path('edit-billing/', views.edit_billing, name='edit-billing'),
    path('edit-prescription/', views.edit_prescription, name='edit-prescription'),
    # path('forgot-password/', views.forgot_password,name='forgot-password'),
    path('patient-dashboard/',views.patient_dashboard, name='patient-dashboard'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('profile-settings/',views.profile_settings, name='profile-settings'),
    path('about-us/', views.about_us, name='about-us'),
    path('patient-register/', views.patient_register, name='patient-register'),
    path('logout/', views.logoutUser, name='logout'),
    path('multiple-hospital/', views.multiple_hospital, name='multiple-hospital'),
    path('chat/<int:pk>/', views.chat, name='chat'),
    path('chat-doctor/', views.chat_doctor, name='chat-doctor'),
    path('hospital-profile/<int:pk>/', views.hospital_profile, name='hospital-profile'),
    path('checkout-payment/', views.checkout_payment, name='checkout-payment'),
    path('shop/', views.pharmacy_shop, name='pharmacy_shop'),
    path('data-table/', views.data_table, name='data-table'),
    path('testing/',views.testing, name='testing'),
    path('hospital-department-list/<int:pk>/', views.hospital_department_list, name='hospital-department-list'),
    path('hospital-doctor-list/<int:pk>/', views.hospital_doctor_list, name='hospital-doctor-list'),
    path('hospital-doctor-register/<int:pk>/', views.hospital_doctor_register, name='hospital-doctor-register'),
    path('view-report/<int:pk>', views.view_report, name='view-report'),
    path('test-cart/<int:pk>/', views.test_cart, name='test-cart'),
    path('prescription-view/<int:pk>', views.prescription_view, name='prescription-view'),
    path('pres_pdf/<int:pk>/',views.prescription_pdf, name='pres_pdf'),
    path('test-single/<int:pk>/', views.test_single, name='test-single'),
    path('test-remove-cart/<int:pk>/', views.test_remove_cart, name='test-remove-cart'),
    path('test-add-to-cart/<int:pk>/<int:pk2>/', views.test_add_to_cart, name='test-add-to-cart'),
    path('delete-prescription/<int:pk>/', views.delete_prescription, name='delete-prescription'),
    path('delete-report/<int:pk>/', views.delete_report, name='delete-report'),

]
NotifyUrls = [
    path('add_notify', add_notification, name='add_notify'),
    path('delete_notify/<uuid:notification_id>', delete_notification, name='delete_notify'),
    path('edit_notify/<uuid:notification_id>', edit_notification, name='edit_notify'),
    path('notification', notification, name='notification'),
]
CareTakerUrl = [
    path('add_caretaker', add_caretaker, name='add_caretaker'),
    path('caretaker_list', caretaker_list, name='caretaker_list'),
    path('caretaker_edit/<uuid:caretaker_id>', caretaker_edit, name='caretaker_edit'),
    path('caretaker_delete/<uuid:caretaker_id>', caretaker_delete, name='caretaker_delete'),
]

heart_rate = [
    path('rate',get_rate,name='get_rate'),
    path('heat_sen',sensor_data_stream,name='sensor_data_stream'),
]
video_conf_url = [
    path('MeetRoom',MeetRoom,name='MeetRoom'),
    path('api/latest-notification-time/', get_latest_notification_time, name='latest-notification-time'),
]

urlpatterns.extend(custom_urls)
urlpatterns.extend(video_conf_url)
urlpatterns.extend(heart_rate)
urlpatterns.extend(CareTakerUrl)
urlpatterns.extend(hospital_urls) 
urlpatterns.extend(NotifyUrls) 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
