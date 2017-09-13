from django import forms
# from home.models import Registration
from teacher.models import Teacher
from student.models import Student
from variables.models import Country, Subject_Expertise, Level_Expertise, Educational_Level, Education, Region, Education_School, Expertise_Type
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField, Field, Reset, HTML, Button
from crispy_forms.bootstrap import TabHolder, Tab, InlineCheckboxes, AppendedText, InlineRadios


class ContactForm(forms.Form):
	full_name = forms.CharField(required=False)
	email = forms.EmailField()
	message = forms.CharField(widget=forms.Textarea)

