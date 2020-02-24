class TitleRatings:
    def __init__(self, dict):
        self.tconst = dict['tconst']
        
        self.averageRating = None if dict['averageRating'] == '\\N' else float(
            dict['averageRating'])
        
        self.numVotes = None if dict['numVotes'] == '\\N' else int(
            dict['numVotes'])

    @staticmethod
    def dict_to_obj(list):
        objects = []

        for i in list:
            objects.append(TitleRating(i))

        return objects