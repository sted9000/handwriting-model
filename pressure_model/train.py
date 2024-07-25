import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import logging
import os
from LTSM_model import HandwritingLSTM
from dataloader import HandwritingSequenceDataset
from torch.nn.utils.rnn import pad_sequence

# Set up logging
logging.basicConfig(level=logging.INFO, filename='training.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Directory to save models
model_dir = 'saved_models'
os.makedirs(model_dir, exist_ok=True)


# Custom collate function to pad sequences
def collate_fn(batch):
    inputs = [item[0] for item in batch]
    labels = [item[1] for item in batch]
    inputs_padded = pad_sequence(inputs, batch_first=True)
    labels_padded = pad_sequence(labels, batch_first=True)
    return inputs_padded, labels_padded


# Load the datasets
train_dataset = HandwritingSequenceDataset('train_data.pt')
val_dataset = HandwritingSequenceDataset('val_data.pt')

# Create the dataloaders with a larger batch size
batch_size = 32
train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_fn)
val_dataloader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, collate_fn=collate_fn)


# Training function
def train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs=100):
    for epoch in range(num_epochs):
        model.train()
        train_loss = 0.0
        for inputs, labels in train_loader:
            outputs = model(inputs)

            # Create a mask to ignore padding in the loss calculation
            mask = labels != 0
            outputs = outputs.squeeze(-1)  # Remove the extra dimension
            outputs = outputs[mask]
            labels = labels[mask]

            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * mask.sum().item()

        train_loss /= len(train_loader.dataset)

        val_loss = 0.0
        model.eval()
        with torch.no_grad():
            for inputs, labels in val_loader:
                outputs = model(inputs)

                # Create a mask to ignore padding in the loss calculation
                mask = labels != 0
                outputs = outputs.squeeze(-1)  # Remove the extra dimension
                outputs = outputs[mask]
                labels = labels[mask]

                loss = criterion(outputs, labels)
                val_loss += loss.item() * mask.sum().item()

        val_loss /= len(val_loader.dataset)

        # Log the training and validation loss
        logger.info(f'Epoch [{epoch + 1}/{num_epochs}], Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}')
        print(f'Epoch [{epoch + 1}/{num_epochs}], Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}')

        # Save the model
        model_save_path = os.path.join(model_dir, f'model_epoch_{epoch + 1}.pth')
        torch.save({
            'epoch': epoch + 1,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'train_loss': train_loss,
            'val_loss': val_loss,
        }, model_save_path)

    return model


# Initialize the model, criterion, and optimizer
input_dim = 3  # (x_coordinate, y_coordinate, end_of_stroke_boolean)
hidden_dim = 50
output_dim = 1  # pen_pressure
num_layers = 2
model = HandwritingLSTM(input_dim, hidden_dim, output_dim, num_layers)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Train the model
trained_model = train_model(model, train_dataloader, val_dataloader, criterion, optimizer, num_epochs=100)
