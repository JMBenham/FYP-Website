Code
====

Language
--------

The website is built on Django version 1.11.2 with Python 2.7. Django was chosen as it enables complex web applications
to be developed and deployed quickly. The scripting capablities and extensability of python mean that features such as
the filtering of database results based on the inputs are easily implemented.

Models
------

There are 4 models that have been included. These provide all of the different values that are available on
the site. The models are:

    #. DeviceQuestionnaire
        * The usability survey that teachers can fill out for each hardware device. It has a relationship with the hardware device that it is filled out for. All the usability surveys for a specific piece of hardware can be retrieved.
    #. Hardware
        * Defines a piece of physical computing hardware. It has attributes name and image.
    #. Profile
        * An extension of the default django user class. It holds the information relevant to the user such as which state they teach in and their previous programming experience.
    #. Subject
        * Defines the subjects which teachers can select from that they teach. Defined as a model so that teachers can add their own subjects if it does not appear on the list.

Extended descriptions for all of the models can be found in the API reference of this manual.

Views
-----

The views control the flow of information between models and templates.

Forms
-----

The forms provide a method of inputting the data into the database models.

Plugins
-------

A number of additional Django apps were included in the project to provide additional functionality to
the website. These provide necessary functions for file and form handling.

Django-crispy-forms.


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