Code
====

Language
--------

The website is built on Django version 1.11.2 with Python 2.7. Django was chosen as it enables complex web applications
to be developed and deployed quickly. The scripting capablities and extensability of python mean that features such as
the filtering of database results based on the inputs are easily implemented.

Models
------

There are 10 models that have been included. These provide all of the different values that are available on
the site. The models are:

    #. Answer
        * Base answer class for the different answer types. Has a relation to the question and a response.
    #. AnswerRadio
        * Stores the results if the question was answered by radio buttons.
    #. AnswerText
        * Stores the result if the question was an open ended text answer.
    #. Category
        * The categories of questions which can be asked.
    #. Hardware
        * Defines a piece of physical computing hardware. It has attributes name and image.
    #. Profile
        * An extension of the default django user class. It holds the information relevant to the user such as which state they teach in and their previous programming experience.
    #. Response
        * Stores the results of completed questionnaires. Has a relation to the user, the survey and the hardware.
    #. Subject
        * Defines the subjects which teachers can select from that they teach. Defined as a model so that teachers can add their own subjects if it does not appear on the list.
    #. Question
        * A specific question to be included on the survey. Has a related questionnaire, category, question type and question text.
    #. Questionnaire
        * Defines a set of questions that can be asked. This allows the questionnaire to be changed quickly. For the
        purposes of this website it is currently hardcoded to a set value.



Extended descriptions for all of the models can be found in the API reference of this manual.

Views
-----

The views control the flow of information between models and templates. There is a unique view for each page on the
website. The list of pages and their urls are:

  - index : "/"
  - register : "/register/"
  - user_login : "/login/"
  - user_logout : "/logout/"
  - profile : "/profile/<Numeric ID>/"
  - device_profile : "/hardware/<Numeric ID>/"
  - about : "/about/"
  - complete_survey : "/completesurvey/"
  - delete_survey : "/deletesurvey/<Numeric ID>/"
  
A number of views are implemented directly from the Django templates. These are used for extra password handling functions.

  - password_reset : "/password/reset/"
  - password_reset_confirm : "/password/reset/confirm"
  - password_reset_done : "/password/reset/done"
  - password_reset_complete : "/password/reset/complete"
  - password_change : "/password/change/"
  - password_change_done : "/password/change/done"

Forms
-----

The forms provide a method of inputting the data into the database models. The forms included in this website are:

  #. UserForm
  #. UserProfileForm
  #. QuestionnaireForm
  #. SubjectForm
  #. HardwareForm
  
Each of these forms links directly to a class which provides the destination for form inputs to be saved.

The UserForm and UserProfileForm provide the registration forms. The UserForm class saves to the Django default user
class. The UserProfileForm is the extension of this class to provide extra inputs that are required by this website.
The UserProfileForm implements the initial survey.

The QuestionnaireForm is the form display of the questionnaire usability model. It is displayed using tabbed elements
for each of the usability criteria to preserve neatness and readability of the page.

The SubjectForm and HardwareForm classes provide simple form layouts for their respective models. These are
kept as simple as possible as these forms are designed to be displayed as modals. These forms are used to add new
subjects or types of hardware when a teacher is filling in the initial survey or a usability questionnaire.

Plugins
-------

A number of additional Django apps were included in the project to provide additional functionality to
the website. These provide necessary functions for file and form handling.

Django-crispy-forms is used for the formatting of forms for display on the frontend. Crispy forms provides functions
for easily marking up the form code to generate HTML. This means that the form markup doesn't have to be written
manually in the HTML templates. All changes to the layout of the forms should therefore be made directlyin the forms
file.

multiselectfield


CSS and JavaScript
------------------

Bootstrap
~~~~~~~~~

Bootstrap was used to quickly develop the necessary front end for the website.

Bootstrap version == 3.2.1

Elements used from bootstrap for the front-end design include.

GSDK
~~~~

The front end of the website is built on CSS files and JavaScript in the GSDK toolkit from Creative Tim.
These files extend the CSS files provided in the default bootstrap installation. The addition of these files give
the site a more modern and finished feel.
