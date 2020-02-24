class TitleCrew:
    def __int__(self, dict):
        self.tconst = dict['tconst']

        self.directors = None if dict['directors'] == '\\N' else dict['directors'].split(
            ',')

        self.writers = None if dict['writers'] == '\\N' else dict['writers'].split(
            ',')

    @staticmethod
    def dict_to_obj(list):
        objects = []

        for i in list:
            objects.append(TitleCrew(i))

        return objects