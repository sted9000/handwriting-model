import pickle
from iam_ondb import bounded_iterator
from .base import DataSplittingProvider
import os


class Custom:

    def __init__(self, data_dir):
        self.data_dir = data_dir

    def __iter__(self):

        for file in self.file_names(self.data_dir):
            strokes, transcript = self.get_data(file)
            yield strokes, transcript

    def file_names(self, path):
        for x in os.listdir(path):
            yield x

    def get_data(self, file):
        # load the pickle file
        print(file)
        content = pickle.load(open(os.path.join(self.data_dir, file), 'rb'))
        transcript = content['transcript']
        strokes = content['strokes']

        return strokes, transcript


class CustomProvider(DataSplittingProvider):
    name = 'custom'

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
        db = Custom(data_dir)

        if validation_data_size:
            num_examples = training_data_size + validation_data_size
            it = bounded_iterator(db, num_examples)
        else:
            it = db.__iter__()

        for strokes, text in it:
            yield strokes, text
