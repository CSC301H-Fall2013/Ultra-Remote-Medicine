from django.test import TestCase
from sample.models import (Doctor, Worker, Patient, Measurement,
        MeasurementType, SpecialtyType, TimeSlot, Case, Scan, Annotation)
from django.contrib.auth.models import User
from psycopg2 import IntegrityError 
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth import login, authenticate
from django.test.client import RequestFactory
from django.test.client import Client
import unittest

def createUser(username, emailaddress, docpassword):
    try:
        user = User(username=username,
            email=emailaddress,
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )
        user.set_password(docpassword)
        return user
    except IntegrityError:
        return HttpResponseServerError()

class SetInfoTests(TestCase):
    """
    Test cases to see whether information on doctor's, worker's and patient's 
    profile page is set up correctly. Also checks whether the information is
    updated correctly when changed.
    """
    
    def test_doctor_first_name(self):
        user = createUser('doctor1', 'a@a.com', 'doctor')
        user.save()
        try:
            doctor1 = Doctor(user=user)
            doctor1.user.first_name = 'F'
            doctor1.registration_time = timezone.now()
            user.save()
            doctor1.save()
        except IntegrityError:
            return HttpResponseServerError()
        
        self.assertEqual(doctor1.user.first_name,'F')
        self.client = Client()
        self.client.login(username="doctor1", password='doctor')
        url = reverse('display_profile', args=[user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].first_name, 'F')
        try:
            doctor1.user.first_name = 'G'
            user.save()
            #doctor1.save()
        except IntegrityError:
            return HttpResponseServerError()
        url = reverse('display_profile', args=[user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(doctor1.user.first_name,'G')
        self.assertEqual(response.context['user'].first_name, 'G')
        
    def test_doctor_change_priority(self):
        user = createUser('doctor1', 'a@a.com', 'doctor')
        user.save()
        try:
            doctor1 = Doctor(user=user)
            doctor1.user.first_name = 'F'
            doctor1.registration_time = timezone.now()
            case1 = Case()
            user.save()
            doctor1.save()
        except IntegrityError:
            return HttpResponseServerError()
        
        self.client = Client()
        self.client.login(username="doctor1", password='doctor')
        url = reverse('display_profile', args=[user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].first_name, 'F')
        try:
            doctor1.user.first_name = 'G'
            user.save()
            #doctor1.save()
        except IntegrityError:
            return HttpResponseServerError()
        url = reverse('display_profile', args=[user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(doctor1.user.first_name,'G')
        self.assertEqual(response.context['user'].first_name, 'G')
        
    def test_doctor_last_name(self):
        user = createUser('doctor1', 'a@a.com', 'doctor')
        try:
            doctor1 = Doctor(user=user)
            doctor1.user.last_name = 'L'
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(doctor1.user.last_name,'L')
    
    def test_doctor_phone(self):
        user = createUser('doctor1', 'a@a.com', 'doctor')
        try:
            doctor1 = Doctor(user=user)
            doctor1.phone = '416'
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(doctor1.phone,'416')
    
    def test_doctor_address(self):
        user = createUser('doctor1', 'a@a.com', 'doctor')
        try:
            doctor1 = Doctor(user=user)
            doctor1.address = 'addr'
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(doctor1.address,'addr')
    
    def test_doctor_comments(self):
        user = createUser('doctor1', 'a@a.com', 'doctor')
        try:
            doctor1 = Doctor(user=user)
            doctor1.comments = 'commie'
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(doctor1.comments,'commie')
    
    def test_worker_first_name(self):
        user = createUser('worker1', 'b@b.com', 'worker')
        try:
            worker1 = Worker(user=user)
            worker1.user.first_name = 'W'
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(worker1.user.first_name,'W')
    
    def test_worker_last_name(self):
        user = createUser('worker1', 'b@b.com', 'worker')
        try:
            worker1 = Worker(user=user)
            worker1.user.last_name = 'E'
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(worker1.user.last_name,'E')
    
    def test_worker_phone(self):
        user = createUser('worker1', 'b@b.com', 'worker')
        try:
            worker1 = Worker(user=user)
            worker1.phone = '647'
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(worker1.phone,'647')    
    
    def test_worker_address(self):
        user = createUser('worker1', 'b@b.com', 'worker')
        try:
            worker1 = Worker(user=user)
            worker1.address = 'wadd'
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(worker1.address,'wadd')  
    
    def test_worker_comments(self):
        user = createUser('worker1', 'b@b.com', 'worker')
        try:
            worker1 = Worker(user=user)
            worker1.comments = 'uncomm'
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(worker1.comments,'uncomm')
        
    def test_patient_first_name(self):
        try:
            patient = Patient()
            patient.first_name = 'troll'
            patient.save()
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(patient.first_name, 'troll')
        
    def test_patient_last_name(self):
        try:
            patient = Patient()
            patient.last_name = 'ho'
            patient.save()
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(patient.last_name, 'ho')
        
    def test_patient_gps(self):
        try:
            patient = Patient()
            patient.gps_coordinates = '101010'
            patient.save()
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(patient.gps_coordinates, '101010')
        
    def test_patient_address(self):
        try:
            patient = Patient()
            patient.address = '420 street'
            patient.save()
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(patient.address, '420 street')
        
    def test_patient_dob(self):
        try:
            patient = Patient()
            patient.date_of_birth = '1999-10-10'
            patient.save()
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(patient.date_of_birth, '1999-10-10')
        
    def test_patient_phone(self):
        try:
            patient = Patient()
            patient.phone = '416'
            patient.save()
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(patient.phone, '416')
        
    def test_patient_health_id(self):
        try:
            patient = Patient()
            patient.health_id = '12345'
            patient.save()
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(patient.health_id, '12345')
        
    def test_patient_gender(self):
        try:
            patient = Patient()
            patient.gender = 'Male'
            patient.save()
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(patient.gender, 'Male')
        
    def test_patient_email(self):
        try:
            patient = Patient()
            patient.email = 'a@a.com'
            patient.save()
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(patient.email, 'a@a.com')
    
    