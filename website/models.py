# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Subject(models.Model):
    subject = models.CharField(max_length=50)

    def __unicode__(self):
        return self.subject

class Hardware(models.Model):
    name = models.CharField(max_length=150)
    imageUrl = models.CharField(max_length=300, default="https://upload.wikimedia.org/wikipedia/commons/f/f8/Question_mark_alternate.svg")

    class Meta:
        verbose_name_plural = "Hardware"

    def __unicode__(self):
        return self.name

class Profile(models.Model):
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
    user = models.ForeignKey(Profile)
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE, null=True)
    question1 = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    question2 = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    question3 = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    question4 = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    question5 = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    question6 = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    question7 = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    question8 = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    question9 = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    question10 = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    question11 = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    question12 = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])


    def __unicode__(self):
        return self.hardware.name
