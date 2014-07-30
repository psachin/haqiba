from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.contrib import messages

# additional python libs
import os
import tarfile
import shutil
from loadGist import load_gist

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
    packages = Dependency.objects.order_by('-download_count')
    bundles = BundleTemplate.objects.order_by('-download_count')

    context_dict = {'codetemplate': codetemplate,
                    'packages': packages,
                    'bundles': bundles}
    return render_to_response('emacshaqiba/index.html', context_dict, context)


def emacs(request):
    context = RequestContext(request)

    if request.session.session_key == None:
        request.session['has_session'] = True
    else:
        session_key = request.session.session_key
        
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    packages = Dependency.objects.order_by('-download_count')
    bundles = BundleTemplate.objects.order_by('-download_count')

    # Make a list of package with NO m2m relation.
    single_package = []
    for d in packages:
        if not d.bundletemplate_set.filter().exists():
            single_package.append(d)

    if request.method == 'POST':
        selected_code_list = request.POST.getlist('selected_code_list')
        selected_package_list = request.POST.getlist('selected_package_list')
        selected_bundle_list = request.POST.getlist('selected_bundle_list')
        print "Code: %s" % selected_code_list
        print "Package: %s" % selected_package_list
        print "Bundle: %s" % selected_bundle_list

        if selected_code_list or selected_package_list or selected_bundle_list:
            init_file = make_init(session_key)

            if selected_code_list:
                for code in selected_code_list:
                    code = CodeTemplate.objects.get(name=code)
                    write_code_config(code, init_file)
            else:
                print "No code selected for download."

            if selected_package_list:
                for package in selected_package_list:
                    package = Dependency.objects.get(name=package)
                    write_package_config(package, init_file, session_key)
            else:
                print "No package selected"

            if selected_bundle_list:
                for bundle in selected_bundle_list:
                    bundle = BundleTemplate.objects.get(name=bundle)
                    # print bundle.name
                    write_bundle_config(bundle, init_file, session_key)
            else:
                print "No Bundle selected."

            tar_data = make_tarball(init_file, session_key)
            response = HttpResponse(tar_data, mimetype="application/x-gzip")
            response['Content-Disposition'] = 'attachment; filename="emacs.d.tar"'
            return response
        else:
            print "Nothing selected."
    else:
        print "No POST request"

    context_dict = {
        'codetemplate': codetemplate,
        'packages': packages,
        'bundles': bundles,
        'dependency': single_package}
    return render_to_response('emacshaqiba/emacs.html', context_dict, context)


def write_package_config(package, init_file, session_key):
    dep_path = "media/%s" % package.tarFile
    if os.path.exists(dep_path):
        tar = tarfile.open(dep_path)
        tar.extractall(path="./temp/" + session_key + "/.emacs.d/")
        tar.close()
        init_file.write(";; " + package.name + "\n")
        if package.loadpath:
            temp_str = str(package.tarFile)
            temp_str2 = temp_str.split('/')[1].replace(".tar", "")
            load_path_string = "\n" + "(add-to-list 'load-path \"~/.emacs.d/"
            end_str = "/\")"
            init_file.write(load_path_string)
            init_file.write(temp_str2)
            init_file.write(end_str + "\n")
        if package.require:
            require_start_str = "(require '"
            require_end_str = ")"
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
    init_file.write(";;; " + code.name + "\n")
    init_file.write(code.code)
    init_file.write("\n\n")
    increment_download_count(code)


def write_bundle_config(bundle, init_file, session_key):
    init_file.write(";;; " + bundle.name + "\n")
    for p in bundle.dep.all():
        write_package_config(p, init_file, session_key)
    # Write bundle related config code.
    init_file.write(bundle.config + "\n\n")
    increment_download_count(bundle)


def make_init(session_key):
    make_temp_dir(session_key)
    init_file = open("./temp/" + session_key + "/.emacs.d/init.el", "w")
    init_file.write(instruction)
    return init_file


