# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.http import HttpResponse


def top(req):
    return HttpResponse(settings.REVISION, content_type='text/plain')
