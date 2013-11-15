from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse

# additional python libs
import os, tarfile, shutil

# import models
from emacshaqiba.models import CodeTemplate, UserProfile
from emacshaqiba.models import BundleTemplate, Dependency
# import forms
from emacshaqiba.forms import CodeTemplateForm, UserForm, UserProfileForm
from emacshaqiba.forms import BundleTemplateForm, PackageTemplateForm
# import init file template
from template import instruction

def index(request):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    context_dict = {'codetemplate':codetemplate,}
    return render_to_response('emacshaqiba/index.html', context_dict ,context)

def emacs_config(request):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    dependency = Dependency.objects.order_by('download_count')
    bundletemplate = BundleTemplate.objects.order_by('-download_count')

    if request.method == 'POST':
        selected_code_list = request.POST.getlist('selected_code_list')
        if selected_code_list:
            response = HttpResponse(content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename=emacs_init.el'
            response.write(instruction + "\n")
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

    context_dict = {
        'codetemplate': codetemplate,
        'dependency': dependency,
        'bundletemplate': bundletemplate,}
    return render_to_response('emacshaqiba/emacs_config.html', context_dict, context)

def about(request):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    context_dict = {'codetemplate': codetemplate,}
    return render_to_response('emacshaqiba/about.html', context_dict , context)

@login_required
def submitcode(request):
    context = RequestContext(request)
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
def editpackage(request, delete_success=False):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    dependency = Dependency.objects.order_by('-download_count')
    dependency_user = Dependency.objects.filter(user=request.user)

    return render_to_response('emacshaqiba/editpackage.html', 
                              {'codetemplate':codetemplate,
                               'dependency': dependency,
                               'dependency_user': dependency_user},
                              context)    

@login_required
def editbundle(request, delete_success=False):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    bundle = BundleTemplate.objects.order_by('-download_count')
    bundle_user = BundleTemplate.objects.filter(user=request.user)

    return render_to_response('emacshaqiba/editbundle.html', 
                              {'codetemplate':codetemplate,
                               'bundle': bundle,
                               'bundle_user': bundle_user},
                              context)    
    
@login_required
def editcode_p(request, id=None):
    context = RequestContext(request)
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
                return HttpResponseRedirect("/emacshaqiba/code/edit/")
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
        print "code with id: %s deleted." % id
        return HttpResponseRedirect('/emacshaqiba/code/edit/')
    except:
        print "code with id: %s not found!!" % id
        return HttpResponseRedirect('/emacshaqiba/code/edit/')

def display_code(request, id):
    context = RequestContext(request)
    codetemplate_id = CodeTemplate.objects.filter(pk=id)
    codetemplate = CodeTemplate.objects.order_by('-download_count')

    if request.POST:
        for i in codetemplate_id:
            response = HttpResponse(content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename=emacs_init.el'
            response.write(instruction + "\n")
            response.write(";;; " + i.name + "\n" + i.code + "\n\n")
            print i.name, i.download_count
            temp_codetemplate = CodeTemplate.objects.get(name=i.name)
            count = temp_codetemplate.download_count + 1
            temp_codetemplate.download_count = count
            temp_codetemplate.save()
        return response
    
    context_dict = {'codetemplate': codetemplate,
                    'codetemplate_id':codetemplate_id,}

    return render_to_response('emacshaqiba/display_code.html', 
                              context_dict,
                              context)

def display_bundle(request, id):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    bundle = BundleTemplate.objects.filter(pk=id).order_by('-download_count')

    
    context_dict = {'codetemplate': codetemplate,
                    'bundle':bundle,}

    return render_to_response('emacshaqiba/display_bundle.html', 
                              context_dict,
                              context)
    
@login_required
def delete_bundle(request, id):
    try:
        bundle = Dependency.objects.get(pk=id)
        bundle.delete()
        print "Bundle with id: %s deleted." % id
        return HttpResponseRedirect('/emacshaqiba/bundle/edit/')
    except:
        print "Bundle with id: %s not found!!" % id
        return HttpResponseRedirect('/emacshaqiba/bundle/edit/')
        
def displayBundle(request):
    """Dirty code, may not work(or misbehave) with multisessions.

    """
    context = RequestContext(request)
    bundle = BundleTemplate.objects.all()
    
    
    if os.path.exists('./temp/.emacs.d/'):
        shutil.rmtree('./temp/.emacs.d/')
        os.makedirs('./temp/.emacs.d/')
    else:
        print "No such dir."
        os.makedirs('./temp/.emacs.d/')

    selected_code_list = CodeTemplate.objects.filter(pk=1)
    if selected_code_list:
        init_file = open("init.el","w")
        for code in selected_code_list:
            init_file.write(code.code)
        init_file.close()

    init_file = open("init.el","a")
    for b in bundle:
        # print b.name, b.user, b.description, b.config, b.screenshot, b.download_count
        # print b.id
            
        dependency = Dependency.objects.filter(bundletemplate=b.id)
        for d in dependency:
            # print d.name
            dep_path = "media/%s" % d.tarFile
            # print d.tarFile
            if os.path.exists(dep_path):
                tar = tarfile.open(dep_path)
                tar.extractall(path="./temp/.emacs.d/")
                tar.close()
                # (add-to-list 'load-path "emacs-epc/")
                temp_str = str(d.tarFile)
                temp_str2 = temp_str.split('/')[1].split(".")[0]
                load_path_string="\n" + "(add-to-list 'load-path \"" 
                end_str = "/\")"
                init_file.write(load_path_string)
                init_file.write(temp_str2)
                init_file.write(end_str)

        init_file.write("\n\n")        
        init_file.write(b.config)

    init_file.close()
    shutil.move('./init.el','./temp/.emacs.d/')    
    tar = tarfile.open("emacs.d.tar","w")
    dep_path = "./temp/.emacs.d/"
    tar.add(dep_path, arcname=os.path.basename(".emacs.d"))
    tar.close()

    # server tarball
    tar_data = open("emacs.d.tar", "rb")
    return HttpResponse(tar_data, mimetype="application/x-gzip")

    
    context_dict = {'bundle':bundle,}
    return render_to_response('emacshaqiba/display_bundle.html', context_dict, 
                              context)

@login_required
def submit_bundle(request):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    success=True

    if request.method == 'POST':
        bundletemplate_form = BundleTemplateForm(data=request.POST)

        if bundletemplate_form.is_valid():
            bundletemplate = bundletemplate_form.save(commit=False)
            if 'screenshot' in request.FILES:
                bundletemplate.screenshot = request.FILES['screenshot']
                
            bundletemplate.user = request.user
            bundletemplate.save()
            bundletemplate_form.save_m2m()
            success = 'success'
        else:
            success = 'error'
            print bundletemplate_form.errors
    else:
        bundletemplate_form = BundleTemplateForm()

    context_dict = {'codetemplate': codetemplate,
                    'bundletemplate_form': bundletemplate_form,}
    return render_to_response('emacshaqiba/submit_bundle.html', context_dict, 
                              context)

@login_required
def submit_package(request):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    success = False

    if request.method == 'POST':
        packagetemplate_form = PackageTemplateForm(data=request.POST)
        # FIXME: tarFile is required
        if packagetemplate_form.is_valid():
            packagetemplate = packagetemplate_form.save(commit=False)
            if 'tarFile' in request.FILES:
                packagetemplate.tarFile = request.FILES['tarFile']
            
            packagetemplate.user = request.user
            packagetemplate.save()
            success = "success"
        else:
            success = "error"
            packagetemplate_form.errors
    else:
        packagetemplate_form = PackageTemplateForm()
        
    context_dict = {'packagetemplate_form': packagetemplate_form,
                    'codetemplate': codetemplate,
                    'success': success,}
    return render_to_response('emacshaqiba/submit_package.html', context_dict, 
                              context)

def register(request):
    if request.session.test_cookie_worked():
        print ">>>> TEST COOKIE WORKED"
        request.session.delete_test_cookie()
        
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

