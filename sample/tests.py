from django.test import TestCase
from sample.models import (Doctor, Worker, Patient, Measurement,
        MeasurementType, SpecialtyType, TimeSlot, Case, Scan, Annotation)
from django.contrib.auth.models import User
from psycopg2 import IntegrityError 
from django.core.urlresolvers import reverse

def createUser(username, emailaddress, docpassword):
    try:
        user = User(username=username,
            email=emailaddress,
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )
        user.set_password(docpassword)
        user.save()
        return user
    except IntegrityError:
        return HttpResponseServerError()

class SetInfoTests(TestCase):
    """
    Test cases to see whether information on doctor's and worker's profile page
    is set up correctly
    """
    def test_doctor_first_name(self):
        user = createUser('doctor1', 'a@a.com', 'doctor')
        try:
            doctor1 = Doctor(user=user)
            doctor1.user.first_name = 'F'
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(doctor1.user.first_name,'F')
        #response = self.client.get('templates/website/doctorprofile.html')
        #self.assertEqual(response.status_code, 200)
        #response = self.client.get(reverse('profile:doctorprofile'))
    
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
    
    