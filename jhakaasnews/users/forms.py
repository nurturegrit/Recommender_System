from django import forms
from .models import User

class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'date_of_birth', 'gender']  # Add the fields you want to collect
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields required as needed
        self.fields['name'].required = True
        self.fields['date_of_birth'].required = True
        self.fields['gender'].required = True