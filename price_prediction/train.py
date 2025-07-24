import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, TensorDataset
import pickle


def train(model):

    # ---- Parameters ----
    WINDOW_SIZE = 7
    BATCH_SIZE = 64
    EPOCHS = 50
    LR = 1e-5
    MODEL_DIM = 64
    HEADS = 4
    LAYERS = 2

    # ---- Load & preprocess data ----
    training_data = pd.read_csv('data/training.csv', index_col=0)
    features = []
    labels = []

    for i in range(len(training_data) - WINDOW_SIZE):
        features.append(training_data.iloc[i:i + WINDOW_SIZE])
        labels.append(training_data.iloc[i + WINDOW_SIZE].Close)

    features = torch.tensor(np.array(features))
    labels = torch.tensor(np.array(labels))

    assert torch.isfinite(features).all(), "Input contains NaNs or infinite values"

    dataset = TensorDataset(features, labels)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    optimizer = torch.optim.Adam(model.parameters(), lr=LR)
    loss_fn = nn.MSELoss()

    # ---- Real-time plotting ----
    losses = []

    # ---- Training loop ----
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 5))

    train_losses = []

    best_train_loss = float('inf')
    epochs_no_improve = 0
    early_stop_patience = 5
    max_epochs = 2000

    for epoch in range(max_epochs):
        model.train()
        train_loss = 0
        for xb, yb in loader:
            xb, yb = xb.float(), yb.float()
            pred = model(xb)
            loss = loss_fn(pred.squeeze(-1), yb)
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            train_loss += loss.item()
        train_loss /= len(loader)

        train_losses.append(train_loss)

        # Plot update
        ax.clear()
        ax.plot(train_losses, label="Train Loss")
        ax.set_title("Loss Over Epochs")
        ax.set_xlabel("Epoch")
        ax.set_ylabel("Loss")
        ax.legend()
        plt.tight_layout()
        plt.pause(0.1)  # allows plot to update

        print(f"Epoch {epoch + 1} - Train Loss: {train_loss:.6f}")

        # Early stopping
        if train_loss < best_train_loss:
            best_train_loss = train_loss
            epochs_no_improve = 0
            best_model_state = model.state_dict()
        else:
            epochs_no_improve += 1
            if epochs_no_improve >= early_stop_patience and epoch > 50:
                print(f"Early stopping at epoch {epoch + 1}")
                break

    # After training
    model.load_state_dict(best_model_state)
    plt.ioff()
    plt.draw()
    plt.pause(5)   # keeps the plot open for 5 seconds
    plt.close()

    torch.save(model.state_dict(), 'artifacts/model.save')

    with open('price_prediction/results/training_loss.pkl', 'wb') as fp:
        pickle.dump(train_loss, fp)
