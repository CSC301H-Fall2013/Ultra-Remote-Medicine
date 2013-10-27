from django import forms

class JQueryUIDatepickerWidget(forms.DateInput):
    ''' Widget designed to allow the user to pick the date. Doesn't work.'''

    def __init__(self, **kwargs):
        super(forms.DateInput, self).__init__(attrs={"size":10, "class": "dateinput"}, **kwargs)

    class Media:
        css = {"all":("http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/themes/redmond/jquery-ui.css",)}
        js = ("http://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js",
              "http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/jquery-ui.min.js",)

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
    sex = forms.ChoiceField(required=False, choices=
            (('Female', 'Female'), ('Male', 'Male'), ('Other', 'Other')))
    email = forms.CharField(max_length=254, required=False)
