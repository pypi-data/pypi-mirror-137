from datetime import date, datetime

# from django.db import connection

# from django.db import backends

from django.test import TestCase
from django.conf import settings

from tests.models import ModelTest


class BirthdayTestManagers(TestCase):
    @classmethod
    def setup_class(self):
        """テストclass実行の前処理"""

        print("setup_class")

    def setUp(self):
        print("setUp")

        self.meiji = ["1905-1-2", "1905-1-1", "1905-2-1", "1905-2-2", "1905-1-30"]
        self.showa = ["1980-7-7", "1975-1-1", "1970-2-15"]
        self.heisei = [
            "2000-01-02",
            "2001-01-01",
            "2002-12-31",
            "2021-2-20",
            "1999-12-25",
        ]

        self.birthdays = self.meiji + self.showa + self.heisei
        for birthday in self.birthdays:
            model_test = ModelTest(
                birthday=datetime.strptime(birthday, "%Y-%m-%d").date()
            )
            model_test.save()

    def test_get_upcoming_birthdays(self):

        print("---" * 20)
        print("test_get_upcoming_birthdays")

        # settings.DEBUG = True

        jan1 = date(year=2010, month=1, day=1)

        # 1月の要素だけ抽出
        count = [int(birthday.split("-")[1]) for birthday in self.birthdays].count(1)

        get_upcoming_birthdays = ModelTest.objects.get_upcoming_birthdays(30, jan1)
        self.assertEqual(get_upcoming_birthdays.count(), count)

        count = 0
        for birthday in self.birthdays:
            month = int(birthday.split("-")[1])
            day = int(birthday.split("-")[2])

            if month == 1 and day != 1:
                count += 1

        get_upcoming_birthdays = ModelTest.objects.get_upcoming_birthdays(
            30, jan1, False
        )
        self.assertEqual(get_upcoming_birthdays.count(), count)

        print("----" * 15)

        settings.DEBUG = False

    def test_order_by_birthday(self):

        print("---" * 20)
        print("test_order_by_birthday")

        pks1 = [obj.pk for obj in ModelTest.objects.order_by("birthday")]
        pks2 = [obj.pk for obj in ModelTest.objects.order_by_birthday(True)]

        # print("pks1", pks1)
        # print("pks2", pks2)
        self.assertNotEqual(pks1, pks2)

        birthdays = ModelTest.objects.order_by_birthday()
        order_by_birthday = [obj.birthday for obj in birthdays]
        print("order_by_birthday", len(order_by_birthday))

        doys = [
            getattr(obj, "birthday_dayofyear_internal")
            for obj in ModelTest.objects.order_by_birthday()
        ]

        obj_birthdays = [
            obj.birthday.timetuple().tm_yday
            for obj in ModelTest.objects.order_by("birthday")
        ]

        # self.assertEqual(doys, [1, 2, 365])
        self.assertEqual(doys, sorted(obj_birthdays))

        doys = [
            getattr(obj, "birthday_dayofyear_internal")
            for obj in ModelTest.objects.order_by_birthday(True)
        ]
        # print("doys", doys)
        # print("obj_birthdays", obj_birthdays, sorted(obj_birthdays, reverse=True))
        self.assertEqual(doys, sorted(obj_birthdays, reverse=True))
        # self.assertEqual(doys, [365, 2, 1])

        years = [obj.birthday.year for obj in ModelTest.objects.order_by("birthday")]
        birthdays = sorted([int(b.split("-")[0]) for b in self.birthdays])

        self.assertEqual(years, birthdays)

    @classmethod
    def teardown_class(self):
        """テストclass実行の後処理"""

        print("teardown_class")