def make_tarball(init_file, session_key):
    init_file.close()
    # shutil.move('./init.el', './temp/' + session_key + '/.emacs.d/')
    tar = tarfile.open("emacs.d.tar", "w")
    dep_path = "./temp/" + session_key + "/.emacs.d/"
    tar.add(dep_path, arcname=os.path.basename(".emacs.d"))
    tar.close()

    # move tarball
    # shutil.move("emacs.d.tar", './temp/' + session_key + '/')
    
    # Delete temp-space
    shutil.rmtree('./temp/' + session_key)
    # server tarball
    return open("emacs.d.tar", "r")


def make_temp_dir(session_key):
    if not os.path.exists('./temp/' + session_key + '/.emacs.d/'):
        os.makedirs('./temp/' + session_key + '/.emacs.d/')
    else:
        shutil.rmtree('./temp/' + session_key)
        os.makedirs('./temp/' + session_key + '/.emacs.d/')


def increment_download_count(instance):
    count = instance.download_count + 1
    instance.download_count = count
    instance.save()


def about(request):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    packages = Dependency.objects.order_by('-download_count')
    bundles = BundleTemplate.objects.order_by('-download_count')

    context_dict = {'codetemplate': codetemplate,
                    'packages': packages,
                    'bundles': bundles}

    return render_to_response('emacshaqiba/about.html', context_dict, context)


@login_required
def submitcode(request):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    packages = Dependency.objects.order_by('-download_count')
    bundles = BundleTemplate.objects.order_by('-download_count')

    if request.method == 'POST':
        codetemplate_form = CodeTemplateForm(data=request.POST)

        if codetemplate_form.is_valid():
            codetemplate = codetemplate_form.save(commit=False)

            if codetemplate.gist_url:
                code_from_gist = load_gist(codetemplate.gist_url)
                codetemplate.code = code_from_gist
            else:
                codetemplate.code = request.POST['code']

            if 'screenshot' in request.FILES:
                codetemplate.screenshot = request.FILES['screenshot']

            print request.user
            codetemplate.user = request.user
            codetemplate.save()
            messages.success(request, "Code submitted successfully !!")
            url = reverse('emacshaqiba.views.submitcode')
            return HttpResponseRedirect(url)
        else:
            print codetemplate_form.errors
            messages.error(request, "Error: Submitting code!")
    else:
        codetemplate_form = CodeTemplateForm()

    context_dict = {'codetemplate_form': codetemplate_form,
                    'codetemplate': codetemplate,
                    'packages': packages,
                    'bundles': bundles}

    return render_to_response('emacshaqiba/submitcode.html',
                              context_dict,
                              context)


@login_required
def editcode(request, delete_success=False):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    packages = Dependency.objects.order_by('-download_count')
    bundles = BundleTemplate.objects.order_by('-download_count')

    context_dict = {'codetemplate_user':
                    codetemplate.filter(user=request.user),
                    'codetemplate': codetemplate,
                    'packages': packages,
                    'bundles': bundles}

    return render_to_response('emacshaqiba/editcode.html',
                              context_dict,
                              context)


@login_required
def editpackage(request, delete_success=False):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    packages = Dependency.objects.order_by('-download_count')
    bundles = BundleTemplate.objects.order_by('-download_count')

    context_dict = {'package_user': packages.filter(user=request.user),
                    'codetemplate': codetemplate,
                    'packages': packages,
                    'bundles': bundles}

    return render_to_response('emacshaqiba/editpackage.html',
                              context_dict,
                              context)


@login_required
def editbundle(request, delete_success=False):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    packages = Dependency.objects.order_by('-download_count')
    bundles = BundleTemplate.objects.order_by('-download_count')

    context_dict = {'bundle_user': bundles.filter(user=request.user),
                    'codetemplate': codetemplate,
                    'packages': packages,
                    'bundles': bundles}

    return render_to_response('emacshaqiba/editbundle.html',
                              context_dict,
                              context)


