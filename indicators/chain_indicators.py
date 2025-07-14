import pandas as pd
import numpy as np

# Function to calculate Hash Rate


def calculate_hash_rate(df, block_time_col='block_time', difficulty_col='difficulty'):
    """
    Hash Rate = Difficulty / Block Time
    """
    df['hash_rate'] = df[difficulty_col] / df[block_time_col]
    return df

# Function to calculate Active Addresses


def calculate_active_addresses(df, unique_senders_col='unique_senders', unique_receivers_col='unique_receivers'):
    """
    Active Addresses = Unique Senders + Unique Receivers
    """
    df['active_addresses'] = df[unique_senders_col] + df[unique_receivers_col]
    return df

# Function to calculate Transaction Volume


def calculate_transaction_volume(df, transaction_count_col='transaction_count', average_transaction_value_col='average_transaction_value'):
    """
    Transaction Volume = Transaction Count * Average Transaction Value
    """
    df['transaction_volume'] = df[transaction_count_col] * df[average_transaction_value_col]
    return df

# Function to calculate Network Value to Transactions (NVT) Ratio


def calculate_nvt_ratio(df, market_cap_col='market_cap', transaction_volume_col='transaction_volume'):
    """
    NVT Ratio = Market Cap / Transaction Volume
    """
    df['nvt_ratio'] = df[market_cap_col] / df[transaction_volume_col]
    return df

# Function to calculate MVRV (Market Value to Realized Value) Ratio


def calculate_mvrv_ratio(df, market_cap_col='market_cap', realized_cap_col='realized_cap'):
    """
    MVRV Ratio = Market Cap / Realized Cap
    """
    df['mvrv_ratio'] = df[market_cap_col] / df[realized_cap_col]
    return df

# Function to calculate Realized Cap


def calculate_realized_cap(df, coin_age_col='coin_age', price_col='close'):
    """
    Realized Cap = Sum of (Coin Age * Price)
    """
    df['realized_cap'] = df[coin_age_col] * df[price_col]
    return df

# Function to calculate Coin Days Destroyed (CDD)


def calculate_coin_days_destroyed(df, coin_age_col='coin_age', transaction_count_col='transaction_count'):
    """
    Coin Days Destroyed = Coin Age * Transaction Count
    """
    df['coin_days_destroyed'] = df[coin_age_col] * df[transaction_count_col]
    return df

# Global function to calculate all on-chain indicators


def calculate_on_chain_indicators(df):
    # Calculate Hash Rate
    df = calculate_hash_rate(df)

    # Calculate Active Addresses
    df = calculate_active_addresses(df)

    # Calculate Transaction Volume
    df = calculate_transaction_volume(df)

    # Calculate NVT Ratio
    df = calculate_nvt_ratio(df)

    # Calculate Realized Cap
    df = calculate_realized_cap(df)

    # Calculate MVRV Ratio
    df = calculate_mvrv_ratio(df)

    # Calculate Coin Days Destroyed
    df = calculate_coin_days_destroyed(df)

    return df
