# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from website.models import Hardware, Profile, Subject, Questionnaire, Question, Answer, Response, AnswerText, AnswerRadio, Category
from django.contrib import admin


class QuestionInLine(admin.TabularInline):
    model = Question
    ordering = ('topic', )
    extra = 0


class CategoryInLine(admin.TabularInline):
    model = Category
    extra = 0


class SurveyAdmin(admin.ModelAdmin):
    inlines = [CategoryInLine, QuestionInLine]


class AnswerBaseInline(admin.StackedInline):
    fields = ('question', 'body')
    #readonly_fields = ('question', )
    extra = 0


class AnswerTextInline(AnswerBaseInline):
    model = AnswerText


class AnswerRadioInline(AnswerBaseInline):
    model = AnswerRadio


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'hardware')
    inlines = [AnswerTextInline, AnswerRadioInline]


admin.site.register(Hardware)
admin.site.register(Profile)
admin.site.register(Subject)
admin.site.register(Questionnaire, SurveyAdmin)
admin.site.register(Response, ResponseAdmin)
