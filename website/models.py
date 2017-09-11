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

    subject : CharField
        The name of the subject.
    """

    subject = models.CharField(max_length=50)

    def __unicode__(self):
        return self.subject


class Hardware(models.Model):
    """
    Defines the hardware model.

    **Attributes**

    name : CharField
        The name of the subject.
    imageUrl : CharField
        Image associated with the hardware.
    """
    name = models.CharField(max_length=150)
    imageUrl = models.CharField(max_length=300, default="https://upload.wikimedia.org/wikipedia/commons/3/33/White_square_with_question_mark.png")

    class Meta:
        verbose_name_plural = "Hardware"

    def __unicode__(self):
        return self.name


class Profile(models.Model):
    """
    Extension of the built in Django user class. This model is used to save the personal questionnaire for each profile.

    **Attributes**

    user : OneToOneField
        One-To-One relationship with default django user model.
    state : CharField
        The state in which the teacher works.
    yearLevels : MultiSelectField
        The year levels that the teacher teaches.
    subjectsTaught : ManyToManyField
        The subjects that the teacher teaches. Many-To-Many field with :class: 'Subject'
    classSize : IntegerField
        The class size the teacher normally teaches.
    technologyBackground : IntegerField
        The technology background of the teacher.
    programmingBackground : IntegerField
        The programming background of the teacher.
    hardware_devices : ManyToManyField
        A list of the hardware devices used by the teacher. Many-To-Many field with 'Hardware' model
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
            " code to large projects and/or coded for high level algorithmic computation)"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=30,
                             choices=STATE_CHOICES,
                             default='VIC')
    yearLevels = MultiSelectField(choices=YEAR_LEVEL_CHOICES,
                                  null=True)
    subjectsTaught = models.ManyToManyField(Subject, blank=True)
    classSize = models.IntegerField(choices=CLASS_SIZE_CHOICES, null=True)
    technologyBackground = models.IntegerField(choices=TECH_BACKGROUND_CHOICES, default=1)
    programmingBackground = models.IntegerField(choices=PROGRAMMING_BACKGROUND_CHOICES, default=1)
    hardware_devices = models.ManyToManyField(Hardware, blank=True)

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name


class Questionnaire(models.Model):
    """
        Creates a survey type which can hold questions

        **Attributes**

        name : Charfield
            Name of the survey

    """

    INPUT_CHOICES = (
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neutral"),
        (4, "Agree"),
        (5, "Strongly Agree"),
    )

    name = models.CharField(max_length=200, default='hardware')

    def __unicode__(self):
        return self.name

    def questions(self):
        if self.pk:
            return  Question.objects.filter(questionnaire=self.pk)
        else:
            return None


class Category(models.Model):
    """
        Categories that questions can be asked in. Provides the categories that are calculated for the device scales.

        **Attributes**

        name : Charfield
            Name of the category
        survey : ForeignKey
            Survey that the category belongs to

    """
    name = models.CharField(max_length=400)
    survey = models.ForeignKey(Questionnaire)

    def __unicode__(self):
        return self.name


class Question(models.Model):
    """
        Questions to be displayed in the survey.

        **Attributes**

        questionnaire : ForeignKey
            Survey that the questions are part of
        topic : ForeignKey
            Category the question falls under
        question_type : Charfield
            Choose if the question is radio button or text
        question : Charfield
            The question to be asked

    """

    INPUT_CHOICES = (
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neutral"),
        (4, "Agree"),
        (5, "Strongly Agree"),
    )

    TEXT = 'text'
    RADIO = 'radio'

    QUESTION_TYPES = (
        (TEXT, 'text'),
        (RADIO, 'radio'),
    )

    questionnaire = models.ForeignKey(Questionnaire)
    topic = models.ForeignKey(Category)
    question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=RADIO)
    question = models.CharField(max_length=100, default="TODO")

    def __unicode__(self):
        return self.questionnaire.name + " - " + self.topic.name + " - " + self.question


class Response(models.Model):
    """
        Store the results of the questionnaire.

        **Attributes**

        user : ForeignKey
            User completing the survey
        survey : ForeignKey
            The questionnaire being completed
        hardware : ForeignKey
            The hardware being evaluated

    """
    user = models.ForeignKey(Profile)
    survey = models.ForeignKey(Questionnaire)
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE, null=True)

    def __unicode__(self):
        return self.user.user.first_name + " - " + self.hardware.name


class Answer(models.Model):
    """
        Answers that are attributed to the survey response.
        This model is used indirectly. Access through either AnswerText or AnswerRadio.

        **Attributes**

        question : ForeignKey
            Question being answered
        response : ForeignKey
            The set of answers that this belongs to
        body : TextField
            Class extensions provide the body for the answer

    """
    question = models.ForeignKey(Question)
    response = models.ForeignKey(Response, null=True)


class AnswerText(Answer):
    body = models.TextField(blank=True, null=True)


class AnswerRadio(Answer):
    body = models.TextField(blank=True, null=True)


