from copy import copy
from django.test import TestCase
from sample.models import (Doctor, Worker, Patient, SpecialtyType, TimeSlot, Case, Scan,
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
from django.test.utils import setup_test_environment

setup_test_environment()

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
        doctor.user_id = doctor_user.id
        doctor.registration_time = timezone.now()
        doctor.save()
    except IntegrityError:
        print 'Failed to create a default doctor'
        return HttpResponseServerError()

    try:
        doctor2_user = createUser('doctor2', 'shista@boo.com', 'd2password')
        doctor2_user.save()
        doctor2 = Doctor(user=doctor2_user)
        doctor2.user_id = doctor2_user.id
        doctor2.registration_time = timezone.now()
        doctor2.save()
    except IntegrityError:
        print 'Failed to create a default doctor'
        return HttpResponseServerError()

    try:
        sample_patient = Patient(
                first_name="Alexis",
                last_name="Advantageous",
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
                status=1,
                priority=10,
                submitter_comments=comment_group,
                date_opened="2012-12-12"
            )
        sample_case.save()
    except IntegrityError:
        print 'Failed to create a default worker user'
        return HttpResponseServerError()

    return [worker_user, worker, doctor_user, doctor, sample_patient, comment,
            comment_group, sample_case, doctor2_user, doctor2]


class NewCaseTests(TestCase):
    '''
    Test cases for creating a new case.
    '''

    def test_add_regular_case(self):

        defaults = populate_default_test_data()
        patient = defaults[4]

        self.client = Client()
        self.client.login(username="theworker", password="password")

        url = reverse('new_case', args=['X'])
        response = self.client.post(url,
            {'patient': patient.id,
             'comments': 'Trololololol.',
             'priority': 10,
             'scan_image': None})

        self.assertEqual(response.status_code, 302, "Bad status code")

        # Test that the case page reflects the new case.
        url = response['location']
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        case_id = response.context['case_id']
        case = Case.objects.filter(id=case_id)[0]

        self.assertEqual(response.context['firstName'], patient.first_name)
        self.assertEqual(response.context['lastName'], patient.last_name)
        self.assertEqual(response.context['patient_id'], patient.id)
        self.assertEqual(response.context['gender'], patient.gender)
        self.assertEqual(response.context['date_of_birth'],
                datetime.date(1999, 06, 10))

        self.assertEqual(response.context['priority'], case.priority)

    def test_add_bad_cases(self):
        ''' Ensure that an invalid POST won't be accepted by the server.'''

        defaults = populate_default_test_data()
        patient = defaults[4]

        self.client = Client()
        self.client.login(username="theworker", password="password")

        good = [patient.id, 10]
        bad = [30, 'High']

        for i in range(0, len(good)):
            entries = good[:]
            entries[i] = bad[i]

            url = reverse('new_case', args=['X'])

            try:
                response = self.client.post(url,
                    {'patient': entries[0],
                     'comments': 'Trololololol.',
                     'priority': entries[1],
                     'scan_image': None})
            except Exception:

                # Failure is good
                pass

            self.assertNotEqual(response.status_code, 302,
                                "Sub-Test %d should not redirect." % i)


class UpdateCaseTests(TestCase):
    ''' Test cases for updating a case.'''

    def test_update_priority_open(self):
        ''' Test updating the priority of a case that is still open and is
        not locked.'''

        defaults = populate_default_test_data()
        patient = defaults[4]
        cpatient = copy(patient)
        case = defaults[7]

        self.client = Client()

        accounts = [["theworker", "password"],
                         ["thedoctor", "thepassword"]]

        # Try as both worker and doctor
        for account in accounts:

            self.client.login(username=account[0], password=account[1])

            url = reverse('display_case', args=[case.id, 'p'])
            response = self.client.post(url, {'priority': 20})

            # Test that the case page reflects the new case status.
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['priority'], '20')

            # A reasonable selection of attributes that should still match.
            self.assertEqual(response.context['firstName'],
                             cpatient.first_name)
            self.assertEqual(response.context['lastName'], cpatient.last_name)
            self.assertEqual(response.context['patient_id'], cpatient.id)
            self.assertEqual(response.context['gender'], cpatient.gender)
            self.assertEqual(response.context['date_of_birth'],
                    datetime.date(1999, 06, 10))

    def test_lock_case_doctor(self):
        ''' Test adopting a case as a doctor.'''

        defaults = populate_default_test_data()
        case = defaults[7]

        self.client = Client()
        self.client.login(username="thedoctor", password="thepassword")

        url = reverse('display_case', args=[case.id, 'a'])
        response = self.client.post(url, {'toggle_field': 1})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['lock_holder'],
                             defaults[3])

    def test_lock_case_different_doctor(self):
        ''' Test adopting a case as a different doctor than who locked it.
        This shouldn't work.'''

        defaults = populate_default_test_data()
        case = defaults[7]

         # Set the case to be locked by that different doctor
        case.lock_holder = defaults[9]
        case.save()

        self.client = Client()
        self.client.login(username="thedoctor", password="thepassword")

        url = reverse('display_case', args=[case.id, 'a'])
        response = self.client.post(url, {'toggle_field': 1})

        self.assertEqual(response.status_code, 500)

    def test_lock_case_worker(self):
        ''' Test adopting a case as a worker. Shouldn't work.'''

        defaults = populate_default_test_data()
        case = defaults[7]

        self.client = Client()
        self.client.login(username="theworker", password="password")

        url = reverse('display_case', args=[case.id, 'a'])
        response = self.client.post(url, {'toggle_field': 1})

        self.assertEqual(response.status_code, 500)

    def test_unlock_case_same_doctor(self):
        ''' Test unlocking a case as the same doctor who locked it.'''

        defaults = populate_default_test_data()
        case = defaults[7]

        # Set the case to be locked by the current doctor
        case.lock_holder = defaults[3]
        case.save()

        self.client = Client()
        self.client.login(username="thedoctor", password="thepassword")

        url = reverse('display_case', args=[case.id, 'a'])
        response = self.client.post(url, {'toggle_field': 2})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['lock_holder'],
                             None)

    def test_unlock_case_different_doctor(self):
        ''' Test unlocking a case as the same doctor who locked it. 
        This should not work.'''

        defaults = populate_default_test_data()
        case = defaults[7]

        # Set the case to be locked by doctor account #2
        case.lock_holder = defaults[9]
        case.save()

        self.client = Client()
        self.client.login(username="thedoctor", password="thepassword")

        url = reverse('display_case', args=[case.id, 'a'])
        response = self.client.post(url, {'toggle_field': 2})

        self.assertEqual(response.status_code, 500)

    def test_unlock_case_worker(self):
        ''' Test unlocking a case as a worker. Shouldn't work.'''

        defaults = populate_default_test_data()
        case = defaults[7]

        self.client = Client()
        self.client.login(username="theworker", password="password")

        url = reverse('display_case', args=[case.id, 'a'])
        response = self.client.post(url, {'toggle_field': 2})

        self.assertEqual(response.status_code, 500)


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

        self.assertEqual(doctor1.user.first_name, 'F')
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
