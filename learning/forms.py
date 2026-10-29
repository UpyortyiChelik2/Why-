from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Submission

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ("answer",)
        widgets = {"answer": forms.Textarea(attrs={"rows": 7, "placeholder": "Опишіть ваше рішення..."} )}
