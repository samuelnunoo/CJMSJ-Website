from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Profile


from .models import Account, Profile

class LoginForm(AuthenticationForm):
    username=forms.CharField(label='', max_length=254, widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'form-control'}))




class SignUpForm(UserCreationForm):
    email=forms.EmailField(max_length=50,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','type':'password'}))
    password2 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','type':'password'}))

    class Meta:
        model=Account
        fields=('email','password1','password2')



class AccountChangeForm(UserChangeForm):

    class Meta:
        model = Account
        fields = ( 'email',)



class ProfileForm(forms.ModelForm):

    class Meta:
        model=Profile
        fields=('first_name','last_name','bio','image')

        widgets={
            'first_name':forms.TextInput( attrs={'class':'form-control my-4','placeholder':'First Name'}),
            'last_name':forms.TextInput( attrs={'class':'form-control my-4','placeholder':'Last Name'}),
            'bio':forms.Textarea(attrs={'class':'form-control'}),
        }





