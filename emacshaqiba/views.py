from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

# import models
from emacshaqiba.models import CodeTemplate

# import forms
from emacshaqiba.forms import CodeTemplateForm

def index(request):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.all()
    context_dict = {'codetemplate':codetemplate}
    return render_to_response('emacshaqiba/index.html', context_dict ,context)


def submitcode(request):
    context = RequestContext(request)
    
    if request.method == 'POST':
        codetemplate_form = CodeTemplateForm(data=request.POST)
        
        if codetemplate_form.is_valid():
            codetemplate = codetemplate_form.save(commit=False)
            if 'screenshot' in request.FILES:
                codetemplate.screenshot = request.FILES['screenshot']
                
            codetemplate.save()
        else:
            print codetemplate_form.errors
            
    else:
        codetemplate_form = CodeTemplateForm()
            
    return render_to_response('emacshaqiba/submitcode.html', 
                              {'codetemplate_form': codetemplate_form,}, 
                              context)
            

