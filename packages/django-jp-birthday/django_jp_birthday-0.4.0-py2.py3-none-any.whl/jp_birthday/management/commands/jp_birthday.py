from django.apps import apps
from django.core.management import BaseCommand, CommandError

# from django.db import models

from jp_birthday.models import BaseBirthdayModel


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):
        parser.add_argument("model_name", type=str, nargs="*")
        parser.add_argument("--method", nargs="?", default="", type=str)

    def handle(self, *args, **options):
        """
        Sometimes django-ordered-models ordering goes wrong, for various reasons,
        try re-ordering to a working state.
        """
        # print("options", options)
        # print("args", args)

        self.verbosity = options["verbosity"]
        base_birthday_models = [
            m._meta.label for m in apps.get_models() if issubclass(m, BaseBirthdayModel)
        ]
        candidates = "\n   {}".format("\n   ".join(base_birthday_models))

        # print("base_birthday_models", base_birthday_models)
        # print("candidates", candidates)

        for model_name in options["model_name"]:
            if model_name not in base_birthday_models:
                self.stdout.write(
                    "Model '{}' is not an ordered model, try: {}".format(
                        model_name, candidates
                    )
                )
                break

            model = apps.get_model(model_name)
            if not issubclass(model, BaseBirthdayModel):
                raise CommandError(
                    "{} does not inherit from OrderedModel or OrderedModelBase".format(
                        str(model)
                    )
                )

            method = options["method"]
            self.run_method(model, method)

            self.stdout.write("handle")

    def run_method(self, model: str, method: str, *args, **options):
        # all = model.objects.all()
        # print("all", all)

        method = "get_age"
        if method in dir(model):
            print("method", method)
            # print(dir(model))