@login_required
def editcode_p(request, id=None):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    packages = Dependency.objects.order_by('-download_count')
    bundles = BundleTemplate.objects.order_by('-download_count')

    if id:
        print "Edit %s" % id
        code_template = get_object_or_404(CodeTemplate, pk=id)
        print code_template.user, code_template.name
        if code_template.user != request.user:
            return HttpResponseForbidden()

        if request.method == 'POST':
            codetemplate_form = CodeTemplateForm(data=request.POST,
                                                 instance=code_template)

            if codetemplate_form.is_valid():
                codetemplate = codetemplate_form.save(commit=False)

                if codetemplate.gist_url:
                    code_from_gist = load_gist(codetemplate.gist_url)
                    codetemplate.code = code_from_gist
                else:
                    codetemplate.code = request.POST['code']

                if 'screenshot' in request.FILES:
                    codetemplate.screenshot = request.FILES['screenshot']

                codetemplate.save()
                print "Code edited successfully."
                return HttpResponseRedirect("/emacshaqiba/code/edit/")
            else:
                print codetemplate_form.errors
                messages.error(request, "Error: Saving changes!")
        else:
            print "GET"
            codetemplate_form = CodeTemplateForm(instance=code_template)

    else:
        return HttpResponse("Code does not exist!!")

    context_dict = {'codetemplate_form': codetemplate_form,
                    'codetemplate': codetemplate,
                    'packages': packages,
                    'bundles': bundles}

    return render_to_response('emacshaqiba/editcode_page.html',
                              context_dict,
                              context)


@login_required
def editpackage_p(request, id=None):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    packages = Dependency.objects.order_by('-download_count')
    bundles = BundleTemplate.objects.order_by('-download_count')

    if id:
        print "Edit %s" % id
        dependency = get_object_or_404(Dependency, pk=id)
        print dependency.user, dependency.name
        if dependency.user != request.user:
            return HttpResponseForbidden()

        if request.method == 'POST':
            print "POST"
            package_form = PackageTemplateForm(data=request.POST,
                                               instance=dependency)

            if package_form.is_valid():
                dependency = package_form.save(commit=False)
                if 'screenshot' in request.FILES:
                    dependency.screenshot = request.FILES['screenshot']

                dependency.save()
                print "Package edited successfully."
                return HttpResponseRedirect("/emacshaqiba/package/edit/")
            else:
                print package_form.errors
                messages.error(request, "Error: Saving changes!")
        else:
            print "GET"
            package_form = PackageTemplateForm(instance=dependency)
    else:
        return HttpResponse("Package does not exist!!")

    context_dict = {'package_form': package_form,
                    'codetemplate': codetemplate,
                    'packages': packages,
                    'bundles': bundles}

    return render_to_response('emacshaqiba/editpackage_page.html',
                              context_dict,
                              context)


@login_required
def editbundle_p(request, id=None):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    packages = Dependency.objects.order_by('-download_count')
    bundles = BundleTemplate.objects.order_by('-download_count')

    if id:
        print "Edit %s" % id
        bundle = get_object_or_404(BundleTemplate, pk=id)
        print bundle.user, bundle.name
        if bundle.user != request.user:
            return HttpResponseForbidden()

        if request.method == 'POST':
            print "Bundle POST."
            bundletemplate_form = BundleTemplateForm(data=request.POST,
                                                     instance=bundle)

            if bundletemplate_form.is_valid():
                bundletemplate = bundletemplate_form.save(commit=False)
                if 'screenshot' in request.FILES:
                    bundletemplate.screenshot = request.FILES['screenshot']

                #bundletemplate.user = request.user
                bundletemplate.save()
                bundletemplate_form.save_m2m()
                print "Bundle edit success"
                return HttpResponseRedirect("/emacshaqiba/bundle/edit/")
            else:
                print bundletemplate_form.errors
                messages.error(request, "Error: Saving changes!")
        else:
            print "Bundle GET"
            bundletemplate_form = BundleTemplateForm(instance=bundle)
    else:
        print "Bundle does not exist."

    context_dict = {'bundletemplate_form': bundletemplate_form,
                    'codetemplate': codetemplate,
                    'packages': packages,
                    'bundles': bundles}

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

    if request.session.session_key == None:
        request.session['has_session'] = True
    else:
        session_key = request.session.session_key

    codetemplate = CodeTemplate.objects.order_by('-download_count')
    packages = Dependency.objects.order_by('-download_count')
    bundles = BundleTemplate.objects.order_by('-download_count')

    if request.POST:
        init_file = make_init(session_key)
        write_code_config(codetemplate.get(pk=id), init_file)
        tar_data = make_tarball(init_file, session_key)
        response = HttpResponse(tar_data, mimetype="application/x-gzip")
        response['Content-Disposition'] = 'attachment; filename="emacs.d.tar"'
        return response

    context_dict = {'codetemplate': codetemplate,
                    'packages': packages,
                    'bundles': bundles,
                    'codetemplate_id': codetemplate.get(pk=id)}

    return render_to_response('emacshaqiba/display_code.html',
                              context_dict,
                              context)


