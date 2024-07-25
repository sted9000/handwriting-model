#!/bin/bash

# Load configuration variables
source config.sh

# Define the directory to be zipped
DATA_NAME="$1"
TRAINING_SIZE="$2"
VALIDATION_SIZE="$3"

# Define the directories on the remote EC2 instance
DATA_DIR="$REMOTE_DIR/$REMOTE_TRAINING_DIR/$DATA_NAME"
MODEL_DIR="$DATA_DIR/checkpoints"
SAMPLES_DIR="$DATA_DIR/samples"

# Check if the local directory exists
if [ ! -d "$LOCAL_DATA_DIR/$DATA_NAME" ]; then
  echo "Error: Directory $LOCAL_DATA_DIR/$DATA_NAME does not exist."
  exit 1
fi

# Run prepare_data.py to create the training and validation datasets
cd sequence_model || exit
python3 prepare_data.py "../$LOCAL_DATA_DIR/$DATA_NAME" "$DATA_PROVIDER" "$TRAINING_SIZE" "$VALIDATION_SIZE" "../$LOCAL_DATA_DIR/$DATA_NAME/lines"
cd - || exit

# Create a zip file from the specified directory, excluding the specified subdirectory
cd "$LOCAL_DATA_DIR/$DATA_NAME" || exit
zip -r $ZIP_FILE . -x "./$EXCLUDE_DIR/*"
cd - || exit

# Create the remote directory if it does not exist
ssh -i "$EC2_KEY" $EC2_USER@$EC2_HOST "mkdir -p $DATA_DIR"

# Copy the zip file to the EC2 instance
scp -i "$EC2_KEY" "$LOCAL_DATA_DIR/$DATA_NAME/$ZIP_FILE" "$EC2_USER@$EC2_HOST:$DATA_DIR"

# Run additional commands on the EC2 instance after copying
ssh -i "$EC2_KEY" $EC2_USER@$EC2_HOST << EOF
    cd $DATA_DIR
    unzip -o $ZIP_FILE
    rm $ZIP_FILE
    echo "Unzipped and removed the zip file on EC2 instance."

    # Create the model directory if it does not exist
    mkdir -p $MODEL_DIR

    # Activate the virtual environment
    cd $REMOTE_DIR
    source venv/bin/activate && echo "Virtual environment activated" >> $DATA_DIR/train.log


    # Start the training script using nohup with additional parameters
    nohup python3 -u $TRAINING_SCRIPT -b $BATCH_SIZE -e $EPOCHS -i $SAMPLING_INTERVAL --samples_dir $SAMPLES_DIR $DATA_DIR $MODEL_DIR > $DATA_DIR/train.log 2> $DATA_DIR/error.log &
    echo "Started the training script using nohup."
EOF

echo "Zip file created, copied, unzipped, and removed on EC2 instance successfully. Training script started."
