import os


class Dir:

    def __init__(self, fp):
        self.fp = fp

    def move_all_files(self, destination):
        """ move all files from Dir to new source """
        all_files = os.listdir(self.fp)

        # if Dir object is passed
        # if destination.fp:
        #     destination = destination.fp

        for f in all_files:
            os.rename(self.fp.joinpath(f), destination.joinpath(f))
