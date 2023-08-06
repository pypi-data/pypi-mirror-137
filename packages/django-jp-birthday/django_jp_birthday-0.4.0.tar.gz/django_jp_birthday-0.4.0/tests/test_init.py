# -*- coding: utf-8 -*-

from datetime import date, datetime

from django.core.exceptions import FieldError

from django.db import models
from django.test import TestCase

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

        self.assertEqual(len(ModelTest._meta.fields), 3)
        self.assertTrue(hasattr(ModelTest, "birthday"))
        # self.assertTrue(hasattr(ModelTest, "birthday_field"))
        self.assertEqual(ModelTest.objects.all().count(), len(self.birthdays))

    def test_ordering(self):
        pks1 = [obj.pk for obj in ModelTest.objects.order_by("birthday")]
        pks2 = [obj.pk for obj in ModelTest.objects.order_by_birthday(True)]

        # print("pks1", pks1)
        # print("pks2", pks2)

        self.assertNotEqual(pks1, pks2)

        doys = [
            getattr(obj, "birthday_dayofyear_internal")
            for obj in ModelTest.objects.order_by_birthday()
        ]
        self.assertEqual(doys, [1, 2, 365])

        doys = [
            getattr(obj, "birthday_dayofyear_internal")
            for obj in ModelTest.objects.order_by_birthday(True)
        ]
        self.assertEqual(doys, [365, 2, 1])

        years = [obj.birthday.year for obj in ModelTest.objects.order_by("birthday")]
        self.assertEqual(years, [2000, 2001, 2002])

    def test_manager(self):
        # settings.DEBUG = True

        jan1 = date(year=2010, month=1, day=1)

        self.assertEqual(ModelTest.objects.get_birthdays(jan1).count(), 1)
        self.assertEqual(ModelTest.objects.get_upcoming_birthdays(30, jan1).count(), 2)
        self.assertEqual(
            ModelTest.objects.get_upcoming_birthdays(30, jan1, False).count(), 1
        )

        dec31 = date(year=2010, month=12, day=31)
        self.assertEqual(ModelTest.objects.get_birthdays(dec31).count(), 1)
        self.assertEqual(ModelTest.objects.get_upcoming_birthdays(30, dec31).count(), 3)

        doys = [
            getattr(obj, "birthday_dayofyear_internal")
            for obj in ModelTest.objects.get_upcoming_birthdays(30, dec31)
        ]
        self.assertEqual(doys, [365, 1, 2])

        doys = [
            getattr(obj, "birthday_dayofyear_internal")
            for obj in ModelTest.objects.get_upcoming_birthdays(30, dec31, reverse=True)
        ]
        self.assertEqual(doys, [2, 1, 365])

        doys = [
            getattr(obj, "birthday_dayofyear_internal")
            for obj in ModelTest.objects.get_upcoming_birthdays(30, dec31, order=False)
        ]
        self.assertEqual(doys, [1, 2, 365])

        self.assertEqual(
            ModelTest.objects.get_upcoming_birthdays(30, dec31, False).count(), 2
        )
        self.assertTrue(ModelTest.objects.get_birthdays().count() in [0, 1])
        # print("~~~" * 20)

    def test_exception(self):
        class BrokenModel(models.Model):
            birthday = BirthdayField()

        self.assertRaises(
            FieldError,
            BirthdayField().contribute_to_class,
            BrokenModel,
            "another_birthday",
        )

    @classmethod
    def teardown_class(self):
        """テストclass実行の後処理"""

        print("teardown_class")
