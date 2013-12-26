from django import forms
from django.contrib.auth.models import User

# import emacshaqiba
from emacshaqiba.models import CodeTemplate, UserProfile
from emacshaqiba.models import BundleTemplate, Dependency

# Extra libs
import urllib2

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
        required=False)
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

    def clean(self):
        cleaned_data = super(CodeTemplateForm, self).clean()
        if cleaned_data.get('gist_url'):
            print "Got gist_url"
            self.clean_gist_url()
        elif cleaned_data.get('code'):
            print "Got code"
            self.clean_code()
        else:
            msg = u"At least this field is required."
            self._errors["code"] = self.error_class([msg])
            #raise forms.ValidationError("At least ONE field is required.")
        return cleaned_data

    def clean_gist_url(self):
        if self.cleaned_data['gist_url']:
            url = self.cleaned_data['gist_url']
            try:
                urllib2.urlopen(self.cleaned_data['gist_url'])
                return url
            except urllib2.HTTPError, error:
                raise forms.ValidationError("Unable to fetch gist, check your URL.")
        else:
            pass

    def clean_code(self):
        if self.cleaned_data['code']:
            code = self.cleaned_data['code']
            return code
        else:
            pass

class UserForm(forms.ModelForm):
    username = forms.CharField(
        label = '',
        widget=forms.TextInput(
            attrs={'class':'form-control',
                   'placeholder': 'Username.'}),
        required=True,
        error_messages={'required':'Username is required.'})
    
    email = forms.EmailField(
        label = '',
        widget=forms.TextInput(
            attrs={'class':'form-control',
                   'placeholder': 'Valid Email address.'}),
        required=True,
        error_messages={'required':'Valid Email address is required.'})
    
    password = forms.CharField(
        label = '',
        widget=forms.PasswordInput(
            attrs={'class':'form-control',
                   'placeholder': 'Password.'}),
        required=True,
        error_messages={'required':'Password is missing.'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    website = forms.URLField(
        label = '',
        widget=forms.TextInput(
            attrs={'class':'form-control',
                   'placeholder': 'Website address(Optional).'}),
        required=False)
    
    picture = forms.ImageField(
        label = 'Profile photo',
        help_text="Select a profile photo to upload.", 
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

    def clean_tarFile(self):
        if self.cleaned_data['tarFile']:
            return self.cleaned_data['tarFile']
        else:
            raise forms.ValidationError("Tarball of a package is required.")
