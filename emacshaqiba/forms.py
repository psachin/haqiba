from django import forms
from django.contrib.auth.models import User

# import emacshaqiba
from emacshaqiba.models import CodeTemplate, UserProfile

class CodeTemplateForm(forms.ModelForm):
    name = forms.CharField(help_text="Name of code snippet.", required=True)
    code = forms.CharField(widget=forms.Textarea, 
                          help_text="Type your code snippet here.", 
                          required=True)
    description = forms.CharField(widget=forms.TextInput, 
                                  help_text="Type description of your code snippet here(Optional).", 
                                  required=False)
    screenshot = forms.ImageField(help_text="Upload screenshot of your code(Optional).", required=False)
    
    class Meta:
        model = CodeTemplate
        exclude = ('user')      # to use instance.
        fields = ['name', 'description', 'code','screenshot']
        # widgets = {
        #     'code' : forms.TextInput(attrs={'id':'id_code'}),
        #     'name' : forms.TextInput(attrs={'class':'form-control'}),
        #     'description' : forms.Textarea(attrs={'class':'form-control'}),
        # }

class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Please enter a username.")
    email = forms.CharField(help_text="Please enter your email.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    website = forms.URLField(help_text="Please enter your website.", required=False)
    picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)

    class Meta:
        model = UserProfile
        fields = ['website', 'picture']


