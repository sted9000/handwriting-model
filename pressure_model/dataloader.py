import torch
from torch.utils.data import Dataset


# Custom Dataset class
class HandwritingSequenceDataset(Dataset):
    def __init__(self, data_path):
        self.X, self.y = torch.load(data_path)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]