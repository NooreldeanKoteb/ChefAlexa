from django import forms
from .models import user

# from .models import home

class homeForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ('name', 'email')

class userForm(forms.ModelForm):
    class Meta:
        model = user

        fields = '__all__'







