# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase


class TopViewTestCase(TestCase):
    def test_content_type(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertRegexpMatches(res['Content-Type'], '^text/plain')
