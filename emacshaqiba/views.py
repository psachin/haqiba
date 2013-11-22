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
    
    # Make a list of package with NO m2m relation.
    single_package = []
    for d in dependency:
        if not d.bundletemplate_set.filter().exists():
            single_package.append(d)

    if request.method == 'POST':
        make_temp_dir()
        
        selected_code_list = request.POST.getlist('selected_code_list')
        selected_package_list = request.POST.getlist('selected_package_list')
        selected_bundle_list = request.POST.getlist('selected_bundle_list')
        print "Code: %s" % selected_code_list
        print "Package: %s" % selected_package_list
        print "Bundle: %s" % selected_bundle_list

        if selected_code_list or selected_package_list or selected_bundle_list:
            init_file = open("init.el","w")
            init_file.write(instruction)
            
            if selected_code_list:
                for code in selected_code_list:
                    code = CodeTemplate.objects.get(name=code)
                    write_code_config(code, init_file)
            else:
                print "No code selected for download."

            #init_file = open("init.el","a")
    
            if selected_package_list:
                for package in selected_package_list:
                    package = Dependency.objects.get(name=package)
                    write_package_config(package, init_file)
            else:
                print "No package selected"

            if selected_bundle_list:
                for bundle in selected_bundle_list:
                    bundle = BundleTemplate.objects.get(name=bundle)
                    print bundle.name
                    init_file.write(";;; " + bundle.name + "\n")
                    increment_download_count(bundle)
                    for p in bundle.dep.all():
                        write_package_config(p, init_file)
                    # Write bundle related config code.
                    init_file.write(bundle.config + "\n\n")
            else:
                print "No Bundle selected."
            
            tar_data = make_tarball(init_file)
            return HttpResponse(tar_data, mimetype="application/x-gzip")
        else:
            print "Nothing selected."
    else:
        print "No POST request"
            
    context_dict = {
        'codetemplate': codetemplate,
        'dependency': single_package,
        'bundletemplate': bundletemplate,}
    return render_to_response('emacshaqiba/emacs_config.html', context_dict, context)

def write_package_config(package, init_file):
    dep_path = "media/%s" % package.tarFile
    if os.path.exists(dep_path):
        tar = tarfile.open(dep_path)
        tar.extractall(path="./temp/.emacs.d/")
        tar.close()
        init_file.write(";; " + package.name)
        temp_str = str(package.tarFile)
        temp_str2 = temp_str.split('/')[1].replace(".tar", "")
        load_path_string="\n" + "(add-to-list 'load-path \"" 
        end_str = "/\")"
        init_file.write(load_path_string)
        init_file.write(temp_str2)
        init_file.write(end_str + "\n")
        require_start_str="(require '"
        require_end_str=")"
        init_file.write(require_start_str)
        init_file.write(package.name)
        init_file.write(require_end_str + "\n")
        if package.config:
            init_file.write(package.config)
        init_file.write("\n\n")
        increment_download_count(package)
    else:
        print "path does not exist."

def write_code_config(code, init_file):
    init_file.write(";;; " + code.name)
    init_file.write(code.code)
    init_file.write("\n\n")
    increment_download_count(code)
    
def make_tarball(init_file):
    init_file.close()
    shutil.move('./init.el','./temp/.emacs.d/')
    tar = tarfile.open("emacs.d.tar","w")
    dep_path = "./temp/.emacs.d/"
    tar.add(dep_path, arcname=os.path.basename(".emacs.d"))
    tar.close()
    
    # Delete temp-space
    shutil.rmtree('./temp/.emacs.d/')
    # server tarball
    return open("emacs.d.tar", "rb")
            
def make_temp_dir():
    if not os.path.exists('./temp/.emacs.d/'):
        os.makedirs('./temp/.emacs.d/')
    else:
        shutil.rmtree('./temp/.emacs.d/')
        os.makedirs('./temp/.emacs.d/')
        
def increment_download_count(instance):
    count = instance.download_count + 1
    instance.download_count = count
    instance.save()
    
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
def editpackage_p(request, id=None):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    submitpackage_success="get"

    if id:
        print "Edit %s" % id 
        dependency = get_object_or_404(Dependency, pk=id)
        print dependency.user, dependency.name
        if dependency.user != request.user:
            return HttpResponseForbidden()
            
        if request.method == 'POST':
            print "POST"
            package_form = PackageTemplateForm(data=request.POST, instance=dependency)
            
            if package_form.is_valid():
                dependency = package_form.save(commit=False)
                if 'screenshot' in request.FILES:
                    dependency.screenshot = request.FILES['screenshot']

                dependency.save()
                submitpackage_success="success"
                print "Package edited successfully."
                return HttpResponseRedirect("/emacshaqiba/package/edit/")
            else:
                submitpackage_success="error"
                print package_form.errors
        else:
            print "GET"
            package_form = PackageTemplateForm(instance=dependency)

    else:
         return HttpResponse("Package does not exist!!")

    return render_to_response('emacshaqiba/editpackage_page.html', 
                              {'package_form': package_form,
                               'codetemplate': codetemplate,
                               'submitpackage_success': submitpackage_success},
                              context)

