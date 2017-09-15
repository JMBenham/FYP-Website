# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import loader, RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.core.urlresolvers import reverse
from django.contrib.auth.admin import User
from django.views.generic import UpdateView
#from django.views.generic.edit import UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from .models import Hardware, Profile, Questionnaire, Subject, Response, AnswerRadio, AnswerText, Category
from .forms import UserForm, UserProfileForm, QuestionnaireForm, SubjectForm, HardwareForm, DeviceFilterForm
from django.shortcuts import render, render_to_response, redirect
import itertools



# Create your views here.


class UserUpdateView(UpdateView):
    """
    Update user view
    - Allow users to update their information after they have registered

    Outputs:
        - Profile object
    """

    form_class = UserProfileForm
    model = Profile
    template_name = 'website/register_crispy_update_form.html'
    pk_url_kwarg = 'id'

    def get(self, request, **kwargs):
        self.object = Profile.objects.get(user=self.request.user)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(reverse('profile', kwargs={'id': self.request.user.id}))


def index(request):
    """
    Home page view

    Outputs:
        - list_of_ratings
            - Is a two level dictionary containing all of the hardware that have completed surveys.
            - Each hardware object is the key to a dictionary containing the survey responses
    """
    list_of_devices = []
    list_of_questionnaires = {}

    if request.method == 'POST':
        filter_form = DeviceFilterForm(data=request.POST)

        filter_data_dict = dict(filter_form.data.iterlists())

        stateFilter = filter_data_dict['state'][0]
        try:
            yearLevelsFilter = filter_data_dict['yearLevels']
            #print yearLevelsFilter
        except:
            yearLevelsFilter = ""

        try:
            subjectsTaughtFilter = filter_data_dict['subjectsTaught']
        except:
            subjectsTaughtFilter = ""

        classSizeFilter = filter_data_dict['classSize'][0]
        techBackgroundFilter = filter_data_dict['technologyBackground'][0]
        programBackgroundFilter = filter_data_dict['programmingBackground'][0]

        if stateFilter != 'ALL':
            users = Profile.objects.filter(state=stateFilter).distinct()
        else:
            users = Profile.objects.all()

        #TODO: Fix filtering on year levels
        """
        if yearLevelsFilter != "":
            print yearLevelsFilter
            users = users.filter(yearLevels__contains=yearLevelsFilter).distinct()
            print users
            """
        if subjectsTaughtFilter != "":
            users = users.filter(subjectsTaught__in=Subject.objects.filter(id__in=subjectsTaughtFilter)).distinct()
        if classSizeFilter != '0':
            users = users.filter(classSize=classSizeFilter).distinct()
        if techBackgroundFilter != '0':
            users = users.filter(technologyBackground=techBackgroundFilter).distinct()
        if programBackgroundFilter != '0':
            users = users.filter(programmingBackground=programBackgroundFilter).distinct()

        answers = []
        for user in users:
            responses = Response.objects.filter(user=user)
            for response in responses:
                query_answers = AnswerRadio.objects.filter(response=response)
                for answer in query_answers:
                    answers.append(answer)

    else:
        filter_form = DeviceFilterForm()
        answers = AnswerRadio.objects.all()

    questionnaire = Questionnaire.objects.get(name='Hardware')
    categories = Category.objects.filter(survey=questionnaire)
    for answer in answers:
        if answer.response.hardware not in list_of_devices:
            list_of_devices.append(Hardware.objects.get(name=answer.response.hardware.name))
        for category in categories:
            if answer.question.topic == category:
                if answer.response.hardware not in list_of_questionnaires.keys():
                    list_of_questionnaires[answer.response.hardware] = {}
                    list_of_questionnaires[answer.response.hardware][category.name] = int(answer.body)
                    #Add the value of the question to the running counter
                else:
                    if category.name not in list_of_questionnaires[answer.response.hardware].keys():
                        list_of_questionnaires[answer.response.hardware][category.name] = int(answer.body)
                    else:
                        list_of_questionnaires[answer.response.hardware][category.name] += int(answer.body)
                        list_of_questionnaires[answer.response.hardware][category.name] /= 2

    template= loader.get_template('website/index.html')
    context = {
        'list_of_ratings': list_of_questionnaires,
        'filter': filter_form,
    }
    return HttpResponse(template.render(context, request))


