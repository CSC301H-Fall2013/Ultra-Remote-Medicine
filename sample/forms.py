from django import forms


class JQueryUIDatepickerWidget(forms.DateInput):
    ''' Widget designed to allow the user to pick the date. Source:
        Stackoverflow. Doesn't work.'''

    def __init__(self, **kwargs):
        super(forms.DateInput, self).__init__(attrs={"size": 10,
                                                     "class": "dateinput"},
                                              **kwargs)

    class Media:
        css = {"all": ("http://ajax.googleapis.com/ajax/libs/jqueryui/\
            1.8.6/themes/redmond/jquery-ui.css",)}
        js = ("http://ajax.googleapis.com/ajax/libs/jquery/1.4.3/\
              jquery.min.js", "http://ajax.googleapis.com/ajax/\
              libs/jqueryui/.8.6/jquery-ui.min.js",)


class NewCaseForm(forms.Form):
    ''' The form used on the new case page.'''

    patient = forms.IntegerField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    priority = forms.ChoiceField(required=False, choices=((10, 'High'),
                                 (20, 'Medium'), (30, 'Low')))
    status = forms.ChoiceField(required=False, choices=((1, 'Open'),
                                 (2, 'Closed')))

    def populate(self, patient_id):
        ''' Populates this form with default information. '''

        if patient_id != 'X':
            self.fields['patient'].initial = patient_id


class UpdateCasePriorityForm(forms.Form):
    ''' The form used on the case page. '''

    priority = forms.ChoiceField(required=False,
                                 widget=forms.Select(attrs={"onChange":
                                                     'this.form.submit()'}),
                                 choices=((10, 'High'), (20, 'Medium'),
                                          (30, 'Low')))

    def populate(self, case):
        ''' Populates this form with default information. '''

        self.fields["priority"].initial = case.priority
        
class UpdateCaseStatusForm(forms.Form):
    ''' The form used on the case page. '''

    status = forms.ChoiceField(required=False,
                                 widget=forms.Select(attrs={"onChange":
                                                     'this.form.submit()'}),
                                 choices=((1, 'Open'), (2, 'Closed')))

    def populate(self, case):
        ''' Populates this form with default information. '''

        self.fields["status"].initial = case.status


class UpdateCaseLockHolderForm(forms.Form):
    ''' The form used on the case page. '''
 
    toggle_field = forms.ChoiceField(required=False,
                                 widget=forms.Select(attrs={"onChange":
                                                     'this.form.submit()'}),
                                 choices=[(1, 'Abort'), (2,'Adopt')])
 
    def populate(self):
        ''' Populates this form with default information. '''
  
        self.fields["toggle_field"].initial = self.fields["toggle_field"].choices[1][0]


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


class PostCommentForm(forms.Form):
    ''' The main form for posting a comment.'''

    comments = forms.CharField(required=False, widget=forms.Textarea)
    arg = forms.CharField(required=False, widget=forms.Textarea)
    comment_id = forms.IntegerField(required=False, widget=forms.Textarea)
    # comment_id = forms.IntegerField(widget=forms.HiddenInput(
    # attrs={'id': 'commentIdentifier'}))
