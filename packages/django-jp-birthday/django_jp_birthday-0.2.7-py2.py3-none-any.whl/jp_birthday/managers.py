from django.conf import settings

from django.db import models, router, connection, backends
from django.db.models import Case, When, Value, IntegerField, QuerySet
from django.db.models.query_utils import Q

# from django.db.models.query_utils import Q

from jeraconv import jeraconv

# from math import pow
from datetime import datetime, date, time, timedelta
import pytz

import unicodedata
import jaconv


class JpBirthdayQuerySet(QuerySet):
    def __init__(self, model=None, query=None, using=None, hints=None):
        super().__init__(model, query, using, hints)

    def order_by_ids_filter(self, ids: list):
        cases = [When(id=id, then=Value(i + 1)) for i, id in enumerate(ids)]

        birthdays = (
            self.filter(id__in=ids)
            .annotate(md_order=Case(*cases, output_field=IntegerField()))
            .order_by("md_order")
        )

        return birthdays


class JpBirthdayManager(models.Manager):
    """[summary]

    Args:
        models ([type]): [description]
    """

    CASE = "CASE WHEN %(bdoy)s<%(cdoy)s THEN %(bdoy)s+365 ELSE %(bdoy)s END"
    j2w = jeraconv.J2W()

    @property
    def _birthday_doy_field(self):
        # print("self.model", self.model)
        # print("self.model._meta", self.model._meta)
        # print("self.model._meta.birthday_field", self.model._meta.birthday_field)
        # print("doy_name", self.model._meta.birthday_field.doy_name)

        return self.model._meta.birthday_field.doy_name

    def _doy(self, day):
        if not day:
            day = date.today()
        return day.timetuple().tm_yday

    def _order(self, reverse=False, case=False) -> QuerySet:
        """[summary]

        Args:
            reverse (bool, optional): Trueの場合は逆順にする. Defaults to False.
            case (bool, optional): [description]. Defaults to False.

        Returns:
            QuerySet: qs.order_byの結果を返す.
        """

        # print("~~~" * 30)

        cdoy = date.today().timetuple().tm_yday
        bdoy = self._birthday_doy_field
        doys = {"cdoy": cdoy, "bdoy": bdoy}

        if case:
            # print("CASE", self.CASE % doys)
            qs = self.extra(select={"internal_bday_order": self.CASE % doys})
            order_field = "internal_bday_order"
        else:
            qs = self.all()
            order_field = bdoy

        order_by = "%s" % order_field
        if reverse:
            order_by = "-%s" % order_field

        results = qs.order_by(order_by)
        return results

    def get_queryset(self):
        return JpBirthdayQuerySet(self.model, using=self._db)

    def cursor_filter_ids(self, cursor: backends.utils.CursorWrapper) -> list:
        columns = [col[0] for col in cursor.description]
        ids = [dict(zip(columns, row))["id"] for row in cursor.fetchall()]

        return ids

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

    def get_wareki_birthdays(self, wareki: str):
        """[summary]

        Args:
            wareki (str): [description]
        """

        l_type = self._check_language(wareki)

        data = None
        for key, value in self.j2w._J2W__data_dic.items():
            reading = value["reading"]

            reading_jp = reading["jp"]
            reading_en = reading["en"]

            if l_type == "kanji":
                if wareki == key:
                    data = value
            elif l_type == "katakana" or l_type == "hiragana":
                wareki = jaconv.kata2hira(wareki)
                if wareki == reading_jp:
                    data = value
                    break
            elif l_type == "english":
                if wareki == reading_en:
                    data = value
                    break
            else:
                break

        if data:
            start = data["start"]
            end = data["end"]

            start_date = str(start["year"]) + "-"
            start_date += str(start["month"]) + "-"
            start_date += str(start["day"])

            end_date = str(end["year"]) + "-"
            end_date += str(end["month"]) + "-"
            end_date += str(end["day"])

            range_birthdays = self.filter(birthday__range=[start_date, end_date])
            return range_birthdays
        return self.filter(birthday=None)

    def _get_upcoming_birthdays(
        self, days=30, after=None, include_day=True, order=True, reverse=False
    ) -> JpBirthdayQuerySet:
        """[summary]

        Args:
            days (int, optional): [description]. Defaults to 30.
            after ([type], optional): [description]. Defaults to None.
            include_day (bool, optional): [description]. Defaults to True.
            order (bool, optional): [description]. Defaults to True.
            reverse (bool, optional): [description]. Defaults to False.

        Returns:
            JpBirthdayQuerySet: [description]
        """
        today = self._doy(after)
        limit = today + days

        q = Q(
            **{
                "%s__gt%s"
                % (self._birthday_doy_field, "e" if include_day else ""): today
            }
        )
        q &= Q(**{"%s__lt" % self._birthday_doy_field: limit})

        if limit > 365:
            limit = limit - 365
            today = 1

            q2 = Q(**{"%s__gte" % self._birthday_doy_field: today})
            q2 &= Q(**{"%s__lt" % self._birthday_doy_field: limit})
            q = q | q2

        if order:
            qs = self._order(reverse, True)
            return qs.filter(q)

        return self.filter(q)

    def get_upcoming_birthdays(
        self, days=30, after=None, include_day=True, order=True, reverse=False
    ) -> JpBirthdayQuerySet:
        """get_upcoming_birthdays

        Args:
            days (int, optional): [description]. Defaults to 30.
            after ([type], optional): [description]. Defaults to None.
            include_day (bool, optional): [description]. Defaults to True.
            order (bool, optional): [description]. Defaults to True.
            reverse (bool, optional): [description]. Defaults to False.

        Returns:
            JpBirthdayQuerySet: [description]
        """

        return self._get_upcoming_birthdays(30, after, include_day, order, reverse)

        db_route = router.db_for_read(self)
        engine = settings.DATABASES[db_route]["ENGINE"]
        db_table_name = self.model._meta.db_table

        cursor = connection.cursor()

        if after:
            after = datetime.combine(after, time())
            after = pytz.timezone("Asia/Tokyo").localize(after)
        else:
            after = datetime.now()

        print("include_day", include_day)
        print("after", after)
        if not include_day:
            after += timedelta(days=1)
            days -= 1
        days = str(days)

        after = after.date()
        after_str = "'{0}'".format(after)

        sql = "select {0}.*, ".format(db_table_name)
        if "sqlite3" in engine:
            sql += "strftime('%m-%d', birthday) as md "
            sql += "from {0} where md ".format(db_table_name)
        else:
            pass

        next = date(year=int(after.year), month=12, day=31) - after

        try:
            ids = []
            if int(days) > next.days:
                diff = int(days) - next.days

                sql_1 = sql
                if "sqlite3" in engine:
                    # sql_1 += "> strftime('%m-%d', {0})".format(after_str)
                    sql_1 += ">= strftime('%m-%d', {0})".format(after_str)
                else:
                    pass

                if order:
                    sql_1 += " order by md asc;"

                cursor.execute(sql_1)
                ids += self.cursor_filter_ids(cursor)

                sql_2 = sql
                if "sqlite3" in engine:
                    sql_2 += "between "
                    sql_2 += "strftime('%m-%d', {0}) and ".format("'2000-01-01'")
                    sql_2 += (
                        "strftime('%m-%d', date({0}, 'localtime', '+{1} day'))".format(
                            "'2000-01-01'", str(diff)
                        )
                    )
                else:
                    pass

                if order:
                    sql_2 += " order by md asc;"

                cursor.execute(sql_2)
                ids += self.cursor_filter_ids(cursor)
            else:
                between_sql = "between "
                if "sqlite3" in engine:
                    between_sql += "strftime('%m-%d', {0}) and ".format(after_str)
                    between_sql += (
                        "strftime('%m-%d', date({0}, 'localtime', '+{1} day'))".format(
                            after_str, days
                        )
                    )

                    # sql += " order by birthday asc;"
                else:
                    pass

                sql += between_sql
                if order:
                    sql += " order by md asc;"

                print("sql", sql)

                cursor.execute(sql)
                ids += self.cursor_filter_ids(cursor)

            print("ids*******", ids)

            if reverse:
                ids.reverse()

            birthdays = self.get_queryset().order_by_ids_filter(ids)

            return birthdays
        finally:
            # print("cursor", type(cursor))
            cursor.close()

    def get_birthdays(self, day=None) -> JpBirthdayQuerySet:
        """[summary]

        Args:
            day ([type], optional): [description]. Defaults to None.

        Returns:
            JpBirthdayQuerySet: [description]
        """
        # print("~~~" * 30)
        # print("get_birthdays")
        # print("self._doy(day)", self._doy(day))
        # print("_birthday_doy_field", self._birthday_doy_field)

        get_birthdays = self.filter(**{self._birthday_doy_field: self._doy(day)})
        # print("get_birthdays", get_birthdays, type(get_birthdays))

        return get_birthdays

    def order_by_birthday(self, reverse=False) -> JpBirthdayQuerySet:
        """生まれた年は関係なく誕生日順に並べる

        Args:
            reverse (bool, optional): Trueの場合は逆順にする. Defaults to False.

        Returns:
            JpBirthdayQuerySet: QuerySetの結果を返す.
        """

        return self._order(reverse)
