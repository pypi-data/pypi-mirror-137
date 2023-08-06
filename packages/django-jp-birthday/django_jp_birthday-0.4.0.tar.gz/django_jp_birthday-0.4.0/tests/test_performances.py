import time

from faker import Faker
from datetime import datetime

from django.core.paginator import Paginator
from django.db import connection

# from django.db import backends
from django.test import TestCase
from django.conf import settings

from tests.models import ModelTestPost, ModelTestAuthor


class BirthdayTestPerformances(TestCase):
    @classmethod
    def setup_class(self):
        """テストclass実行の前処理"""

        print("setup_class")

    def setUp(self):
        fakegen = Faker("ja_JP")

        self.meiji = ["1905-1-2", "1905-1-1", "1905-2-1", "1905-2-2"]
        self.showa = ["1980-7-7", "1975-1-1", "1970-2-15"]
        self.heisei = ["2000-01-02", "2001-01-01", "2002-12-31", "2021-2-20"]

        self.birthdays = self.meiji + self.showa + self.heisei
        count = len(self.birthdays)
        # count = 5000
        count = 500

        self.birthdays = [str(fakegen.date_of_birth()) for _ in range(count)]
        for birthday in self.birthdays:
            name = fakegen.name()
            title = fakegen.text(max_nb_chars=30)
            text = fakegen.text(max_nb_chars=150)

            author = ModelTestAuthor(name=name)
            author.save()

            model_test = ModelTestPost(
                title=title,
                text=text,
                author=author,
                birthday=datetime.strptime(birthday, "%Y-%m-%d").date(),
            )
            model_test.save()

    def test_models_test_post_orm(self):

        # settings.DEBUG = True

        start = time.perf_counter()

        for m in ModelTestPost.objects.all():
            # name = m.author.name
            _ = m.author.name

        end = time.perf_counter()
        run_time_1 = end - start
        # self.assertTrue(run_time_1 > 1)

        start = time.perf_counter()
        for p in ModelTestPost.objects.prefetch_related("author").all():
            # print(p.author.name)
            # author_name = p.author.name
            _ = p.author.name

        end = time.perf_counter()
        run_time_2 = end - start
        self.assertTrue(1 > run_time_2)

        settings.DEBUG = False

        for query in connection.queries:
            # sql = query["sql"]
            _ = query["sql"]
            # print("sql: {0}".format(sql))

        print("run_time_1", run_time_1)
        print("run_time_2", run_time_2)

    def test_models_test_post_raw_sql(self):
        cur = connection.cursor()

        # N + 1
        start = time.perf_counter()

        db_table_name = ModelTestPost.objects.model._meta.db_table
        sql = "select * from {0}".format(db_table_name)
        for c in cur.execute(sql).fetchall():
            author_id = c[4]
            db_table_name = ModelTestAuthor.objects.model._meta.db_table

            sql = "select * from {0} where id=?".format(db_table_name)
            cur.execute(sql, (author_id,)).fetchone()

        end = time.perf_counter()
        run_time_1 = end - start
        # self.assertTrue(run_time_1 > 1)

        # prefetch_related
        start = time.perf_counter()

        db_table_name = ModelTestPost.objects.model._meta.db_table
        sql = "select * from {0}".format(db_table_name)

        post_table = cur.execute(sql).fetchall()
        db_table_test_author_name = ModelTestAuthor.objects.model._meta.db_table
        sql = "select * from {0}".format(db_table_test_author_name)
        sql += " where id in (" + ",".join([str(c[4]) for c in post_table]) + ")"
        # print("sql", sql)

        # cur.execute(
        #     sql,
        # ).fetchall()

        end = time.perf_counter()
        run_time_2 = end - start

        # values
        db_table_test_author_name = ModelTestAuthor.objects.model._meta.db_table
        name = "{0}__name".format("author")

        start = time.perf_counter()

        for values in ModelTestPost.objects.values(name).all():
            values["author__name"]
            # print("values", values['author__name'])

        end = time.perf_counter()
        run_time_3 = end - start

        print("run_time_1", run_time_1)
        print("run_time_2", run_time_2)
        print("run_time_3", run_time_3)

    def test_exists(self):
        # fakegen = Faker("ja_JP")

        # settings.DEBUG = True

        first_title = ModelTestPost.objects.filter(id=1).first().title

        start = time.perf_counter()

        # title = fakegen.text(max_nb_chars=30)
        exists = ModelTestPost.objects.filter(title=first_title).exists()
        print("exists 1", exists)

        end = time.perf_counter()
        run_time_1 = end - start

        start = time.perf_counter()

        # title = fakegen.text(max_nb_chars=30)
        exists = ModelTestPost.objects.filter(title=first_title).count() > 0
        print("exists 2", exists)

        end = time.perf_counter()
        run_time_2 = end - start

        print("first_title", first_title)
        print("test_exists run_time_1", run_time_1)
        print("test_exists run_time_2", run_time_2)

        settings.DEBUG = False

        for query in connection.queries:
            sql = query["sql"]
            print("sql", sql)

    def test_pagination(self):
        # settings.DEBUG = True

        page_num = 10
        # page_num = 1
        page_size = 50

        start = time.perf_counter()
        paginator = Paginator(ModelTestPost.objects.all(), page_size)
        post_tables = paginator.page(page_num).object_list
        for p in post_tables:
            # title = p.title
            _ = p.title
            # print(p.title)

        end = time.perf_counter()
        run_time_1 = end - start

        start = time.perf_counter()
        s = (page_num - 1) * page_size
        e = page_num * page_size
        post_tables = ModelTestPost.objects.all()[s:e]
        for p in post_tables:
            # title = p.title
            _ = p.title
            # print(p.title)

        end = time.perf_counter()
        run_time_2 = end - start

        print("test_pagination run_time_1", run_time_1)
        print("test_pagination run_time_2", run_time_2)

        settings.DEBUG = False

        for query in connection.queries:
            sql = query["sql"]
            print("sql", sql)

    @classmethod
    def teardown_class(self):
        """テストclass実行の後処理"""

        print("teardown_class")
