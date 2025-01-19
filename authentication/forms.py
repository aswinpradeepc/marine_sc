from django import forms

from authentication.models import User


class SignUpForm(forms.ModelForm):
    full_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address', required=True)
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    mobile_number = forms.CharField(max_length=15, help_text='Enter your mobile number', required=True)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'gender', 'mobile_number')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        if User.objects.filter(mobile_number=mobile_number).exists():
            raise forms.ValidationError("Mobile number already exists")
        return mobile_number
