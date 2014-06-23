#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template import Library

register = Library()

def datetime_as_string(date_time):
    return "%s/%s às %s:%s" % (date_time.day, date_time.month, date_time.hour, date_time.minute)

@register.filter
def get_range(value, min_value=1):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
  """
  return range(min_value, value)