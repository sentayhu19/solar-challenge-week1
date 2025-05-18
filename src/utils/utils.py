import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

def load_data(file_path):
    """
    Load data from CSV file
    """
    return pd.read_csv(file_path, parse_dates=['Timestamp'])

def missing_values_report(df):
    """
    Generate missing values report
    """
    total = df.isnull().sum().sort_values(ascending=False)
    percent = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)
    report = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    return report[report['Percent'] > 0.05]

def detect_outliers(df, columns, z_threshold=3):
    """
    Detect outliers using Z-score method
    """
    outliers = pd.DataFrame()
    
    for col in columns:
        if col in df.columns:
            z_scores = np.abs(stats.zscore(df[col].dropna()))
            outliers[col] = z_scores > z_threshold
    
    return outliers

def clean_data(df, columns_to_clean, strategy='median'):
    """
    Clean data by imputing missing values
    """
    df_clean = df.copy()
    
    for col in columns_to_clean:
        if col in df.columns:
            if strategy == 'median':
                df_clean[col] = df_clean[col].fillna(df_clean[col].median())
            elif strategy == 'mean':
                df_clean[col] = df_clean[col].fillna(df_clean[col].mean())
            elif strategy == 'mode':
                df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
    
    return df_clean

def plot_time_series(df, columns, title='Time Series Plot'):
    """
    Plot time series data
    """
    plt.figure(figsize=(15, 8))
    
    for col in columns:
        if col in df.columns:
            plt.plot(df['Timestamp'], df[col], label=col)
            
    plt.title(title)
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    return plt

def plot_correlation_heatmap(df, columns):
    """
    Plot correlation heatmap
    """
    plt.figure(figsize=(12, 10))
    corr = df[columns].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm', 
                linewidths=0.5, vmin=-1, vmax=1)
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    
    return plt

def plot_scatter(df, x_col, y_col, title=None):
    """
    Create scatter plot
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(df[x_col], df[y_col], alpha=0.5)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(title if title else f'{x_col} vs {y_col}')
    plt.grid(True)
    
    return plt

def plot_bubble_chart(df, x_col, y_col, size_col, title=None):
    """
    Create bubble chart
    """
    plt.figure(figsize=(12, 8))
    
    # Normalize size column for better visualization
    size = df[size_col].values
    size = (size - size.min()) / (size.max() - size.min()) * 200 + 20
    
    plt.scatter(df[x_col], df[y_col], s=size, alpha=0.5)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(title if title else f'{x_col} vs {y_col} (size={size_col})')
    plt.colorbar(plt.cm.ScalarMappable(), label=size_col)
    plt.grid(True)
    
    return plt

def plot_histogram(df, column, bins=30, title=None):
    """
    Create histogram
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(df[column], bins=bins, kde=True)
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.title(title if title else f'Distribution of {column}')
    plt.grid(True)
    
    return plt

def save_dataframe(df, file_path):
    """
    Save DataFrame to CSV
    """
    # Create directory if it doesn't exist
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")
