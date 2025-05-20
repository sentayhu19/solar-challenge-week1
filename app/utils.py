import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict
import numpy as np

def load_data(file_paths: Dict[str, str]) -> pd.DataFrame:
    """Load and combine data from multiple CSV files."""
    dfs = []
    for country, path in file_paths.items():
        try:
            df = pd.read_csv(path)
            df['Country'] = country
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
            dfs.append(df)
        except FileNotFoundError:
            print(f"Warning: {path} not found. Skipping...")
    
    if not dfs:
        raise FileNotFoundError("No data files could be loaded")
    
    return pd.concat(dfs, ignore_index=True)

def create_metric_boxplot(data: pd.DataFrame, metric: str) -> go.Figure:
    """Create an interactive boxplot for the specified metric."""
    fig = px.box(data, x='Country', y=metric,
                 title=f'{metric} Distribution by Country',
                 color='Country',
                 points='all',  
                 notched=True) 
    
    fig.update_layout(
        xaxis_title='Country',
        yaxis_title=f'{metric} (W/m²)',
        showlegend=True,
        template='plotly_white',
        height=500
    )
    return fig

def calculate_summary_stats(data: pd.DataFrame, metrics: List[str]) -> pd.DataFrame:
    """Calculate summary statistics for each metric by country."""
    summary_stats = []
    for metric in metrics:
        stats = data.groupby('Country')[metric].agg([
            ('mean', 'mean'),
            ('median', 'median'),
            ('std', 'std'),
            ('min', 'min'),
            ('max', 'max'),
            ('count', 'count')
        ])
        stats['metric'] = metric
        summary_stats.append(stats)
    return pd.concat(summary_stats).round(2)

def create_ghi_ranking(data: pd.DataFrame) -> go.Figure:
    """Create an interactive bar chart ranking countries by average GHI."""
    avg_ghi = data.groupby('Country')['GHI'].agg(['mean', 'std']).reset_index()
    avg_ghi = avg_ghi.sort_values('mean', ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=avg_ghi['mean'],
        y=avg_ghi['Country'],
        orientation='h',
        error_x=dict(type='data', array=avg_ghi['std']),
        marker_color='#2ecc71',
        name='Average GHI'
    ))
    
    fig.update_layout(
        title='Average GHI by Country (with Standard Deviation)',
        xaxis_title='GHI (W/m²)',
        yaxis_title='Country',
        template='plotly_white',
        height=400,
        showlegend=True
    )
    
    return fig

def create_correlation_heatmap(data: pd.DataFrame, metrics: List[str]) -> go.Figure:
    """Create a correlation heatmap for the specified metrics."""
    corr_matrix = data[metrics].corr()
    
    fig = px.imshow(
        corr_matrix,
        labels=dict(color="Correlation"),
        color_continuous_scale="RdBu",
        aspect="auto"
    )
    
    fig.update_layout(
        title='Correlation between Metrics',
        template='plotly_white',
        height=500,
        width=500
    )
    
    for i in range(len(corr_matrix.index)):
        for j in range(len(corr_matrix.columns)):
            fig.add_annotation(
                text=f"{corr_matrix.iloc[i, j]:.2f}",
                x=j,
                y=i,
                showarrow=False,
                font=dict(color='black' if abs(corr_matrix.iloc[i, j]) < 0.7 else 'white')
            )
    
    return fig
    avg_ghi = data.groupby('Country')['GHI'].mean().sort_values(ascending=False)
    fig = px.bar(x=avg_ghi.index, y=avg_ghi.values,
                 title='Average GHI by Country',
                 labels={'x': 'Country', 'y': 'GHI (W/m²)'})
    return fig