def register(request):
    """
    Registration view

    Outputs:
        - subjects
        - hardware
        - user_form
        - profile_form
        - subject_form
        - hardware_form
    """

    # Get the request's context
    context = RequestContext(request)

    # Boolean value to check whether the customRegistration was successful
    registered = False

    # Only process data if the request is a POST method
    if request.method == 'POST':
        # Attempt to take the information from the form
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        subject_form = SubjectForm(data=request.POST)
        hardware_form = HardwareForm(data=request.POST)

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
            userprofile = profile_form.save(commit=False)
            userprofile.user = user

            userprofile.save()
            profile_form.save_m2m()

            # Update our variable to tell the template customRegistration was successful.
            registered = True

        elif subject_form.is_valid():
            subject_form.save()
            return redirect('register')

        elif hardware_form.is_valid():
            hardware = hardware_form.save(commit=False)
            hardware.imageUrl = "https://upload.wikimedia.org/wikipedia/commons/3/33/White_square_with_question_mark.png"

            hardware.save()
            return redirect('register')
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
        hardware_form = HardwareForm()
        subject_form = SubjectForm()

        hardware_form.helper.form_action = 'register'
        subject_form.helper.form_action = 'register'

    # Render the template depending on the context.
    template= loader.get_template('website/register_crispy.html')
    context = {
        'subjects': Subject.objects.all(),
        'hardware': Hardware.objects.all(),
        'user_form': user_form,
        'profile_form': profile_form,
        'subject_form': subject_form,
        'hardware_form': hardware_form,
    }
    return HttpResponse(template.render(context, request))


def user_login(request):
    """Display the profile of the currently logged in user.

        .. Get:
            Return the login form

        ..Post:
            Use Django's built in authentication system to log in the user.

        **Template:**\n
         - website/login.html
        """
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
def user_logout(request):
    """Call Django's built in logout method.

        **Template:**\n
         - website/logout.html
        """


    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')


@login_required
def profile(request, id):
    """Display the profile of the currently logged in user.

    **Context**\n
     - user: Currently logged in user
     - remoteuser: Instance  of User object obtained with 'id'
     - userprofile: Instance of Profile object linked to 'remoteuser'
     - questionnaires: List of all of the surveys completed by the user
     - subjectsTaught: List all of the subjects taught by user
     - hardwareUsed: List all hardware devices used by user
     - class: Class size from user profile
     - techBackground: Technology background from user profile
     - programmingBackground: Programming background from user profile

    **Template:**\n
     - website/profile.html
    """

    context = RequestContext(request)
    context_dict = {}
    u = User.objects.get(pk=id)

    answers = []
    yearlevels = []

    try:
        up = Profile.objects.get(user=u)
    except:
        up = None

    submitted_questionnaires = Response.objects.filter(user=up)
    for survey in submitted_questionnaires:
        answers += AnswerText.objects.filter(response=survey)
        answers += AnswerRadio.objects.filter(response=survey)

    for year in up.yearLevels:
        yearlevels.append(dict(up.YEAR_LEVEL_CHOICES)[int(year)])

    categories = Category.objects.all()
    subjects = up.subjectsTaught.all()
    hardware = up.hardware_devices.all()

    size_class = dict(up.CLASS_SIZE_CHOICES)[up.classSize]
    tech_background = dict(up.TECH_BACKGROUND_CHOICES)[up.technologyBackground]
    programming_background = dict(up.PROGRAMMING_BACKGROUND_CHOICES)[up.programmingBackground]
    template = loader.get_template('website/profile.html')
    context = {
        'user': request.user,
        'remoteuser': u,
        'userprofile': up,
        'questionnaires': submitted_questionnaires,
        'yearlevels': yearlevels,
        'categories': categories,
        'answers': answers,
        'subjectsTaught': subjects,
        'hardwareUsed': hardware,
        'class': size_class,
        'techBackground': tech_background,
        'programmingBackground': programming_background,
    }
    return HttpResponse(template.render(context, request))


