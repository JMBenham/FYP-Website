# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Subject(models.Model):
    """
    Defines the subject model. Creates a new table in the database so new subjects can be always updated.

    **Attributes**

    subject
        The name of the subject.
    """

    subject = models.CharField(max_length=50)

    def __unicode__(self):
        return self.subject

class Hardware(models.Model):
    """
    Defines the hardware model.

    **Attributes**

    name
        The name of the subject.

    imageUrl
        Image associated with the hardware.
    """
    name = models.CharField(max_length=150)
    imageUrl = models.CharField(max_length=300, default="https://upload.wikimedia.org/wikipedia/commons/f/f8/Question_mark_alternate.svg")

    class Meta:
        verbose_name_plural = "Hardware"

    def __unicode__(self):
        return self.name

class Profile(models.Model):
    """
    Extension of the built in Django user class. This model is used to save the personal questionnaire for each profile.

    **Attributes**

    user
        One-To-One relationship with default django user model.
    state
        The state in which the teacher works.
    yearLevels
        The year levels that the teacher teaches.
    subjectsTaught
        The subjects that the teacher teaches. Many-To-Many field with :class: 'Subject'
    classSize
        The class size the teacher normally teaches.
    technologyBackground
        The technology background of the teacher.
    programmingBackground
        The programming background of the teacher.
    hardware_devices
        A list of the hardware devices used by the teacher. Many-To-Many field with .. py:class: 'Hardware'
    """
    STATE_CHOICES = (
        ('VIC', 'Victoria'),
        ('ACT', 'Australian Capital Territory'),
        ('NSW', 'New South Wales'),
        ('QLD', 'Queensland'),
        ('WA', 'Western Australia'),
        ('SA', 'South Australia'),
        ('NT', 'Northern Territory'),
        ('TAS', 'Tasmania'))
    YEAR_LEVEL_CHOICES = (
        (0, 'Prep'),
        (1, 'Grade 1'),
        (2, 'Grade 2'),
        (3, 'Grade 3'),
        (4, 'Grade 4'),
        (5, 'Grade 5'),
        (6, 'Grade 6'),
        (7, 'Year 7'),
        (8, 'Year 8'),
        (9, 'Year 9'),
        (10, 'Year 10'),
        (11, 'Year 11'),
        (12, 'Year 12'))
    CLASS_SIZE_CHOICES = (
        (1, '0-5'),
        (2, '6-10'),
        (3, '11-15'),
        (4, '16-20'),
        (5, '21-25'),
        (6, '25+'),
    )
    TECH_BACKGROUND_CHOICES = (
        (1, "I never use technology (e.g. Only touch a computer when required)"),
        (2, "Novice (e.g. Only use it to send emails and browse the internet)"),
        (3, "Intermediate (e.g. Can confidently use technology most of the time without assistance)"),
        (4, "Expert (e.g. Most of the time people come to you as the person to ask with their technology issues)"),
    )
    PROGRAMMING_BACKGROUND_CHOICES = (
        (1, "I have never programmed before (e.g. Only touch a computer when required)"),
        (2, "Some programming (e.g. I have written some programs to carry out simple tasks)"),
        (3, "Experienced programmer (e.g. I have used programs for computation, automation)"),
        (4, "Expert programmer (e.g. I have worked as a programmer before, contributed" +
            "code to large projects and/or coded for high level algorithmic computation)"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=3,
                             choices=STATE_CHOICES,
                             default='VIC')
    yearLevels = MultiSelectField(choices=YEAR_LEVEL_CHOICES,
                                  null=True)
    subjectsTaught = models.ManyToManyField(Subject, blank=True)
    classSize = models.IntegerField(choices=CLASS_SIZE_CHOICES, null=True)
    technologyBackground = models.IntegerField(choices=TECH_BACKGROUND_CHOICES, default="Expert")
    programmingBackground = models.IntegerField(choices=PROGRAMMING_BACKGROUND_CHOICES, default="Expert")
    hardware_devices = models.ManyToManyField(Hardware, blank=True)

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name

class DeviceQuestionnaire(models.Model):
    """
        Model to create and store the questionnaire on a per device basis.

        **Attributes**

        *user*
            ForeignKey relationship with logged in user.

        *hardware*
            ForeignKey relationship with the hardware being evaluated.

        *question1*
            Question 1

        """
    INPUT_CHOICES = (
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neutral"),
        (4, "Agree"),
        (5, "Strongly Agree"),
    )
    user = models.ForeignKey(Profile)
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE, null=True)
    question1 = models.PositiveIntegerField(default=1, choices=INPUT_CHOICES)
    question2 = models.PositiveIntegerField(default=1, choices=INPUT_CHOICES)
    question3 = models.PositiveIntegerField(default=1, choices=INPUT_CHOICES)
    question4 = models.PositiveIntegerField(default=1, choices=INPUT_CHOICES)
    question5 = models.PositiveIntegerField(default=1, choices=INPUT_CHOICES)
    question6 = models.PositiveIntegerField(default=1, choices=INPUT_CHOICES)
    question7 = models.PositiveIntegerField(default=1, choices=INPUT_CHOICES)
    question8 = models.PositiveIntegerField(default=1, choices=INPUT_CHOICES)
    question9 = models.PositiveIntegerField(default=1, choices=INPUT_CHOICES)
    question10 = models.PositiveIntegerField(default=1, choices=INPUT_CHOICES)
    question11 = models.PositiveIntegerField(default=1, choices=INPUT_CHOICES)
    question12 = models.PositiveIntegerField(default=1, choices=INPUT_CHOICES)


    def __unicode__(self):
        return self.hardware.name
