#!/bin/bash

# Load configuration variables
source config.sh

# Define the directory to be zipped
DATA_NAME="$1"

# Define the directories on the remote EC2 instance
DATA_DIR="$REMOTE_DIR/$REMOTE_TRAINING_DIR/$DATA_NAME"

# SSH And Zip both the model and the data
ssh -i "$EC2_KEY" $EC2_USER@$EC2_HOST << EOF
    cd $DATA_DIR
    zip -r $DATA_NAME.zip checkpoints samples train.log error.log
    echo "Zip file created on EC2 instance."
EOF

# Copy the zip file to the local machine
scp -i "$EC2_KEY" "$EC2_USER@$EC2_HOST:$DATA_DIR/$DATA_NAME.zip" "$LOCAL_DATA_DIR/$DATA_NAME/$DATA_NAME.zip"
echo "Zip file copied to local machine successfully."

# Unzip the file
unzip "$LOCAL_DATA_DIR/$DATA_NAME/$DATA_NAME.zip" -d "$LOCAL_DATA_DIR/$DATA_NAME"
echo "Zip file unzipped on local machine successfully."