def device_profile(request, id):
    """Display the hardware device profile and the related extended questionnaires.

    **Context**\n
     - device: An instance of :class:'Hardware'
     - surveys: All related instances of :class:'DeviceQuestionnaire'

    **Template:**\n
     - website/device_profile.html
    """

    hardware = Hardware.objects.get(pk = id)
    questionnaires = Response.objects.filter(hardware=hardware)
    categories = Category.objects.all()
    answers = []
    answersRadio = []
    answersAverage = {}
    for survey in questionnaires:
        answers += AnswerText.objects.filter(response=survey)
        answersRadio += AnswerRadio.objects.filter(response=survey)

    for answer in answersRadio:
        if answer.question.topic not in answersAverage.keys():
            answersAverage[answer.question.topic] = int(answer.body)
        else:
            answersAverage[answer.question.topic] += int(answer.body)
            answersAverage[answer.question.topic] /= 2


    template = loader.get_template('website/device_profile.html')
    context = {
        'device': hardware,
        'surveys': questionnaires,
        'categories': categories,
        'answers': answers,
        'answersRadio': answersRadio,
        'answersCategories': answersAverage,
    }
    return HttpResponse(template.render(context, request))


def about(request):
    """Display a generic about page to give users some information about the website.
    TODO: Include links to the paper and describe the usability framework.

    **Template:**\n
     - website/profile.html
    """
    template = loader.get_template('website/about.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


@login_required
def complete_survey(request):
    """User can complete a survey for a specified device.

    .. Get:
        Return an empty form to the browser.

    .. Post:
        Process and save the completed survey.

    **Context**\n
     - survey_form: An instance of a 'QuestionnaireForm' object
     - hardware_form: An instance of a 'HardwareForm' object

    **Template:**\n
     - website/submit_survey.html
    """


    # Only process data if the request is a POST method
    if request.method == 'POST':
        # Attempt to take the information from the form
        survey_form = QuestionnaireForm(data=request.POST)
        hardware_form = HardwareForm(data=request.POST)

        if survey_form.is_valid():
            user = Profile.objects.get(user=request.user)
            #Include a test to check if the user has already submitted a survey for the piece of hardware.
            survey = survey_form.save(user)
            survey.save()

            return redirect('index')
        elif hardware_form.is_valid():
            hardware = hardware_form.save(commit =False)
            hardware.imageUrl = "https://upload.wikimedia.org/wikipedia/commons/3/33/White_square_with_question_mark.png"

            hardware.save()
            return redirect('completesurvey')
        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print survey_form.errors

    # Not a HTTP POST, the form is rendered using the form instance
    # This form is blank, ready for user input.
    else:
        survey_form = QuestionnaireForm()
        hardware_form = HardwareForm()

    template = loader.get_template('website/submit_survey.html')
    context = {
        'survey_form': survey_form,
        'hardware_form': hardware_form,
    }
    return HttpResponse(template.render(context, request))


@login_required
def delete_survey(request, id):
    """Delete the survey referenced by 'id'

    Check to ensure that the device questionnaire is owned by the current user with
    'device.user.id' is the same as 'user.id'

    **Redirect:**\n
     - website/profile.html
    """
    devicesurvey = Response.objects.get(pk=id)
    user = request.user

    if devicesurvey.user.id == user.id:
        devicesurvey.delete()

    return redirect('profile', id=user.id)




