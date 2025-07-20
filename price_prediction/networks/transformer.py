import torch
import torch.nn as nn


class Transformer(nn.Module):
    def __init__(self, input_dim, model_dim, num_heads, num_layers, dropout=0.1):
        super().__init__()
        self.input_linear = nn.Linear(input_dim, model_dim)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=model_dim, nhead=num_heads, dropout=dropout
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.output_linear = nn.Linear(model_dim, 1)  # Predict next price

    def forward(self, x):
        # x: (batch, seq_len, input_dim)
        x = self.input_linear(x)
        x = x.permute(1, 0, 2)  # Transformer expects (seq_len, batch, model_dim)
        x = self.transformer(x)
        x = x[-1]  # Use the final token's representation
        return self.output_linear(x)
