# Introduction

**WIP: This repository is a work in progress.**

![Handwriting Synthesis](./assets/improve_me_please.png)

This repository aims to build upon the work of [X-rayLaser's handwriting synthesis](https://github.com/X-rayLaser/pytorch-handwriting-synthesis-toolkit) and build upon it. More specifically, make it indistinguishable from human produced handwriting! 

The original repository is a toolkit for handwriting synthesis using recurrent neural networks. The implementation closely follows Alex Graves's paper [Generating Sequences With Recurrent Neural Networks](https://arxiv.org/abs/1308.0850). I highly recommend X-rayLaser's README and the paper for a great explanation of the model and the process.

In a nutshell, a model takes inputs in the shape of an array of tuple  (x-coord, y-coord, end_of_stroke) paired with a string of text. The model predicts the next pen coordinates and whether the pen is touching the surface. The result is a sequence of pen coordinates that form handwritten line of text.

Here, I will expand on the original work by:
1. Collecting and processing custom and more diverse dataset
1. Experimenting tweaking training parameters
1. Layer an additional model to account for pen pressure

# Methodology
## Custom Dataset

### Original Dataset
The original dataset used for training the model is the [IAM On-Line Handwriting Database](https://fki.tic.heia-fr.ch/databases/iam-on-line-handwriting-database). X-rayLaser's repository includes a script to download and prepare the data for training. The dataset consists of handwritten lines of text (strings) paired with the pen coordinates (arrays of tuples) used to write the text. The dataset is fairly large and diverse, making it a good starting point for training the model.

### Custom Dataset
I expanded the array of characters the model can produce by including both text and numbers in the new dataset. The text prompts are taken from a collection of famous speeches, and the numbers are generated randomly using [random_number_prompts.py](./utils/random_number_prompts.py).

### Hardware
I did not have access to the technology used to collect the original dataset. Instead, I used a Wacom Intuos tablet to collect the data. The tablet records the pen coordinates and whether the pen is touching the surface of the tablet. Additionally, it records pen pressure, which I will use to build a new model.

### Software
Wacom provides a software development kit (SDK) that allows developers to access data from the tablet. I used the web-based UI and SDK to collect the data and save it in a Universal Ink Model (UIM) file. I used [parse_uim.py](./utils/parse_uim.py) to convert the UIM files to the basic data format of (x, y, pen state, pressure).

### Comparison of Datasets
Todo: Add a comparison of the original dataset and the custom dataset.

## Preprocessing the Custom Dataset
Before loading the new dataset into a data provider, I needed to preprocess the data to match the format of the IAM dataset. Details can be found in [/notebooks](./notebooks).

## Building a New Data Provider
To prepare the new dataset for training, I built a new data provider called [CustomProvider](./handwriting_synthesis/data_providers/custom.py). The data provider reads the pen coordinates and the corresponding text from the preprocessed dataset and prepares it for training. I followed the instructions [here](https://github.com/X-rayLaser/pytorch-handwriting-synthesis-toolkit?tab=readme-ov-file#data-preparation).

## Training and Evaluating Experiments
I trained the model with four different datasets:
1. IAM dataset
2. Custom dataset
3. Combined dataset (IAM + Custom)
4. IAM dataset fine-tuned with the custom dataset

### IAM Training Metrics
#### Batch Size 32
<p float="left">
  <img src="./assets/iam_32_loss.png" width="30%" />
  <img src="./assets/iam_32_mse.png" width="30%" /> 
  <img src="./assets/iam_32_sse.png" width="30%" />
</p>

#### Batch Size 64
<p float="left">
  <img src="./assets/iam_64_loss.png" width="30%" />
  <img src="./assets/iam_64_mse.png" width="30%" /> 
  <img src="./assets/iam_64_sse.png" width="30%" />
</p>

### Custom Training Metrics

### Combined Training Metrics

### Fine-tuned IAM Dataset Metrics

### Results

## Building a New Model (In Progress)
Happy with the improved performance, I have decided to build an additional model that accounts for pen pressure. I will use "stroke thickness" as a proxy for pen pressure. Stay tuned for updates on this model!

# Todo
- [ ] Add a comparison of the original dataset and the custom dataset.
- [ ] Add a detailed section on the data provider.
- [ ] Add a section on the new model that accounts for pen pressure.
- [ ] Add training infrastructure section.
- [ ] Add priming section.
- [ ] Add dataflow automation with Prefect.
