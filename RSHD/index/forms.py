from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100) 

class DateForm(forms.Form):
    date = forms.DateField(input_formats=['%d/%m/%Y'])