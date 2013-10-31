from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse

# import models
from emacshaqiba.models import CodeTemplate, UserProfile

# import forms
from emacshaqiba.forms import CodeTemplateForm, UserForm, UserProfileForm

def encode_url(string):
    if ' ' or '-' in string:
        return string.replace(' ', 'SPACE').replace('-', 'HYPHEN')
    else:
        return string

def decode_url(string):
    if 'SPACE' or 'HYPHEN' in string:
        return string.replace('SPACE', ' ').replace('HYPHEN','-')
    else:
        return string

def index(request):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    #code_list = get_code_list()
    context_dict = {'codetemplate':codetemplate,}
    return render_to_response('emacshaqiba/index.html', context_dict ,context)

def emacs_config(request):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    # code_list = get_code_list()
    
    if request.method == 'POST':
        selected_code_list = request.POST.getlist('selected_code_list')
        if selected_code_list:
            response = HttpResponse(content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename=emacs_init.el'
            for e in selected_code_list:
                CODE = CodeTemplate.objects.filter(name=e)
                for i in CODE:
                    response.write(";;; " + i.name + "\n" + i.code + "\n\n")
                    print i.name, i.download_count
                    temp_codetemplate = CodeTemplate.objects.get(name=i.name)
                    count = temp_codetemplate.download_count + 1
                    temp_codetemplate.download_count = count
                    temp_codetemplate.save()
            return response
        else:
            print "No code selected for download."
    else:
        print "No POST request"

    context_dict = {'codetemplate': codetemplate,}
    return render_to_response('emacshaqiba/emacs_config.html', context_dict, context)

def about(request):
    context = RequestContext(request)
    # code_list = get_code_list()
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    context_dict = {'codetemplate': codetemplate,}
    return render_to_response('emacshaqiba/about.html', context_dict , context)

def get_code_list():
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    for e in codetemplate:
        e.url = encode_url(e.name)
        if e.download_count == None:
            e.download_count = 0
    return codetemplate

@login_required
def submitcode(request):
    context = RequestContext(request)
    # code_list = get_code_list()
    
    submitcode_success="get"
    
    if request.method == 'POST':
        codetemplate_form = CodeTemplateForm(data=request.POST)

        if codetemplate_form.is_valid():
            codetemplate = codetemplate_form.save(commit=False)
            if 'screenshot' in request.FILES:
                codetemplate.screenshot = request.FILES['screenshot']
            
            print request.user
            codetemplate.user = request.user
            codetemplate.save()
            submitcode_success="success"
        else:
            submitcode_success="error"
            print codetemplate_form.errors
    else:
        codetemplate_form = CodeTemplateForm()
    
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    return render_to_response('emacshaqiba/submitcode.html', 
                              {'codetemplate_form': codetemplate_form,
                               'codetemplate': codetemplate,
                               'submitcode_success': submitcode_success,},
                              context)

@login_required
def editcode(request, delete_success=False):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    codetemplate_user = CodeTemplate.objects.filter(user=request.user)

    return render_to_response('emacshaqiba/editcode.html', 
                              {'codetemplate':codetemplate,
                               'codetemplate_user': codetemplate_user},
                              context)
    
@login_required
def editcode_p(request, id=None):
    context = RequestContext(request)
    # code_list = get_code_list()
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    submitcode_success="get"

    if id:
        print "Edit %s" % id 
        code_template = get_object_or_404(CodeTemplate, pk=id)
        print code_template.user, code_template.name
        if code_template.user != request.user:
            return HttpResponseForbidden()
            
        if request.method == 'POST':
            print "POST"
            codetemplate_form = CodeTemplateForm(data=request.POST, instance=code_template)
            
            if codetemplate_form.is_valid():
                codetemplate = codetemplate_form.save(commit=False)
                if 'screenshot' in request.FILES:
                    codetemplate.screenshot = request.FILES['screenshot']

                codetemplate.save()
                submitcode_success="success"
                print "Code edited successfully."
                return HttpResponseRedirect("/emacshaqiba/edit_code/")
                # return HttpResponseRedirect("/emacshaqiba/edit_code/%s" % id)
            else:
                submitcode_success="error"
                print codetemplate_form.errors
        else:
            print "GET"
            codetemplate_form = CodeTemplateForm(instance=code_template)

    else:
         return HttpResponse("Code does not exist!!")

    return render_to_response('emacshaqiba/editcode_page.html', 
                              {'codetemplate_form': codetemplate_form,
                               'codetemplate':codetemplate,
                               'submitcode_success':submitcode_success},
                              context)

@login_required
def delete_code(request, id):
    try:
        codetemplate = CodeTemplate.objects.get(pk=id)
        codetemplate.delete()
        print "code with id: %s Delete." % id
        return HttpResponseRedirect('/emacshaqiba/edit_code/')
    except:
        print "code with id: %s not found!!" % id
        return HttpResponseRedirect('/emacshaqiba/edit_code/')

def display_code(request, id):
    context = RequestContext(request)
    #code_name = decode_url(code_name)
    codetemplate_id = CodeTemplate.objects.filter(pk=id)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    #code_list = get_code_list()
        
    context_dict = {'codetemplate': codetemplate,
                    'codetemplate_id':codetemplate_id,}

    return render_to_response('emacshaqiba/display_code.html', 
                              context_dict,
                              context)

def register(request):
    if request.session.test_cookie_worked():
        print ">>>> TEST COOKIE WORKED"
        request.session.delete_test_cookie()
        
    #code_list = get_code_list()
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    # A boolean value for telling the template whether the
    # registration was successful.  Set to False initially. Code
    # changes value to True when registration succeeds.
    registered = False
    form_error = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.  Since we need to
            # set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid
            # integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?  If so, we need
            # to get it from the input form and put it in the
            # UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration
            # was successful.
            registered = True
            
        
        # Invalid form or forms - mistakes or something else?  Print
        # problems to the terminal.  They'll also be shown to the
        # user.
        else:
            if user_form.errors or profile_form.errors:
                form_error = True
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm
    # instances.  These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response( 
        'emacshaqiba/register.html', 
        {'user_form': user_form, 
         'profile_form': profile_form, 
         'registered': registered,
         'form_error': form_error,
         'codetemplate': codetemplate,}, 
        context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    # code_list = get_code_list()
    context_dict = {'codetemplate': codetemplate,}
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            context_dict['bad_details'] = True
            return render_to_response('emacshaqiba/login.html', context_dict, context)

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('emacshaqiba/login.html', context_dict, context)

@login_required
def profile(request):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    codetemplate_user = CodeTemplate.objects.filter(user=request.user)
    # code_list = get_code_list()
    context_dict = {'codetemplate': codetemplate,
                    'codetemplate_user': codetemplate_user,}
    u = User.objects.get(username=request.user)

    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None

    context_dict['user'] = u
    context_dict['userprofile'] = up
    return render_to_response('emacshaqiba/profile.html', context_dict, context)

@login_required
def user_logout(request):
    # Like before, obtain the request's context.
    context = RequestContext(request)

    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

