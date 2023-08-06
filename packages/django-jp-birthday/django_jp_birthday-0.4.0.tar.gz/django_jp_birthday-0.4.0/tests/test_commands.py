# -*- coding: utf-8 -*-

from datetime import date, datetime
from io import StringIO

from django.core.exceptions import FieldError

from django.db import models
from django.test import TestCase
from django.core.management import call_command

from jp_birthday.fields import BirthdayField

from tests.models import ModelTest


class BirthdayTest(TestCase):
    def setUp(self):
        self.birthdays = ["2001-01-01", "2000-01-02", "2002-12-31"]
        for birthday in self.birthdays:
            ModelTest.objects.create(
                birthday=datetime.strptime(birthday, "%Y-%m-%d").date()
            )

    def test_default(self):

        out = StringIO()
        result = call_command(
            "jp_birthday",
            "jp_birthday.ModelTest",
            method="get_zodiac",
            verbosity=1,
            stdout=out,
        )
        print("result", type(result))
        # .call_command('mycommand', 'mydata', myopt=2)

        # print("out.getvalue()", out.getvalue())
        # self.assertEqual(len(ModelTest._meta.fields), 3)
        # self.assertTrue(hasattr(ModelTest, "birthday"))
        # self.assertEqual(ModelTest.objects.all().count(), len(self.birthdays))

    def test_success(self):
        pass

    @classmethod
    def teardown_class(self):
        """テストclass実行の後処理"""

        print("teardown_class")
