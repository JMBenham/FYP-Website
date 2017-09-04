from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder, Fieldset, Field, Button, HTML
from crispy_forms.bootstrap import Tab, TabHolder, InlineCheckboxes, InlineRadios
from website.models import Profile, Hardware, Subject, Questionnaire, Category, Question, Response, Answer, AnswerText, AnswerRadio
from django.contrib.auth.admin import User
from django.contrib.auth.forms import PasswordResetForm
from django.utils.safestring import mark_safe


class UserForm(forms.ModelForm):
    """
        User form

        Inputs:

            - first_name : Text
            - last_name : Text
            - username : Text
            - email : Text
            - password : Text
    """

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-user_form"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-6'
        self.helper.form_method = 'post'
        self.helper.form_action = 'register'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Fieldset(
                'Your details',
                'first_name',
                'last_name',
                'username',
                'email',
                'password',
            )
        )
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter surname'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    """
        Profile form

        Inputs:

            - state : Dropdown
            - yearLevels : Checkbox
            - subjectsTaught : Checkbox
            - classSize : Dropdown
            - technologyBackground : Dropdown
            - programmingBackground : Dropdown
            - hardware_devices : Checkbox

    """
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-profile_form"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-6'
        self.helper.form_method = 'post'
        self.helper.form_action = 'register'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Fieldset(
                'Some information about your technology usage: ',
                'state',
                'yearLevels',

                'subjectsTaught',
                'classSize',
                'technologyBackground',
                'programmingBackground',
                'hardware_devices',
            ),
        )

    state = forms.ChoiceField(label="Which state do you primarily teach in?", choices=Profile.STATE_CHOICES)
    yearLevels = forms.ChoiceField(label="What year levels do you teach?", choices=Profile.YEAR_LEVEL_CHOICES, widget=forms.CheckboxSelectMultiple)
    subjectsTaught = forms.ModelMultipleChoiceField(label="Which subjects do you teach?", queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple)
    classSize = forms.ChoiceField(label="What is you average class size?", choices=Profile.CLASS_SIZE_CHOICES)
    technologyBackground = forms.ChoiceField(label="What is your technology background?", choices=Profile.TECH_BACKGROUND_CHOICES)
    programmingBackground = forms.ChoiceField(label="What is your programming background?", choices=Profile.PROGRAMMING_BACKGROUND_CHOICES)
    hardware_devices = forms.ModelMultipleChoiceField(label="Which devices do you use?", queryset=Hardware.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Profile
        fields = ('state', 'yearLevels', 'subjectsTaught', 'classSize', 'technologyBackground', 'programmingBackground', 'hardware_devices')


class QuestionnaireForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        question_list = []
        super(QuestionnaireForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-questionnaire_form"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-7'
        self.helper.form_method = 'post'
        self.helper.form_action = 'completesurvey'
        self.questionnaire = Questionnaire.objects.get(name='Hardware')
        self.fields['survey'].required = False

        self.helper.layout = Layout(
            Fieldset(
                'What are your experiences with tech hardware?',
                'hardware',
            ),
            HTML('<button type="button" class="btn btn-primary pull-right" data-toggle="modal" data-target="#newHardwareModal" data-whatever="@mdo">Add new hardware</button>'),
            HTML('</br>'),
            HTML('</br>'),
            Fieldset(
                'Complete these questions about the hardware.',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white pull-right')
            )
        )
        for q in self.questionnaire.questions():
            question_list.append(q.pk)
            if q.question_type == Question.TEXT:
                self.fields["question_%d" %q.pk] = forms.CharField(label=q.question, widget=forms.Textarea)
                self.helper.layout[4].append('question_%d' % q.pk)
            elif q.question_type == Question.RADIO:
                self.fields["question_%d" % q.pk] = forms.ChoiceField(label=q.question,
                                                                      choices=q.INPUT_CHOICES)
                self.helper.layout[4].append(InlineRadios('question_%d' %q.pk))

            if q.topic:
                classes = self.fields["question_%d" % q.pk].widget.attrs.get("class")
                if classes:
                    self.fields["question_%d" % q.pk].widget.attrs["class"] = classes + (" cat_%s" % q.topic.name)
                else:
                    self.fields["question_%d" % q.pk].widget.attrs["class"] = (" cat_%s" % q.topic.name)
                self.fields["question_%d" % q.pk].widget.attrs["category"] = q.topic.name
    hardware = forms.ModelChoiceField(
        label="Which hardware do you use?",
        queryset=Hardware.objects.all(),
    )

    def save(self, user_id, *args, **kwargs):
        response = super(QuestionnaireForm, self).save(commit=False)
        response.survey = self.questionnaire
        response.user = user_id
        response.save()

        for field_name, field_value in self.cleaned_data.iteritems():
            if field_name.startswith("question_"):
                q_id = int(field_name.split("_")[1])
                q = Question.objects.get(pk=q_id)

                if q.question_type == Question.TEXT:
                    a = AnswerText(question=q)
                    a.body = field_value
                elif q.question_type == Question.RADIO:
                    a = AnswerRadio(question=q)
                    a.body = field_value

                a.response = response
                a.save()
        return response

    class Meta:
        model = Response
        exclude = ('user',)


class SubjectForm(forms.ModelForm):
    """
    Subject form

    Inputs:

        - subject : Text
        - Submit : Button
    """
    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-subject_form"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-7'
        self.helper.form_method = 'post'
        self.helper.form_action = 'completesurvey'

        self.helper.layout = Layout(
            Fieldset('',
                     'subject'),

            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )

    class Meta:
        model = Subject
        fields = ('subject',)


class HardwareForm(forms.ModelForm):
    """
    Hardware form

    Inputs:

        - Name : Text
        - Submit : Button
    """
    def __init__(self, *args, **kwargs):
        super(HardwareForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-hardware_form"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-7'
        self.helper.form_method = 'post'
        self.helper.form_action = 'completesurvey'

        self.helper.layout = Layout(
            Fieldset('',
                     'name'),

            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )

    class Meta:
        model = Hardware
        fields = ('name',)