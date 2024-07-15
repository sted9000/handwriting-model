# Introduction

This repository aims to take the work of [X-rayLaser's handwriting synthesis](https://github.com/X-rayLaser/pytorch-handwriting-synthesis-toolkit) and make it even better! The original repository is a toolkit for doing handwriting prediction and handwriting synthesis with recurrent neural networks. The implementation closely follows Alex Graves's paper [Generating Sequences With Recurrent Neural Networks](https://arxiv.org/abs/1308.0850). I highly recommend X-rayLaser's README and the paper for a great explanation of the model and the process.

Here I will expand on the original work by:
1. Collecting a custom dataset of handwritten text
2. Building a new data provider for the custom dataset
3. Train and evaluate the model on the custom data
4. Build an additional model to account for pen pressure and use "stroke thickness" as a proxy
5. Combine and evaluate the combination of the two models for handwriting synthesis

Also included are:
- Visualization tools for training run metrics
- Tool for comparison of new datasets to the original dataset

## Collecting a Custom Dataset
### Original Dataset
The original dataset used for training the model is the [IAM On-Line Handwriting Database](https://fki.tic.heia-fr.ch/databases/iam-on-line-handwriting-database). X-rayLaser's repository includes a script to download and prepare the data for training. The dataset consists of handwritten lines of text (string) paired with the pen coordinates (array of tuples) to write the text. The dataset is fairly large and diverse, making it a good starting point for training the model.

I included text and numbers in the new dataset to see how the model performs on different types of data. The text prompts are taken from a collection of famous speeches, and the numbers are generated using a script.

### Hardware
I did not have access to the technology that was used to collect the original dataset. Instead, I used a Wacom Intuos tablet to collect the data. The tablet records the pen coordinates and whether the pen is touching surface of the tablet. Additionally, it records pen pressure, which I will use to build a new model.

### Software
Wacom provides a software development kit (SDK) that allows developers to access the data from the tablet. I used the web-based UI and SDK to collect the data and save it. The output file is call Universal Ink Model (uim). I used python script was used to convert the uim files to the basic data format (x, y, pen state, pressure).

### Comparison of Datasets

## Building a New Data Provider
To prepare the new dataset for training, I built a new data provider called [NumbersProvider](). The data provider reads the pen coordinates and the corresponding text from the dataset and prepares it for training. I followed the instructions [here](https://github.com/X-rayLaser/pytorch-handwriting-synthesis-toolkit?tab=readme-ov-file#data-preparation) and detailed how the provider works and my learnings below.

<details>
    <summary>Data provider details</summary>

    ## Detailed Section
</details>

<details>
    <summary>My learnings</summary>

    ## Detailed Section
</details>

Before training the model I want to compaare input samples from the IAD dataset and the custom dataset. I will use the `compare_datasets.py` script to visualize the differences between the two datasets. Below are the results of the comparison.

## Training and Evaluating the Model
I trained the model three different ways:
1. IAM dataset
2. Combined dataset (IAM + Custom)
3. IAM dataset fine-tuned with the custom dataset

### IAM Training Metrics

### Combined Training Metrics

### Fine-tuned IAM Dataset Metrics

### Training Results

## Building a New Model (In Progress)
Happy enough with the improved performance, I have decided to build an additional model that accounts for pen pressure. I will use the "stroke thickness" as a proxy for pen pressure. Stay tuned for updates on this model! 

## Other
- Character distribution comparison