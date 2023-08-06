# -*- coding: utf-8 -*-

from datetime import datetime

from django.test import TestCase

from tests.models import ModelTest


class BirthdayTest(TestCase):
    def setUp(self):
        self.birthdays = ["2001-01-01", "2000-01-02", "2002-12-31"]
        for birthday in self.birthdays:
            ModelTest.objects.create(
                birthday=datetime.strptime(birthday, "%Y-%m-%d").date()
            )

    def test_default(self):
        # print("ModelTest._meta.fields", ModelTest._meta.fields)

        self.assertEqual(len(ModelTest._meta.fields), 3)
        self.assertTrue(hasattr(ModelTest, "birthday"))
        self.assertEqual(ModelTest.objects.all().count(), len(self.birthdays))

    @classmethod
    def teardown_class(self):
        """テストclass実行の後処理"""

        print("teardown_class")
