from jeraconv import jeraconv


class JpEra:
    def __init__(self, *args, **kwargs):
        self.j2w = jeraconv.J2W()

    def __convert_to_jp_era(self, year: int, month: int, day: int) -> dict:
        """[summary]

        Args:
            year (int): [description]
            month (int): [description]
            day (int): [description]

        Returns:
            dict: [description]
        """
        pass

    def convert(self, str_arg, limit_check=True):
        pass

    def __pre_process(self, str_arg):
        pass

    def __is_correct_format(self, str_arg):
        pass

    def __is_correct_era(self, str_arg):
        pass
