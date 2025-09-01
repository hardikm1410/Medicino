# Django Project Structure and Setup
# Run these commands to create Django project:
# django-admin startproject medicino_project .
# python manage.py startapp medicino_app

# ===== settings.py =====
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'medicino_app',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'medicino_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'medicino_django.db',
    }
}

CORS_ALLOW_ALL_ORIGINS = True
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# ===== models.py =====
from django.db import models
from django.utils import timezone

class Medicine(models.Model):
    CATEGORY_CHOICES = [
        ('analgesic', 'Analgesic'),
        ('antibiotic', 'Antibiotic'),
        ('antihistamine', 'Antihistamine'),
        ('nsaid', 'NSAID'),
        ('ppi', 'Proton Pump Inhibitor'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    dosage = models.CharField(max_length=500)
    side_effects = models.TextField()
    contraindications = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class SymptomDatabase(models.Model):
    SEVERITY_CHOICES = [
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
        ('critical', 'Critical'),
    ]

    condition_name = models.CharField(max_length=200)
    symptoms = models.TextField(help_text="Comma-separated symptoms")
    ayurvedic_remedy = models.TextField()
    medicine_suggestion = models.TextField()
    severity_level = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    description = models.TextField()
    precautions = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.condition_name

    def get_symptoms_list(self):
        return [symptom.strip() for symptom in self.symptoms.split(',')]

    class Meta:
        ordering = ['condition_name']

class DiagnosisHistory(models.Model):
    symptoms = models.TextField()
    diagnosed_condition = models.CharField(max_length=200)
    ayurvedic_remedy = models.TextField()
    medicine_suggestion = models.TextField()
    confidence_score = models.FloatField()
    user_feedback = models.TextField(blank=True, null=True)
    user_ip = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.diagnosed_condition} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Diagnosis Histories"

# ===== serializers.py =====
from rest_framework import serializers
from .models import Medicine, SymptomDatabase, DiagnosisHistory

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

class SymptomDatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomDatabase
        fields = '__all__'

class DiagnosisHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisHistory
        fields = '__all__'

class DiagnosisRequestSerializer(serializers.Serializer):
    symptoms = serializers.CharField(max_length=1000)

# ===== views.py =====
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Medicine, SymptomDatabase, DiagnosisHistory
from .serializers import MedicineSerializer, DiagnosisRequestSerializer, DiagnosisHistorySerializer
import json
import re

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def diagnose_symptoms_ai(symptoms_text):
    """AI-like symptom diagnosis logic using Django ORM"""
    conditions = SymptomDatabase.objects.all()
    input_symptoms = [s.strip().lower() for s in re.split(r'[,\s]+', symptoms_text.lower()) if s.strip()]

    best_match = None
    best_score = 0

    for condition in conditions:
        condition_symptoms = [s.strip().lower() for s in condition.symptoms.split(',')]
        matches = sum(1 for symptom in input_symptoms if any(symptom in cs or cs in symptom for cs in condition_symptoms))
        score = matches / len(condition_symptoms) if condition_symptoms else 0

        if score > best_score and score > 0.3:
            best_score = score
            best_match = condition

    if best_match:
        return {
            'disease': best_match.condition_name,
            'ayurvedic': best_match.ayurvedic_remedy,
            'medicine': best_match.medicine_suggestion,
            'confidence': round(best_score * 100, 2),
            'severity': best_match.severity_level,
            'description': best_match.description,
            'precautions': best_match.precautions
        }
    else:
        return {
            'disease': 'Unable to determine condition',
            'ayurvedic': 'Please consult an Ayurvedic practitioner for personalized treatment.',
            'medicine': 'Please consult a healthcare professional for proper diagnosis.',
            'confidence': 0,
            'severity': 'unknown',
            'description': 'Symptoms do not match any known conditions in our database.',
            'precautions': 'Seek professional medical advice for proper diagnosis.'
        }

def index(request):
    """Main page view"""
    return render(request, 'index.html')

@api_view(['POST'])
def diagnose_api(request):
    """Diagnosis API endpoint"""
    serializer = DiagnosisRequestSerializer(data=request.data)
    if serializer.is_valid():
        symptoms = serializer.validated_data['symptoms']
        diagnosis_result = diagnose_symptoms_ai(symptoms)

        # Save to history
        DiagnosisHistory.objects.create(
            symptoms=symptoms,
            diagnosed_condition=diagnosis_result['disease'],
            ayurvedic_remedy=diagnosis_result['ayurvedic'],
            medicine_suggestion=diagnosis_result['medicine'],
            confidence_score=diagnosis_result['confidence'],
            user_ip=get_client_ip(request)
        )

        return Response({'success': True, 'data': diagnosis_result})
    else:
        return Response({'success': False, 'message': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def medicine_detail_api(request, medicine_name):
    """Medicine detail API endpoint"""
    try:
        medicine = Medicine.objects.filter(name__icontains=medicine_name).first()
        if medicine:
            serializer = MedicineSerializer(medicine)
            return Response({'success': True, 'data': serializer.data})
        else:
            return Response({'success': False, 'message': 'Medicine not found'})
    except Exception as e:
        return Response({'success': False, 'message': str(e)})

class MedicineListAPIView(generics.ListAPIView):
    """List all medicines API"""
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

class DiagnosisHistoryAPIView(generics.ListAPIView):
    """Diagnosis history API"""
    queryset = DiagnosisHistory.objects.all()[:50]  # Latest 50 records
    serializer_class = DiagnosisHistorySerializer

# ===== urls.py (main project) =====
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('medicino_app.urls')),
    path('api/', include('medicino_app.urls')),
]

# ===== urls.py (app) =====
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/diagnose/', views.diagnose_api, name='diagnose_api'),
    path('api/medicine/<str:medicine_name>/', views.medicine_detail_api, name='medicine_detail_api'),
    path('api/medicines/', views.MedicineListAPIView.as_view(), name='medicine_list_api'),
    path('api/history/', views.DiagnosisHistoryAPIView.as_view(), name='diagnosis_history_api'),
]

# ===== admin.py =====
from django.contrib import admin
from .models import Medicine, SymptomDatabase, DiagnosisHistory

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']

@admin.register(SymptomDatabase)
class SymptomDatabaseAdmin(admin.ModelAdmin):
    list_display = ['condition_name', 'severity_level', 'created_at']
    list_filter = ['severity_level', 'created_at']
    search_fields = ['condition_name', 'symptoms', 'description']
    ordering = ['condition_name']

@admin.register(DiagnosisHistory)
class DiagnosisHistoryAdmin(admin.ModelAdmin):
    list_display = ['diagnosed_condition', 'confidence_score', 'user_ip', 'created_at']
    list_filter = ['diagnosed_condition', 'created_at']
    search_fields = ['symptoms', 'diagnosed_condition']
    readonly_fields = ['created_at', 'user_ip']
    ordering = ['-created_at']

# ===== Django Requirements =====
# Create requirements_django.txt with:
"""
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
"""

# ===== Management Commands =====
# Create management/commands/setup_data.py:
"""
from django.core.management.base import BaseCommand
from medicino_app.models import Medicine, SymptomDatabase

class Command(BaseCommand):
    help = 'Setup initial data for Medicino app'

    def handle(self, *args, **options):
        # Clear existing data
        Medicine.objects.all().delete()
        SymptomDatabase.objects.all().delete()

        # Add medicines and conditions data
        # (Use the same data as in the Flask version)
        self.stdout.write(self.style.SUCCESS('Successfully setup initial data'))
"""
