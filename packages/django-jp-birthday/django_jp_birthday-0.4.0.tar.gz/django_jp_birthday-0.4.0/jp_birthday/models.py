import datetime

from django.db import models

from datetime import date

from jp_birthday.fields import BirthdayField
from jp_birthday.managers import JpBirthdayManager
from jp_birthday.eras import JapanEra


class BaseBirthdayModel(models.Model):
    """BaseBirthdayModel"""

    objects = JpBirthdayManager()
    birthday = BirthdayField()

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def birthday_month(self):
        return self.birthday.timetuple().tm_mon

    @property
    def birthday_day(self):
        return self.birthday.timetuple().tm_mday

    @property
    def birthday_month_day(self):
        month = self.birthday.timetuple().tm_mon
        if 10 > month:
            month = "0" + str(month)

        day = self.birthday.timetuple().tm_mday
        if 10 > day:
            day = "0" + str(day)

        return str(month) + "-" + str(day)

    @property
    def birthday_tm_yday(self):
        return self.birthday.timetuple().tm_yday

    def _get_jp_era_birthday(self, birthday: datetime.date) -> dict:
        """
        西暦の誕生日から和暦の誕生日に変換する.

        Args:
            birthday (datetime.date): 自身の誕生日.

        Returns:
            dict: [description]
        """

        # print("get_jp_era", BaseBirthdayModel.objects)

        era = JapanEra()
        return era.convert_to_jp_era(birthday)

    def get_wareki_birthday(self, dict_type=False) -> object:
        """get wareki birthday

        Args:
            dict_type (bool, optional): 辞書型で返すか文字列で返すかのフォーマト指定. Defaults to False.

        Returns:
            object: dictで返すか文字列で返すのどちらかになる.
        """
        birthday = self.birthday
        wareki_birthday = self._get_jp_era_birthday(birthday)

        if not dict_type:
            wareki = wareki_birthday["era_short"]
            year = str(wareki_birthday["year"])
            month = str(wareki_birthday["month"])
            day = str(wareki_birthday["day"])
            wareki_birthday = wareki + "-" + year + "-" + month + "-" + day
        return wareki_birthday

    def get_age(self) -> int:
        """get age from birthday.

        誕生日を元に年齢を割り出して返す.

        Returns:
            int: age.
        """
        today = date.today()

        this_year_birthday = date(today.year, self.birthday.month, self.birthday.day)

        age = (today - self.birthday).days
        age = int(age / 365)

        if this_year_birthday > today:
            age -= 1

        return age

    def get_zodiac(self) -> str:
        """
        誕生日を元に干支を取得する.

        Returns:
            str: 干支を返す.
        """
        zodiacs = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

        birthday = self.birthday
        year = birthday.timetuple().tm_year

        num_zodiac = (year + 8) % 12
        zodiac = zodiacs[num_zodiac]

        return zodiac


class BirthdayModel(BaseBirthdayModel):
    """BirthdayModel"""

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # super(BirthdayModel, self).__init__(*args, **kwargs)
