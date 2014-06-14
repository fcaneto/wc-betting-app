#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template

register = template.Library()

def datetime_as_string(date_time):
    return "%s/%s às %s:%s" % (date_time.day, date_time.month, date_time.hour, date_time.minute)