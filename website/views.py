# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import loader, RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.admin import User
from django.http import HttpResponse, HttpResponseRedirect
from .models import Hardware, Profile, DeviceQuestionnaire
from .forms import UserForm, UserProfileForm
from django.shortcuts import render, render_to_response


# Create your views here.

def index(request):
    list_of_devices = Hardware.objects.all()
    questionnaires = DeviceQuestionnaire.objects.all()
    list_of_questionnaires = {}
    for device in questionnaires:
        usability = (device.question1 + device.question2 + device.question3 + device.question4) / 4
        retention = (device.question5 + device.question6 + device.question7 + device.question8) / 4
        fun = (device.question9 + device.question10 + device.question11 + device.question12) / 4

        if device.hardware.name in list_of_questionnaires.keys():
            list_of_questionnaires[device.hardware.name]['usability'] = (usability + list_of_questionnaires[device.hardware.name]['usability']) / 2
            list_of_questionnaires[device.hardware.name]['retention'] = (retention + list_of_questionnaires[device.hardware.name]['retention']) /2
            list_of_questionnaires[device.hardware.name]['fun'] = (fun + list_of_questionnaires[device.hardware.name]['fun']) / 2

        else:
            list_of_questionnaires[device.hardware.name] = {"usability": usability,
                                                        "retention": retention,
                                                        "fun": fun}
    template= loader.get_template('website/index.html')
    context = {
        'list_of_devices': list_of_devices,
        'list_of_ratings': list_of_questionnaires
    }
    return HttpResponse(template.render(context, request))

# This is the main view, which will be the calendar in weekly view
def register(request):
    # Get the request's context
    context = RequestContext(request)

    # Boolean value to check whether the customRegistration was successful
    registered = False

    # Only process data if the request is a POST method
    if request.method == 'POST':
        # Attempt to take the information from the form
        #TODO create the forms for user customRegistration
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            # Update our variable to tell the template customRegistration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, the form is rendered using the form instance
    # This form is blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
        'website/registerCrispy.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
        context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

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
            return render_to_response('website/login.html', {'text': "invalid"}, context)

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('website/login.html', {}, context)

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

@login_required
def profile(request, id):
    context = RequestContext(request)
    context_dict = {}
    u = User.objects.get(pk = id)

    try:
        up = Profile.objects.get(user=u)
    except:
        up = None

    context_dict['user'] = request.user
    context_dict['remoteuser'] = u
    context_dict['userprofile'] = up

    return render_to_response('website/profile.html', context_dict, context)

def about(request):
    template= loader.get_template('website/about.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

@login_required
def completeSurvey(request):
    template= loader.get_template('website/submit_survey.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

