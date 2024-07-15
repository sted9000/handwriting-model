import pickle
from iam_ondb import bounded_iterator
from .base import Provider, DataSplittingProvider
import os


# Create a subclasses of Provider here
class MyProvider(Provider):
    name = 'example'

    def get_training_data(self):
        raise NotImplementedError

    def get_validation_data(self):
        raise NotImplementedError


class DummyProvider(Provider):
    name = 'dummy'

    def get_training_data(self):
        handwriting = [
            [(1, 2), (1, 3), (2, 5)],
            [(10, 3), (15, 4), (18, 8)],
            [(22, 10), (20, 5)]
        ]

        transcript = 'Hi'
        yield handwriting, transcript

    def get_validation_data(self):
        handwriting = [
            [(1, 2), (1, 3), (2, 5)],
            [(10, 3), (15, 4), (18, 8)],
            [(22, 10), (20, 5)]
        ]

        transcript = 'Hi'
        yield handwriting, transcript

#

class Ink:

    def __init__(self, coord_path, transcript_path):
        self.coord_path = coord_path
        self.transcript_path = transcript_path

    def __iter__(self):

        for file in self.file_names(self.coord_path):
            print(file)
            strokes, transcript = self.get_data(file)
            yield strokes, transcript

    def file_names(self, path):
        for x in os.listdir(path):
            yield x

    def get_data(self, file):
        strokes = pickle.load(open(os.path.join(self.coord_path, file), 'rb'))
        with open(os.path.join(self.transcript_path, file[:-4] + '.txt'), 'r') as f:
            transcript = f.read().strip()

        return strokes, transcript


class InkProvider(DataSplittingProvider):
    name = 'ink'

    def __init__(self, training_data_size, validation_data_size=0, data_dir=None):
        if data_dir is None:
            print('No data directory specified. Using default directory.')
            exit()

        training_data_size, validation_data_size = self._parse_args(training_data_size,
                                                                    validation_data_size)

        iterator = self.get_generator(training_data_size, validation_data_size, data_dir)
        super().__init__(iterator, training_data_size, validation_data_size)

    def _parse_args(self, training_data_size, validation_data_size):
        return int(training_data_size), int(validation_data_size)

    def get_generator(self, training_data_size, validation_data_size, data_dir):
        db = Ink(os.path.join(data_dir, 'pkl'), os.path.join(data_dir, 'txt'))

        if validation_data_size:
            num_examples = training_data_size + validation_data_size
            it = bounded_iterator(db, num_examples)
        else:
            it = db.__iter__()

        for strokes, text in it:
            yield strokes, text

