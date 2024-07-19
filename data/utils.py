import os
from collections import defaultdict

import ipywidgets as widgets
import yaml
from IPython.display import display
import pickle
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from uim.codec.parser.uim import UIMParser
from uim.model.ink import InkModel
from uim.model.inkinput.inputdata import InputContext, SensorContext
from uim.model.inkinput.sensordata import SensorData

"""
Helper Functions
"""


class CheckboxSelector:
    def __init__(self, options, prompt):
        self.checkboxes = [widgets.Checkbox(value=False, description=option) for option in options]
        self.prompt = prompt

    def display(self):
        print(self.prompt)
        for checkbox in self.checkboxes:
            display(checkbox)

    def get_selected_items(self):
        selected_items = [checkbox.description for checkbox in self.checkboxes if checkbox.value]
        return selected_items


def has_formatted_data(data_source):
    return os.path.exists(f'./{data_source}/lines')


def plot_line(file):
    file = unpickle(file)
    transcript = file['transcript']
    strokes = file['strokes']
    for stroke in strokes:
        x = [point[0] for point in stroke]
        y = [point[1] for point in stroke]
        # invert the y axis
        y = [-i for i in y]
        plt.plot(x, y)

    # stretch the plot to match the aspect ratio of the text
    plt.gca().set_aspect('equal', adjustable='box')
    print(transcript)
    return plt.show()


def plot_line_from_strokes(strokes):
    for stroke in strokes:
        x = [point[0] for point in stroke]
        y = [point[1] for point in stroke]
        # invert the y axis
        y = [-i for i in y]
        plt.plot(x, y)

    # stretch the plot to match the aspect ratio of the text
    plt.gca().set_aspect('equal', adjustable='box')
    return plt.show()



def unpickle(file):
    with open(file, 'rb') as f:
        return pickle.load(f)


def get_line_files(root, data_source):
    lines_dir = f'{root}/{data_source}/lines'
    return os.listdir(lines_dir)


"""
Analyze Functions
"""


def clean_transcript_characters(characters):
    # remove white space
    characters = characters.replace(' ', '')
    # remove new lines
    characters = characters.replace('\n', '')
    # remove periods
    characters = characters.replace('.', '')
    # remove commas
    characters = characters.replace(',', '')
    # remove colons
    characters = characters.replace(':', '')
    # remove semicolons
    characters = characters.replace(';', '')
    # remove apostrophes
    characters = characters.replace('\'', '')
    # remove quotation marks
    characters = characters.replace('"', '')
    # remove hyphens
    characters = characters.replace('-', '')

    return characters


"""
IAM Functions
"""


def list_files(directory, ext):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(ext):
                yield os.path.join(root, file)


def lines_from_file(file):
    """
    Get transcript lines from a file
    """
    with open(file, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if line]
        lines = lines[lines.index('CSR:') + 1:]
        return lines


def save_line(line, index, file):
    """
    Save lines individually to new files
    """
    # split the file path
    path_as_list = file.split('/')
    # format the index to have 2 digits and to start at 1
    index = str(index + 1).zfill(2)
    # add the index to the file name (counting from 1)
    path_as_list[-1] = path_as_list[-1].replace('.txt', f'-{index}.txt')
    # join the path back together
    new_file = '/'.join(path_as_list)
    # write the line to the new file
    with open(new_file, 'w') as f:
        f.write(line)


def strokes_from_file(file):
    """
    Get strokes from an XML file
    """
    tree = ET.parse(file)
    root = tree.getroot()
    strokes = []
    for stroke in root.iter('Stroke'):
        points = []
        for point in stroke.iter('Point'):
            x = int(point.attrib['x'])
            y = int(point.attrib['y'])
            points.append((x, y))
        strokes.append(points)
    return strokes


def format_iam_data():
    # make dir to store the lines
    lines_dir = './IAM/lines'
    if not os.path.exists(lines_dir):
        os.makedirs(lines_dir)

    # iterate through the xml files
    for i, file in enumerate(list_files('./IAM/lineStrokes', '.xml')):

        # see if the corresponding ascii file exists
        line_strokes_pth = file.split('/')
        ascii_pth = line_strokes_pth.copy()
        ascii_pth[2] = 'ascii'
        ascii_pth[-1] = ascii_pth[-1].replace('xml', 'txt')
        ascii_pth = '/'.join(ascii_pth)
        if not os.path.exists(ascii_pth):
            print(f'File {file} has no matching ascii file {ascii_pth}.')
            continue

        # get the strokes from the xml file
        strokes = strokes_from_file(file)

        # packaged the strokes with the transcript
        with open(ascii_pth, 'r') as f:
            transcript = f.read()
        line = {'transcript': transcript, 'strokes': strokes, 'original_file_name': file}
        with open(f'{lines_dir}/{i}.pkl', 'wb') as f:
            pickle.dump(line, f)


"""
UIM_V1_Functions
"""


def create_lines_from_strokes(s, coord_constant):
    # input list of strokes which are lists comprised of tuples - (x, y)
    # output list of lines which are lists of strokes which are lists of tuples - (x, y)
    lines = []
    line = []
    for i, stroke in enumerate(s):
        # if first stroke, add to line
        if i == 0:
            line.append(stroke)
            continue
        # if not first stroke, check if it's the start of a new line
        else:
            first_point = stroke[0]
            first_x = first_point[0]
            first_y = first_point[1]
            # against the last point in the previous stroke
            last_point = s[i - 1][-1]
            last_x = last_point[0]
            last_y = last_point[1]

            # if it is, start a new line
            if last_x - first_x > (.01 * coord_constant) and first_y - last_y > (
                    .015 * coord_constant):
                # add the previous line to lines
                lines.append(line)
                # start a new line
                line = [stroke]
            # if it isn't, add to the current line
            else:
                line.append(stroke)

    lines.append(line)

    return lines


