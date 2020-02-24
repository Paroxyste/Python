import csv

class TSV :
    def __init__(self, filepath):
        # TODO check if the file exists
        self.fh = open(filepath, 'rt')

        # TODO What if there is no header in the file ?
        self.header = self.fh.readline()

    def read_sequential(self, n):
        lines_list = []
        line = self.sh.readline()
        curr_line = None
        counter = 0

        while line and counter < n:
            lines_list.append(line)
            counter += 1
            line = self.sh.readline()

        if len(lines_list) == 0:
            return None

        lines_list.insert(0, self.header)
        line_as_dict = csv.DictReader(lines_list, 
                                      delimiter = '\t', 
                                      quoting = csv.QUOTE_NONE)

        return line_as_dict