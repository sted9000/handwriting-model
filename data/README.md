# Data
Prepare data for training the model. The idea is to be able to use lot of different data sources. To do so, we need some methods to format the data in a standardized way so that the model can use it.

## Usage
In order:
1. Add your data to the appropriate directory.
1. Add config file to the data directory.
1. format.ipynb
1. analyze.ipynb
1. package.ipynb

## format.ipynb
This notebook is used to format the data into a standardized format. The data is then saved in the data directory in the ```/lines```directory. 

The data is saved in the following structure: {'transcript': 'transcript', 'strokes': [stroke1, stroke2, ...]}

A stroke has the following format: [[x1, y1], [x2, y2], ...]

## Datasets
### IAM
Obtain and learn more about the data [here](http://www.fki.inf.unibe.ch/databases/iam-handwriting-database). To process the data, follow place the extracted data in the following structure and follow the instructions in the `format.ipynb` notebook.

```
data/
|-- IAM
    |-- ascii
    |-- lineStrokes
```

### Custom
To process the data custom data create a directory in /data with the data source's name and the file structure below. Create a ```config.yaml``` file, and then follow the instructions in the `format.ipynb` notebook.

```
data/
    |-- <your_data_source_directory>
        |-- raw_strokes
        |-- transcripts
        config.yaml
```
```yaml
# config.yaml
data_type: <your_custom_data_type>
```