def get_code_list(max_results=0, starts_with=''):
    code_list = []
    if starts_with:
        code_list = CodeTemplate.objects.filter(name__contains=starts_with)
        code_list = code_list.order_by('-download_count')
    else:
        code_list = CodeTemplate.objects.all().order_by('-download_count')

    # if max_results > 0:
    #     if len(code_list) > max_results:
    #         code_list = code_list[:max_results]

    return code_list


def get_package_list(max_results=0, starts_with=''):
    package_list = []
    if starts_with:
        package_list = Dependency.objects.filter(name__contains=starts_with)
        package_list = package_list.order_by('-download_count')
    else:
        package_list = Dependency.objects.all().order_by('-download_count')
    return package_list


def get_bundle_list(max_results=0, starts_with=''):
    bundle_list = []
    if starts_with:
        bundle_list = BundleTemplate.objects.filter(name__contains=starts_with)
        bundle_list = bundle_list.order_by('-download_count')
    else:
        bundle_list = BundleTemplate.objects.all().order_by('-download_count')
    return bundle_list


def suggest(request):
    context = RequestContext(request)
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
        print "GET: suggestion"
        print starts_with
    else:
        starts_with = request.POST['suggestion']

    code_list = get_code_list(8, starts_with)
    package_list = get_package_list(8, starts_with)
    bundle_list = get_bundle_list(8, starts_with)

    context_dict = {'codetemplate': code_list,
                    'packages': package_list,
                    'bundles': bundle_list}
    return render_to_response('emacshaqiba/code_list.html',
                              context_dict, context)


def display_package(request, id):
    context = RequestContext(request)

    if request.session.session_key == None:
        request.session['has_session'] = True
    else:
        session_key = request.session.session_key
        
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    packages = Dependency.objects.order_by('-download_count')
    bundles = BundleTemplate.objects.order_by('-download_count')

    if request.POST:
        init_file = make_init(session_key)
        write_package_config(packages.get(pk=id), init_file, session_key)
        tar_data = make_tarball(init_file, session_key)
        return HttpResponse(tar_data, mimetype="application/x-gzip")

    context_dict = {'codetemplate': codetemplate,
                    'packages': packages,
                    'bundles': bundles,
                    'package_id': packages.get(pk=id)}

    return render_to_response('emacshaqiba/display_package.html',
                              context_dict,
                              context)


def display_bundle(request, id):
    context = RequestContext(request)

    if request.session.session_key == None:
        request.session['has_session'] = True
    else:
        session_key = request.session.session_key
        
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    packages = Dependency.objects.order_by('-download_count')
    bundles = BundleTemplate.objects.order_by('-download_count')

    if request.POST:
        init_file = make_init(session_key)
        write_bundle_config(bundles.get(pk=id), init_file, session_key)
        tar_data = make_tarball(init_file, session_key)
        return HttpResponse(tar_data, mimetype="application/x-gzip")

    context_dict = {'codetemplate': codetemplate,
                    'packages': packages,
                    'bundles': bundles,
                    'bundle_id': bundles.get(pk=id)}

    return render_to_response('emacshaqiba/display_bundle.html',
                              context_dict,
                              context)


