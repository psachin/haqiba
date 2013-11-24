from django import forms
from django.contrib.auth.models import User

# import emacshaqiba
from emacshaqiba.models import CodeTemplate, UserProfile
from emacshaqiba.models import BundleTemplate, Dependency

class CodeTemplateForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text="Name of code snippet.", required=True)
    gist_url = forms.URLField(
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text="GitHub gist url",
        required=False)
    code = forms.CharField(
        widget=forms.Textarea(attrs={'class':'form-control'}), 
        help_text="Type your code snippet here.", 
        required=True)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class':'form-control'}), 
        help_text="Type description of your code snippet here(Optional).", 
        required=False)
    screenshot = forms.ImageField(
        help_text="Upload screenshot of your code(Optional).", 
        required=False)
    
    class Meta:
        model = CodeTemplate
        exclude = ('user')      # to use instance.
        fields = ['name', 'description', 'gist_url', 'code','screenshot']

class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Please enter a username.")
    email = forms.CharField(help_text="Please enter your email.")
    password = forms.CharField(
        widget=forms.PasswordInput(), 
        help_text="Please enter a password.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    website = forms.URLField(help_text="Please enter your website.", 
                             required=False)
    picture = forms.ImageField(
        help_text="Select a profile image to upload.", 
        required=False)

    class Meta:
        model = UserProfile
        fields = ['website', 'picture']

class BundleTemplateForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text="Name of bundle.", required=True)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class':'form-control'}),         
        help_text="Description of bundle.", required=False)
    dep = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                         queryset = Dependency.objects.all(),
                                         error_messages={'required':'At-least one Dependency has to be included.'})
    config = forms.CharField(
        widget=forms.Textarea(attrs={'class':'form-control'}),
        required=False)
    screenshot = forms.ImageField(
        help_text="Upload screenshot of your Bundle(Optional).", 
        required=False)

    class Meta:
        model = BundleTemplate
        fields = ['name', 'description', 'dep', 'config', 'screenshot']

class PackageTemplateForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text="Name of bundle.", required=True)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class':'form-control'}),         
        help_text="Description of a Package.", required=False)
    loadpath = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'checked':'checked'}),
        required=False)
    require = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'checked':'checked'}),
        required=False)
    tarFile = forms.FileField(required=False)
    config = forms.CharField(
        widget=forms.Textarea(attrs={'class':'form-control'}),
        required=False)
    screenshot = forms.ImageField(
        help_text="Upload screenshot of your Package(Optional).", 
        required=False)

    class Meta:
        model = Dependency
        fields = ['name', 'description', 'loadpath', 'require', 'config',
                  'tarFile', 'screenshot']

