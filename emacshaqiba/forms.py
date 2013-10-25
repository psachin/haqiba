from django import forms

from emacshaqiba.models import CodeTemplate

class CodeTemplateForm(forms.ModelForm):
    name = forms.CharField(help_text="Name of code snippet.", required=True)
    code = forms.CharField(widget=forms.TextInput, 
                          help_text="Type your code snippet here.", 
                          required=True)
    screenshot = forms.ImageField(help_text="Upload screenshot of your code.", required=False)
    
    class Meta:
        model = CodeTemplate
        fields = ['name', 'code', 'screenshot']
