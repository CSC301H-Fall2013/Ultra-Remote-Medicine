from django.test import TestCase
from sample.models import (Doctor, Worker, Patient, Measurement,
        MeasurementType, SpecialtyType, TimeSlot, Case, Scan, Annotation,
        Comment, CommentGroup)
from django.contrib.auth.models import User
from psycopg2 import IntegrityError
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth import login, authenticate
from django.test.client import RequestFactory
from django.test.client import Client
import unittest
from django.http import HttpResponseServerError
import datetime

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


client = Client()


def populate_default_test_data():
    ''' Populates the database with default test data. '''

    try:
        worker_user = createUser('theworker', 'o@hola.com', 'password')
        worker_user.save()
        worker = Worker(user=worker_user)
        worker.registration_time = timezone.now()
        worker.save()

    except IntegrityError:
        print 'Failed to create a default worker user'
        return HttpResponseServerError()

    try:
        doctor_user = createUser('thedoctor', 'o@boo.com', 'thepassword')
        doctor_user.save()
        doctor = Doctor(user=doctor_user)
        doctor.user_id = worker_user.id
        doctor.registration_time = timezone.now()
        doctor.save()
    except IntegrityError:
        print 'Failed to create a default doctor'
        return HttpResponseServerError()

    try:
        sample_patient = Patient(
                first_name="Jacobi",
                last_name="Miniti",
                gps_coordinates="101010",
                address="Yonge street",
                date_of_birth="1999-06-10",
                phone="646646646464",
                health_id="324324234",
                gender="Male",
                email="test@test.com"
            )

        sample_patient.save()
    except IntegrityError:
        print 'Failed to create a default patient'
        return HttpResponseServerError()

    try:
        comment = Comment(author=worker_user,
                          text="Trololololol.",
                          time_posted=timezone.now())
        comment.save()
    except IntegrityError:
        print 'Failed to create a default comment'
        return HttpResponseServerError()

    try:
        comment_group = CommentGroup()
        comment_group.save()
        comment_group.comments.add(comment)
    except IntegrityError:
        print 'Failed to create a default comment group'
        return HttpResponseServerError()

    try:
        sample_case = Case(
                patient=sample_patient,
                submitter=worker,
                lock_holder=None,
                priority=10,
                submitter_comments=comment_group,
                date_opened="2012-12-12"
            )
        sample_case.save()
    except IntegrityError:
        print 'Failed to create a default worker user'
        return HttpResponseServerError()

    return [worker_user, worker, doctor_user, doctor, sample_patient, comment,
            comment_group, sample_case]


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
        defaults = populate_default_test_data()
        user = defaults[2]
        #user.save()
        try:
            doctor1 = defaults[3]
            patient1 = defaults[4]
            #user.save()
            #doctor1.save()
            #patient1.save()
        except IntegrityError:
            return HttpResponseServerError()
        
        self.client = Client()
        self.client.login(username="thedoctor", password='thepassword')
        url = reverse('display_case', args=[defaults[-1].id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(defaults[-1].priority, 10)
        try:
            defaults[-1].priority = 30
            defaults[-1].save()
            #doctor1.save()
        except IntegrityError:
            return HttpResponseServerError()
        url = reverse('display_case', args=[defaults[-1].id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(defaults[-1].priority, 30)
        
    def test_worker_change_priority(self):
        defaults = populate_default_test_data()
        user = defaults[0]
        #user.save()
        try:
            worker1 = defaults[1]
            patient1 = defaults[4]
            #user.save()
            #doctor1.save()
            #patient1.save()
        except IntegrityError:
            return HttpResponseServerError()
        
        self.client = Client()
        self.client.login(username="theworker", password='password')
        url = reverse('display_case', args=[defaults[-1].id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(defaults[-1].priority, 10)
        try:
            defaults[-1].priority = 30
            defaults[-1].save()
            #doctor1.save()
        except IntegrityError:
            return HttpResponseServerError()
        url = reverse('display_case', args=[defaults[-1].id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(defaults[-1].priority, 30)

    def test_doctor_last_name(self):
        user = createUser('doctor1', 'a@a.com', 'doctor')
        try:
            doctor1 = Doctor(user=user)
            doctor1.user.last_name = 'L'
            user.save()
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(doctor1.user.last_name, 'L')

    def test_doctor_phone(self):
        user = createUser('doctor1', 'a@a.com', 'doctor')
        try:
            doctor1 = Doctor(user=user)
            doctor1.phone = '416'
            user.save()
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(doctor1.phone, '416')

    def test_doctor_address(self):
        user = createUser('doctor1', 'a@a.com', 'doctor')
        try:
            doctor1 = Doctor(user=user)
            doctor1.address = 'addr'
            user.save()
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(doctor1.address, 'addr')

    def test_doctor_comments(self):
        user = createUser('doctor1', 'a@a.com', 'doctor')
        try:
            doctor1 = Doctor(user=user)
            doctor1.comments = 'commie'
            user.save()
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(doctor1.comments, 'commie')

    def test_worker_first_name(self):
        user = createUser('worker1', 'b@b.com', 'worker')
        try:
            worker1 = Worker(user=user)
            worker1.user.first_name = 'W'
            user.save()
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(worker1.user.first_name, 'W')

    def test_worker_last_name(self):
        user = createUser('worker1', 'b@b.com', 'worker')
        try:
            worker1 = Worker(user=user)
            worker1.user.last_name = 'E'
            user.save()
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(worker1.user.last_name, 'E')

    def test_worker_phone(self):
        user = createUser('worker1', 'b@b.com', 'worker')
        try:
            worker1 = Worker(user=user)
            worker1.phone = '647'
            user.save()
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(worker1.phone, '647')

    def test_worker_address(self):
        user = createUser('worker1', 'b@b.com', 'worker')
        try:
            worker1 = Worker(user=user)
            worker1.address = 'wadd'
            user.save()
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(worker1.address, 'wadd')

    def test_worker_comments(self):
        user = createUser('worker1', 'b@b.com', 'worker')
        try:
            worker1 = Worker(user=user)
            worker1.comments = 'uncomm'
            user.save()
        except IntegrityError:
            return HttpResponseServerError()
        self.assertEqual(worker1.comments, 'uncomm')

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

    def test_create_new_patient(self):
        user = createUser('doctor2', 'a@a.com', 'doctorf')
        user.save()
        try:
            doctor1 = Doctor(user=user)
            doctor1.user.first_name = 'F'
            doctor1.registration_time = timezone.now()
            user.save()
            doctor1.save()
        except IntegrityError:
            return HttpResponseServerError()

        try:
            patient = Patient(
                first_name = "John",
                last_name = "Smith",
                gps_coordinates = "101010",
                address = "Yonge street",
                date_of_birth = "1999-06-10",
                phone = "646646646464",
                health_id = "324324234",
                gender = "Male",
                email = "test@test.com"
            )
            patient.save()
        except IntegrityError:
            return HttpResponseServerError()

        self.assertEqual(patient.first_name, "John")
        self.assertEqual(patient.last_name, "Smith")
        self.assertEqual(patient.gps_coordinates, "101010")
        self.assertEqual(patient.address, "Yonge street")
        self.assertEqual(patient.date_of_birth, "1999-06-10")
        self.assertEqual(patient.phone, "646646646464")
        self.assertEqual(patient.health_id, "324324234")
        self.assertEqual(patient.gender, "Male")
        self.assertEqual(patient.email, "test@test.com")

        self.client.login(username="doctor2", password='doctorf')
        url2 = reverse('display_patient', args=[patient.id])
        response = self.client.get(url2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['firstName'], "John")
        self.assertEqual(response.context['viewer'], user)
        self.assertEqual(response.context['user'], user)
        self.assertEqual(response.context['lastName'], "Smith")
        self.assertEqual(response.context['gender'], "Male")
        self.assertEqual(response.context['date_of_birth'], datetime.date(1999, 06,10))
        self.assertEqual(response.context['gps_coordinates'], "101010")
        self.assertEqual(response.context['health_id'], "324324234")
        self.assertEqual(response.context['address'], "Yonge street")
        self.assertEqual(response.context['phone'], "646646646464")
        self.assertEqual(response.context['email'], "test@test.com")
