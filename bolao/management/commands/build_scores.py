#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bolao.score import build_scores
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Correlate players'

    def handle(self, *args, **options):
        build_scores()