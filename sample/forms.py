from django import forms


class JQueryUIDatepickerWidget(forms.DateInput):
    ''' Widget designed to allow the user to pick the date. Source:
        Stackoverflow Doesn't work.'''

    def __init__(self, **kwargs):
        super(forms.DateInput, self).__init__(attrs={"size": 10,
            "class": "dateinput"}, **kwargs)

    class Media:
        css = {"all": ("http://ajax.googleapis.com/ajax/libs/jqueryui/"\
            "1.8.6/themes/redmond/jquery-ui.css",)}
        js = ("http://ajax.googleapis.com/ajax/libs/jquery/1.4.3/"\
              "jquery.min.js", "http://ajax.googleapis.com/ajax/"\
              "libs/jqueryui/.8.6/jquery-ui.min.js",)


class NewCaseForm(forms.Form):
    ''' The form used on the new case page.'''

    patient = forms.IntegerField();
    comments = forms.CharField(required=False, widget=forms.Textarea)
    priority = forms.ChoiceField(required=False, choices=((10, 'Low'),
        (20, 'Medium'), (30, 'High')))


class NewPatientForm(forms.Form):
    ''' The form used on the new patient page.'''

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    gps_coordinates = forms.CharField(max_length=63, required=False)
    address = forms.CharField(max_length=254, required=False)
    date_of_birth = forms.DateField(required=False,
        widget=JQueryUIDatepickerWidget)
    phone_number = forms.CharField(max_length=63, required=False)
    health_id = forms.CharField(max_length=63, required=False)
    photo_link = forms.URLField(required=False)
    sex = forms.ChoiceField(required=False, choices=(('Female', 'Female'),
        ('Male', 'Male'), ('Other', 'Other')))
    email = forms.CharField(max_length=254, required=False)


class UpdateFieldWorkerForm(forms.Form):
    ''' The main form for updating field worker information.'''

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=63)
    address = forms.CharField(max_length=254)
    comments = forms.CharField(required=False, widget=forms.Textarea)

    def populate(self, worker):

        self.fields["first_name"].initial = worker.user.first_name
        self.fields["last_name"].initial = worker.user.last_name
        self.fields["phone_number"].initial = worker.phone
        self.fields["address"].initial = worker.address
        self.fields["comments"].initial = worker.comments


class UpdateDoctorForm(forms.Form):
    ''' The main form for updating field worker information.'''

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=63)
    address = forms.CharField(max_length=254)
    comments = forms.CharField(required=False, widget=forms.Textarea)

    def populate(self, doctor):

        self.fields["first_name"].initial = doctor.user.first_name
        self.fields["last_name"].initial = doctor.user.last_name
        self.fields["phone_number"].initial = doctor.phone
        self.fields["address"].initial = doctor.address
        self.fields["comments"].initial = doctor.comments
