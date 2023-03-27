from datetime import datetime

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import ToDoModel, MyUser
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class ToDoUser(ModelForm):
    class Meta:
        model = ToDoModel
        fields = ('title', 'content', 'date_ending')
        widgets = {
            'date_ending': DateTimePickerInput()}

    def clean(self):
        date_ending = self.cleaned_data['date_ending']
        if date_ending <= datetime.now(date_ending.tzinfo):
            raise forms.ValidationError(_('Enter correct date'))
        return super().clean()


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label=_('Login'),
                               widget=forms.TextInput(
                                   attrs={'class': 'form-input'}))
    password = forms.CharField(label=_('Password'),
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-input'}))


class RegistrationCustomUserForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'photo')


class UpdateCustomUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'photo')