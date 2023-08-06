import datetime
import json
import unicodedata
import jaconv

from jeraconv import jeraconv
from jeraconv.jeraconv import PATH_BASE, DIR_DATA, FILE_JSON


class JapanEra:
    def __init__(self, *args, **kwargs):
        self.filepath = PATH_BASE + "/" + DIR_DATA + "/" + FILE_JSON
        with open(self.filepath, encoding="utf-8_sig") as f:
            self.__data_dic = json.load(f)

        # west to japanera
        self.wtj = WestToJapanEra(self.__data_dic)

        # japanera to west
        self.jtw = JapanEraToWest(self.__data_dic)

        # print("PATH_BASE", PATH_BASE)
        # print("DIR_DATA", DIR_DATA)
        # print("FILE_JSON", FILE_JSON)

    def convert_to_jp_era(
        self,
        birthday=datetime.date.today(),
    ) -> dict:
        if isinstance(birthday, datetime.date):
            jp_era = self.wtj._convert_to_jp_era(
                int(birthday.year),
                int(birthday.month),
                int(birthday.day),
            )
            return jp_era

    def get_date_range_from_jp_era(self, jp_era: str) -> dict:
        """
        和暦から西暦の範囲を返す.

        Args:
            jp_era (str): 和暦

        Returns:
            dict: [description]
        """
        return self.jtw._get_date_range_from_jp_era(jp_era)

    # def convert(
    #     self,
    #     year=datetime.date.today().year,
    #     month=datetime.date.today().month,
    #     day=datetime.date.today().day,
    #     return_type='str'
    # ):
    #     pass

    def __pre_process(self, str_arg):
        """[summary]

        Args:
            str_arg ([type]): [description]
        """
        pass

    def __is_correct_format(self, str_arg):
        """[summary]

        Args:
            str_arg ([type]): [description]
        """
        pass

    def __is_correct_era(self, str_arg):
        """[summary]

        Args:
            str_arg ([type]): [description]
        """
        pass


class WestToJapanEra:
    def __init__(self, *args, **kwargs):
        self.data_dic = args[0]
        self.w2j = jeraconv.W2J()

    def convert(
        self,
        year=datetime.date.today().year,
        month=datetime.date.today().month,
        day=datetime.date.today().day,
        return_type="str",
    ):
        # return_type = "dict"
        era_date = self.w2j.convert(year, month, day, return_type)
        return era_date

    def _convert_to_jp_era(self, year: int, month: int, day: int) -> dict:
        """[summary]

        Args:
            year (int): [description]
            month (int): [description]
            day (int): [description]

        Returns:
            dict: [description]
        """
        date = self.convert(year, month, day, return_type="dict")

        era = date["era"]
        era_year = date["year"]

        reading = self.data_dic[era]["reading"]

        era_en = reading["en"]
        era_en_short = era_en[0]

        return {
            "era": era_en,
            "era_short": era_en_short,
            "year": int(era_year),
            "month": int(month),
            "day": int(day),
        }


class JapanEraToWest:
    def __init__(self, *args, **kwargs):
        self.data_dic = args[0]
        self.j2w = jeraconv.J2W()

    def _get_date_range_from_jp_era(self, jp_era: str) -> dict:
        """[summary]

        Args:
            jp_era (str): [description]

        Returns:
            dict: [description]
        """
        l_type = self._check_language(jp_era)

        data = None
        for key, value in self.data_dic.items():
            reading = value["reading"]

            reading_jp = reading["jp"]
            reading_en = reading["en"]

            if l_type == "kanji":
                if jp_era == key:
                    data = value
            elif l_type == "katakana" or l_type == "hiragana":
                jp_era = jaconv.kata2hira(jp_era)
                if jp_era == reading_jp:
                    data = value
                    break
            elif l_type == "english":
                if jp_era == reading_en:
                    data = value
                    break
            else:
                break
        return data

    def _check_language(self, string):
        l_type = ""
        for ch in string:
            name = unicodedata.name(ch)

            if "CJK UNIFIED" in name:
                l_type = "kanji"
            elif "HIRAGANA" in name:
                l_type = "hiragana"
            elif "KATAKANA" in name:
                l_type = "katakana"
            elif "LATIN" in name:
                l_type = "english"
            else:
                l_type = "none"
        return l_type
