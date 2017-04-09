from django.forms import ModelForm
from . models import User

from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name']

class UserCreationForm ( forms.ModelForm ) :

    password1 = forms.CharField( label = 'Password', widget = forms.PasswordInput )
    password2 = forms.CharField( label = 'Password confirmation', widget = forms.PasswordInput )

    class Meta :
        model = User
        fields = ( 'email', 'first_name', )

    def clean_password2 ( self ) :
        # Check that the two password entries match
        password1 = self.cleaned_data.get( "password1" )
        password2 = self.cleaned_data.get( "password2" )
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError( "Passwords don't match" )
        return password1

    def save( self, commit = True ) :
        # Save the provided password in hashed format
        user = super( UserCreationForm, self ).save( commit = False )
        user.set_password( self.cleaned_data[ "password1" ] )
        if commit:
            user.save()
        return user
