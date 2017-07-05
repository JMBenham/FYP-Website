# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from website.models import Hardware, Profile, Subject, DeviceQuestionnaire
from django.contrib import admin

admin.site.register(Hardware)
admin.site.register(Profile)
admin.site.register(Subject)
admin.site.register(DeviceQuestionnaire)
