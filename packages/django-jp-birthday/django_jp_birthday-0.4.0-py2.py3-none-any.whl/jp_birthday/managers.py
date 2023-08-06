from django.conf import settings

from django.db import models, router, connection, backends
from django.db.models import Case, When, Value, IntegerField, QuerySet
from django.db.models.query_utils import Q

from jp_birthday.eras import JapanEra

from datetime import date


class JpBirthdayQuerySet(QuerySet):
    def __init__(self, model=None, query=None, using=None, hints=None):
        super().__init__(model, query, using, hints)


class JpBirthdayManager(models.Manager):
    """[summary]

    Args:
        models ([type]): [description]
    """

    CASE = "CASE WHEN %(bdoy)s<%(cdoy)s THEN %(bdoy)s+365 ELSE %(bdoy)s END"

    _era = JapanEra()

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

    def get_wareki_birthdays(self, wareki: str) -> QuerySet:
        """
        入力された和暦の誕生日を抽出

        Args:
            wareki (str): 和暦 (大正,昭和,平成,令和)

        Returns:
            QuerySet: 対象とするQuerySet
        """

        # datetime.date型の範囲を取得
        data = self._era.get_date_range_from_jp_era(wareki)

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

    def get_birthdays(self, day=None) -> JpBirthdayQuerySet:
        """[summary]

        Args:
            day ([type], optional): [description]. Defaults to None.

        Returns:
            JpBirthdayQuerySet: [description]
        """
        get_birthdays = self.filter(**{self._birthday_doy_field: self._doy(day)})
        return get_birthdays

    def order_by_birthday(self, reverse=False) -> JpBirthdayQuerySet:
        """生まれた年は関係なく誕生日順に並べる

        Args:
            reverse (bool, optional): Trueの場合は逆順にする. Defaults to False.

        Returns:
            JpBirthdayQuerySet: QuerySetの結果を返す.
        """

        return self._order(reverse)