@login_required
def editbundle_p(request, id=None):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    success=True

    if id:
        print "Edit %s" % id
        bundle = get_object_or_404(BundleTemplate, pk=id)
        print bundle.user, bundle.name
        if bundle.user != request.user:
            return HttpResponseForbidden()

        if request.method == 'POST':
            print "Bundle POST."
            bundletemplate_form = BundleTemplateForm(data=request.POST, instance=bundle)

            if bundletemplate_form.is_valid():
                bundletemplate = bundletemplate_form.save(commit=False)
                if 'screenshot' in request.FILES:
                    bundletemplate.screenshot = request.FILES['screenshot']
                    
                #bundletemplate.user = request.user
                bundletemplate.save()
                bundletemplate_form.save_m2m()
                success = 'success'
                print "Bundle edit success"
                return HttpResponseRedirect("/emacshaqiba/bundle/edit/")
            else:
                success = 'error'
                print bundletemplate_form.errors
        else:
            print "Bundle GET"
            bundletemplate_form = BundleTemplateForm(instance=bundle)
    else:
        print "Bundle does not exist."

    context_dict = {'codetemplate': codetemplate,
                    'bundletemplate_form': bundletemplate_form,
                    'success': success,}
    return render_to_response('emacshaqiba/editbundle_page.html',
                              context_dict, 
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

@login_required
def delete_package(request, id):
    try:
        package = Dependency.objects.get(pk=id)
        package.delete()
        print "Package with id: %s deleted." % id
        return HttpResponseRedirect('/emacshaqiba/package/edit/')
    except:
        print "Package with id: %s not found!!" % id
        return HttpResponseRedirect('/emacshaqiba/package/edit/')

@login_required
def delete_bundle(request, id):
    try:
        bundle = BundleTemplate.objects.get(pk=id)
        bundle.delete()
        print "Bundle with id: %s deleted." % id
        return HttpResponseRedirect('/emacshaqiba/bundle/edit/')
    except:
        print "Bundle with id: %s not found!!" % id
        return HttpResponseRedirect('/emacshaqiba/bundle/edit/')        

def display_code(request, id):
    context = RequestContext(request)
    codetemplate_id = CodeTemplate.objects.get(pk=id)
    codetemplate = CodeTemplate.objects.order_by('-download_count')

    if request.POST:
        make_temp_dir()
        init_file = open("init.el","w")
        init_file.write(instruction)
        write_code_config(codetemplate_id, init_file)
        tar_data = make_tarball(init_file)
        return HttpResponse(tar_data, mimetype="application/x-gzip")
        
    context_dict = {'codetemplate': codetemplate,
                    'codetemplate_id':codetemplate_id,}

    return render_to_response('emacshaqiba/display_code.html', 
                              context_dict,
                              context)

def display_package(request, id):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    packages = Dependency.objects.order_by('-download_count')
    package_id = Dependency.objects.get(pk=id)

    if request.POST:
        make_temp_dir()
        init_file = open("init.el","w")
        init_file.write(instruction)
        write_package_config(package_id, init_file)
        tar_data = make_tarball(init_file)
        return HttpResponse(tar_data, mimetype="application/x-gzip")

    context_dict = {'codetemplate': codetemplate,
                    'package_id': package_id,}

    return render_to_response('emacshaqiba/display_package.html', 
                              context_dict,
                              context)    

def display_bundle(request, id):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    bundle_id = BundleTemplate.objects.get(pk=id)

    context_dict = {'codetemplate': codetemplate,
                    'bundle': bundle_id,}

    return render_to_response('emacshaqiba/display_bundle.html', 
                              context_dict,
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
                    'bundletemplate_form': bundletemplate_form,
                    'success': success,}
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
    dependency_user = Dependency.objects.filter(user=request.user)
    bundle_user = BundleTemplate.objects.filter(user=request.user)

    context_dict = {'codetemplate': codetemplate,
                    'codetemplate_user': codetemplate_user,
                    'dependency_user': dependency_user,
                    'bundle_user': bundle_user,}
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

