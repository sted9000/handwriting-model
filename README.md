# Introduction

**WIP: This repository is a work in progress.**

![Handwriting Synthesis](./assets/improve_me_please.png)

This repository aims to build upon the work of [X-rayLaser's handwriting synthesis](https://github.com/X-rayLaser/pytorch-handwriting-synthesis-toolkit) and make it even better! The original repository is a toolkit for handwriting prediction and synthesis using recurrent neural networks. The implementation closely follows Alex Graves's paper [Generating Sequences With Recurrent Neural Networks](https://arxiv.org/abs/1308.0850). I highly recommend X-rayLaser's README and the paper for a great explanation of the model and the process.

Here, I will expand on the original work by:
1. Collecting a custom dataset of handwritten text
2. Building a preprocessing flow for the custom dataset
3. Creating a new data provider for the custom dataset
4. Experimenting with different ways to train the model
5. Developing an additional model to account for pen pressure and using "stroke thickness" as a proxy
6. Combining and evaluating the two models for handwriting synthesis

Additional features include:
- Visualization tools for training run metrics
- A tool for comparing new datasets to the original dataset

## Installation
Todo: Add installation instructions.

## Usage
Todo: Add usage instructions.

## Collecting a Custom Dataset

### Original Dataset
The original dataset used for training the model is the [IAM On-Line Handwriting Database](https://fki.tic.heia-fr.ch/databases/iam-on-line-handwriting-database). X-rayLaser's repository includes a script to download and prepare the data for training. The dataset consists of handwritten lines of text (strings) paired with the pen coordinates (arrays of tuples) used to write the text. The dataset is fairly large and diverse, making it a good starting point for training the model.

### Custom Dataset
I expanded the array of characters the model can produce by including both text and numbers in the new dataset. The text prompts are taken from a collection of famous speeches, and the numbers are generated randomly using `random_number_prompts.py`.

### Hardware
I did not have access to the technology used to collect the original dataset. Instead, I used a Wacom Intuos tablet to collect the data. The tablet records the pen coordinates and whether the pen is touching the surface of the tablet. Additionally, it records pen pressure, which I will use to build a new model.

### Software
Wacom provides a software development kit (SDK) that allows developers to access data from the tablet. I used the web-based UI and SDK to collect the data and save it in a Universal Ink Model (UIM) file. I used `parse_uim.py` to convert the UIM files to the basic data format of (x, y, pen state, pressure).

### Comparison of Datasets
Todo: Add a comparison of the original dataset and the custom dataset.

## Preprocessing the Custom Dataset
Before loading the new dataset into a data provider, I needed to preprocess the data to match the format of the IAM dataset. A summary is below, and detailed steps are in the repository's /notebooks folder.

## Building a New Data Provider
To prepare the new dataset for training, I built a new data provider called [CustomProvider](). The data provider reads the pen coordinates and the corresponding text from the preprocessed dataset and prepares it for training. I followed the instructions [here](https://github.com/X-rayLaser/pytorch-handwriting-synthesis-toolkit?tab=readme-ov-file#data-preparation).

<details>
  <summary>Data provider details</summary>

  ## Detailed Section
</details>

## Training and Evaluating Experiments
I trained the model in three different ways:
1. IAM dataset
2. Combined dataset (IAM + Custom)
3. IAM dataset fine-tuned with the custom dataset

### IAM Training Metrics
#### Batch Size 32
![iam_32_loss](./assets/iam_32_loss.png)
![iam_32_mse](./assets/iam_32_mse.png)
![iam_32_sse](./assets/iam_32_sse.png)

![iam_64_loss](./assets/iam_64_loss.png)
![iam_64_mse](./assets/iam_64_mse.png)
![iam_64_sse](./assets/iam_64_sse.png)

### Combined Training Metrics

### Fine-tuned IAM Dataset Metrics

### Training Results

## Building a New Model (In Progress)
Happy with the improved performance, I have decided to build an additional model that accounts for pen pressure. I will use "stroke thickness" as a proxy for pen pressure. Stay tuned for updates on this model!