def parse_uim_file(uim_file_path, coord_constant):
    # input uim file
    # output list of strokes - (x, y) coordinates
    parser: UIMParser = UIMParser()
    ink_model: InkModel = parser.parse(uim_file_path)
    if ink_model.has_ink_structure():
        strokes = []
        for stroke in ink_model.strokes:
            x = []
            y = []
            p = []
            sd: SensorData = ink_model.sensor_data.sensor_data_by_id(stroke.sensor_data_id)
            input_context: InputContext = ink_model.input_configuration.get_input_context(sd.input_context_id)
            sensor_context: SensorContext = ink_model.input_configuration \
                .get_sensor_context(input_context.sensor_context_id)
            for scc in sensor_context.sensor_channels_contexts:
                for c in scc.channels:
                    if c.type.name == 'X':
                        x = sd.get_data_by_id(c.id).values
                    if c.type.name == 'Y':
                        y = sd.get_data_by_id(c.id).values
                    if c.type.name == 'PRESSURE':
                        p = sd.get_data_by_id(c.id).values
            current_stroke = []
            for i in range(len(x)):
                current_stroke.append((round(x[i] * coord_constant), round(y[i] * coord_constant), round(p[i] * 100)))
            strokes.append(current_stroke)
        return strokes


def files_to_lines(pth, files, lines_per_sample, coord_constant):
    # parse the uim files
    lines = []
    files_to_remove = []
    for i, file in enumerate(files):

        # turn the uim file into a list of strokes
        strokes = parse_uim_file(os.path.join(pth, file), coord_constant)

        # split the strokes into lines
        uim_lines = create_lines_from_strokes(strokes, coord_constant)

        # print a warning if not four lines (should be zero or one (the last one))
        if len(uim_lines) != lines_per_sample:
            if i != len(files) - 1:
                print(f'Warning: Last file {file} has {len(uim_lines)} lines')
            lines += [None for _ in range(lines_per_sample)]
            continue

        # add the lines to all_lines
        lines += uim_lines

    return lines


def format_uim_v1_data(data_source):
    # get the config file
    config_file = os.path.join(data_source, 'config.yaml')
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    # get the files and order them
    uim_path = os.path.join(data_source, 'raw_strokes')
    files = os.listdir(uim_path)
    files.sort(key=lambda x: int(x.split('.')[0]))

    # get the lines from the files
    lines = files_to_lines(uim_path, files, config['lines_per_sample'], config['coord_constant'])

    # remove blacklisted lines
    blacklisted_transcripts = config['blacklisted_transcripts']

    # save the lines with the transcripts
    output_dir = f'{data_source}/lines'
    os.makedirs(output_dir, exist_ok=True)
    print(f'Length of lines: {len(lines)}')
    for i, line in enumerate(lines):
        if i not in blacklisted_transcripts:
            if line is not None:
                print(f'Line {i} is not None')
                if os.path.exists(f'{data_source}/transcripts/{i}.txt'):
                    print(f'Tscr exists')
                    transcript = open(f'{data_source}/transcripts/{i}.txt', 'r').read()
                    with open(f'{output_dir}/{i}.pkl', 'wb') as fp:
                        pickle.dump({'transcript': transcript, 'strokes': line}, fp)


"""
Analyzers
"""


def analyze_characters(root, ds):
    characters = 0
    spaces = 0
    clean_characters = 0
    character_dict = defaultdict(int)
    for file in get_line_files(root, ds):
        # turn the pkl file into a list of strokes
        with open(f'{root}/{ds}/lines/{file}', 'rb') as f:
            strokes_file = pickle.load(f)
            transcript = strokes_file['transcript']

            # count the number of characters in the transcript
            characters += len(transcript)

            # get the number of spaces in the transcript
            spaces += transcript.count(' ')

            # count the number of 'clean'
            clean_characters += len(clean_transcript_characters(transcript))

            for character in transcript:
                character_dict[character] += 1

    return characters, spaces, clean_characters, character_dict


def analyze_points(root, ds):
    points = 0
    for file in get_line_files(root, ds):
        # turn the pkl file into a list of strokes
        with open(f'{root}/{ds}/lines/{file}', 'rb') as f:
            strokes_file = pickle.load(f)
            strokes = strokes_file['strokes']

            # count the number of points in the strokes
            for stroke in strokes:
                points += len(stroke)

    return points


def analyze_width(root, ds):
    width = 0
    for file in get_line_files(root, ds):
        # turn the pkl file into a list of strokes
        with open(f'{root}/{ds}/lines/{file}', 'rb') as f:
            strokes_file = pickle.load(f)
            strokes = strokes_file['strokes']

            # extend the total width
            first_stroke = strokes[0]
            last_stroke = strokes[-1]
            x_min_first_stroke = min([point[0] for point in first_stroke])
            x_max_last_stroke = max([point[0] for point in last_stroke])
            width += x_max_last_stroke - x_min_first_stroke

    return width
