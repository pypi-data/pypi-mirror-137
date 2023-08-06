from django.db import models

from jp_birthday.models import BirthdayModel


class ModelTest(BirthdayModel):
    class Meta:
        app_label = "jp_birthday"
        ordering = ("pk",)


class ModelTestAuthor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ModelTestPost(BirthdayModel):
    class Meta:
        app_label = "jp_birthday"
        ordering = ("pk",)

    title = models.CharField("title", max_length=255)
    text = models.TextField("Text")
    author = models.ForeignKey(
        ModelTestAuthor, verbose_name="author", on_delete=models.PROTECT
    )
