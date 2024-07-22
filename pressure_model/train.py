import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from pressure_model.LTSM_model import HandwritingLSTM
from pressure_model.dataloader import HandwritingSequenceDataset


# Load the datasets
train_dataset = HandwritingSequenceDataset('train_data.pt')
val_dataset = HandwritingSequenceDataset('val_data.pt')

# Create the dataloaders
train_dataloader = DataLoader(train_dataset, batch_size=1, shuffle=True, collate_fn=lambda x: x)
val_dataloader = DataLoader(val_dataset, batch_size=1, shuffle=False, collate_fn=lambda x: x)


# Training function
def train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs=100):
    model.train()

    for epoch in range(num_epochs):
        train_loss = 0.0
        for sequences in train_loader:
            inputs, labels = sequences[0]
            inputs = inputs.unsqueeze(0)  # Adding a batch dimension
            labels = labels.unsqueeze(0)  # Adding a batch dimension

            outputs = model(inputs)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * inputs.size(0)

        train_loss /= len(train_loader.dataset)

        val_loss = 0.0
        model.eval()
        with torch.no_grad():
            for sequences in val_loader:
                inputs, labels = sequences[0]
                inputs = inputs.unsqueeze(0)  # Adding a batch dimension
                labels = labels.unsqueeze(0)  # Adding a batch dimension

                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item() * inputs.size(0)

        val_loss /= len(val_loader.dataset)

        print(f'Epoch [{epoch + 1}/{num_epochs}], Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}')

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
