class TitleAkas:
    def __init__(self, dict):
        self.titleId  = dict['titleId']
        self.ordering = dict['ordering']
        self.title    = dict['title']

        self.region = None if dict['region'] == '\\N' else int(
            dict['region'])

        self.language = None if dict['language'] == '\\N' else int(
            dict['language'])

        self.types = None if dict['types'] == '\\N' else int(
            dict['types'])

        self.attributes = None if dict['attributes'] == '\\N' else int(
            dict['attributes'])

        self.isOriginalTitle = None if dict['isOriginalTitle'] == '\\N' else int(
            dict['isOriginalTitle'])

    @staticmethod
    def dict_to_obj(list):
        objects = []

        for i in list:
            objects.append(TitleAkas(i))

        return objects