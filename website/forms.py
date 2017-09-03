from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder, Fieldset, Field, Button, HTML
from crispy_forms.bootstrap import Tab, TabHolder, InlineCheckboxes, InlineRadios
from website.models import Profile, Hardware, Subject, DeviceQuestionnaire
from django.contrib.auth.admin import User
from django.contrib.auth.forms import PasswordResetForm


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
    """
    Questionnaire form

    Inputs:

        - hardware : Dropdown

        10 tabs for the different categories
        Each has 3 questions on a 5 point scale

        - Submit : Button
    """
    def __init__(self, *args, **kwargs):
        super(QuestionnaireForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-questionnaire_form"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-7'
        self.helper.form_method = 'post'
        self.helper.form_action = 'completesurvey'

        self.helper.layout = Layout(
            Fieldset(
                'What are your experiences with tech hardware?',
                'hardware',
            ),
            HTML('<button type="button" class="btn btn-primary pull-right" data-toggle="modal" data-target="#newHardwareModal" data-whatever="@mdo">Add new hardware</button>'),
            HTML('</br>'),
            HTML('</br>'),
            TabHolder(
                Tab(
                    'Non-threatening',
                    InlineRadios('question1'),
                    InlineRadios('question2'),
                    InlineRadios('question3'),
                ),
                Tab(
                    'Engagement',
                    InlineRadios('question4'),
                    InlineRadios('question5'),
                    InlineRadios('question6'),
                ),
                Tab(
                    'Visibility',
                    InlineRadios('question7'),
                    InlineRadios('question8'),
                    InlineRadios('question9'),

                ),
                Tab(
                    'Clarity',
                    InlineRadios('question10'),
                    InlineRadios('question11'),
                    InlineRadios('question12'),
                ),
                Tab(
                    'Error avoidance',
                    InlineRadios('question13'),
                    InlineRadios('question14'),
                    InlineRadios('question15'),
                ),
                Tab(
                    'Feedback',
                    InlineRadios('question16'),
                    InlineRadios('question17'),
                    InlineRadios('question18'),

                ),
                Tab(
                    'Cost',
                    InlineRadios('question19'),
                    InlineRadios('question20'),
                    InlineRadios('question21'),
                ),
                Tab(
                    'Time',
                    InlineRadios('question22'),
                    InlineRadios('question23'),
                    InlineRadios('question24'),
                ),
                Tab(
                    'Technical',
                    InlineRadios('question25'),
                    InlineRadios('question26'),
                    InlineRadios('question27'),
                ),
                Tab(
                    'Curriculum',
                    InlineRadios('question28'),
                    InlineRadios('question29'),
                    InlineRadios('question30'),
                )

            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white pull-right')
            )
        )

    hardware = forms.ModelChoiceField(
        label="Which hardware do you use?",
        queryset = Hardware.objects.all(),
    )
    question1 = forms.ChoiceField(
        label = "The interface is inviting to new users",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question2 = forms.ChoiceField(
        label = "I am never afraid that I may lose all my work due to small mistakes",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question3 = forms.ChoiceField(
        label = "Students feel positive the first time they use this system",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question4 = forms.ChoiceField(
        label = "Students are highly motivated to use this hardware",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question5 = forms.ChoiceField(
        label = "Students are excited to spend time using the hardware",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question6 = forms.ChoiceField(
        label = "Students do not get distracted from the programming concepts",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question7 = forms.ChoiceField(
        label = "The system always does what I am expecting",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question8 = forms.ChoiceField(
        label = "I always know what the system is doing",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question9 = forms.ChoiceField(
        label = "TODO",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question10 = forms.ChoiceField(
        label = "The interface is clear and easy to understand",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question11 = forms.ChoiceField(
        label = "I never have to look up how to do something on the interface",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question12 = forms.ChoiceField(
        label = "I spend only a small amount of time explaining the interface to new students",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question13 = forms.ChoiceField(
        label = "How easy was it actually to use?",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question14 = forms.ChoiceField(
        label = "How easy was it actually to use?",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question15 = forms.ChoiceField(
        label = "How easy was it actually to use?",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question16 = forms.ChoiceField(
        label = "How easy was it actually to use?",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question17 = forms.ChoiceField(
        label = "How easy was it actually to use?",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question18 = forms.ChoiceField(
        label = "How easy was it actually to use?",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question19 = forms.ChoiceField(
        label = "How easy was it actually to use?",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question20 = forms.ChoiceField(
        label = "How easy was it actually to use?",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question21 = forms.ChoiceField(
        label = "How easy was it actually to use?",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question22 = forms.ChoiceField(
        label = "How easy was it actually to use?",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question23 = forms.ChoiceField(
        label = "How easy was it actually to use?",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question24 = forms.ChoiceField(
        label = "How easy was it actually to use?",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question25 = forms.ChoiceField(
        label = "How easy was it actually to use?",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question26 = forms.ChoiceField(
        label = "How easy was it actually to use?",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question27 = forms.ChoiceField(
        label = "How easy was it actually to use?",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question28 = forms.ChoiceField(
        label = "How easy was it actually to use?",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question29 = forms.ChoiceField(
        label = "How easy was it actually to use?",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    question30 = forms.ChoiceField(
        label = "How easy was it actually to use?",
        choices=DeviceQuestionnaire.INPUT_CHOICES
    )
    class Meta:
        model = DeviceQuestionnaire
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