@login_required
def submit_bundle(request):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    packages = Dependency.objects.order_by('-download_count')
    bundles = BundleTemplate.objects.order_by('-download_count')

    if request.method == 'POST':
        bundletemplate_form = BundleTemplateForm(data=request.POST)

        if bundletemplate_form.is_valid():
            bundletemplate = bundletemplate_form.save(commit=False)
            if 'screenshot' in request.FILES:
                bundletemplate.screenshot = request.FILES['screenshot']

            bundletemplate.user = request.user
            bundletemplate.save()
            bundletemplate_form.save_m2m()
            messages.success(request, "Bundle submitted successfully !!")
            url = reverse('emacshaqiba.views.submit_bundle')
            return HttpResponseRedirect(url)
        else:
            print bundletemplate_form.errors
            messages.error(request, "Error: Submitting bundle!")
    else:
        bundletemplate_form = BundleTemplateForm()

    context_dict = {'codetemplate': codetemplate,
                    'bundletemplate_form': bundletemplate_form,
                    'packages': packages,
                    'bundles': bundles}

    return render_to_response('emacshaqiba/submit_bundle.html',
                              context_dict,
                              context)


@login_required
def submit_package(request):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    packages = Dependency.objects.order_by('-download_count')
    bundles = BundleTemplate.objects.order_by('-download_count')

    if request.method == 'POST':
        packagetemplate_form = PackageTemplateForm(data=request.POST)
        if packagetemplate_form.is_valid():
            packagetemplate = packagetemplate_form.save(commit=False)
            if 'tarFile' in request.FILES:
                packagetemplate.tarFile = request.FILES['tarFile']

            packagetemplate.user = request.user
            packagetemplate.save()
            messages.success(request, "Package submitted successfully !!")
            url = reverse('emacshaqiba.views.submit_package')
            return HttpResponseRedirect(url)
        else:
            packagetemplate_form.errors
            messages.error(request, "Error: Submitting package!")
    else:
        packagetemplate_form = PackageTemplateForm()

    context_dict = {'packagetemplate_form': packagetemplate_form,
                    'codetemplate': codetemplate,
                    'packages': packages,
                    'bundles': bundles}
    return render_to_response('emacshaqiba/submit_package.html',
                              context_dict,
                              context)


def register(request):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    packages = Dependency.objects.order_by('-download_count')
    bundles = BundleTemplate.objects.order_by('-download_count')
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
                messages.error(request, "Warning! One or more field \
                required!.")
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm
    # instances.  These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {'user_form': user_form,
                    'profile_form': profile_form,
                    'registered': registered,
                    'form_error': form_error,
                    'codetemplate': codetemplate,
                    'packages': packages,
                    'bundles': bundles}
    # Render the template depending on the context.
    return render_to_response('emacshaqiba/register.html',
                              context_dict,
                              context)


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    packages = Dependency.objects.order_by('-download_count')
    bundles = BundleTemplate.objects.order_by('-download_count')

    context_dict = {'codetemplate': codetemplate,
                    'packages': packages,
                    'bundles': bundles}

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.  If None
        # (Python's way of representing the absence of a value), no
        # user with matching credentials was found.
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
            return render_to_response('emacshaqiba/login.html',
                                      context_dict, context)

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('emacshaqiba/login.html',
                                  context_dict, context)


@login_required
def profile(request):
    context = RequestContext(request)
    codetemplate = CodeTemplate.objects.order_by('-download_count')
    packages = Dependency.objects.order_by('-download_count')
    bundles = BundleTemplate.objects.order_by('-download_count')

    context_dict = {'codetemplate': codetemplate,
                    'packages': packages,
                    'bundles': bundles,
                    'codetemplate_user':
                    codetemplate.filter(user=request.user),
                    'dependency_user': packages.filter(user=request.user),
                    'bundle_user': bundles.filter(user=request.user)}
    u = User.objects.get(username=request.user)

    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None

    context_dict['user'] = u
    context_dict['userprofile'] = up
    return render_to_response('emacshaqiba/profile.html',
                              context_dict, context)


@login_required
def user_logout(request):
    # Like before, obtain the request's context.
    context = RequestContext(request)

    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')
