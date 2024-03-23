from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['role'].disabled = True

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'role', 'photo', 'username']
