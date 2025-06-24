from django import forms
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField
from captcha.fields import CaptchaField


User = get_user_model()

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'last_name', 'email', 'password']
        widgets = {'password': forms.PasswordInput()}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


from django import forms

class ContactAdminForm(forms.Form):
    your_email = forms.EmailField(label="Email manzilingiz", disabled=True)
    subject = forms.CharField(max_length=100, label="Mavzu")
    message = forms.CharField(widget=forms.Textarea, label="Xabar")

    def __init__(self, *args, **kwargs):
        user_email = kwargs.pop('user_email', None)
        super().__init__(*args, **kwargs)
        if user_email:
            self.fields['your_email'].initial = user_email

from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'bio', 'image']

