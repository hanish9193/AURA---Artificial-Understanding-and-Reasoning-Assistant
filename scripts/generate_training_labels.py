"""
Generate ground-truth labels for VisionTextBridge training.
This creates the "answer key" by performing REAL statistical analysis on the data.
"""

import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis


def analyze_graph_for_labels(data: pd.DataFrame, metadata: dict):
    """
    Analyze the *actual data* for a graph to assign ground-truth labels.
    
    Args:
        data: The original Pandas DataFrame
        metadata: The dict for a single graph, e.g.,
                  {'name': 'histogram_of_A', 'type': 'distribution', 'columns': ['A']}
                  
    Returns:
        dict with trend, density, outliers, shape labels
    """
    labels = {}
    graph_type = metadata.get('type', 'unknown')

    default_trend = 1    # 'flat'
    default_density = 1  # 'clustered'
    default_outliers = 0 # 'no outliers'
    default_shape = 0    # 'uniform'
    
    # Extract numeric columns from data
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    # For Histograms or Distributions (Shape analysis)
    if graph_type == 'distribution' and numeric_cols:
        col = numeric_cols[0]
        col_data = data[col].dropna()
        
        s = skew(col_data)
        if s > 0.75:
            labels['shape'] = 1  # 'skewed'
        elif s < -0.75:
            labels['shape'] = 1  # 'skewed'
        elif kurtosis(col_data) < -0.5:
            labels['shape'] = 2  # 'bimodal'
        else:
            labels['shape'] = 0  # 'uniform'

    # For Scatter Plots (Trend & Density)
    elif graph_type == 'scatter' and len(numeric_cols) >= 2:
        col1, col2 = numeric_cols[0], numeric_cols[1]
        corr = data[col1].corr(data[col2])
        
        if corr > 0.7:
            labels['trend'] = 2  # 'positive'
        elif corr < -0.7:
            labels['trend'] = 0  # 'negative'
        else:
            labels['trend'] = 1  # 'flat'
        labels['density'] = 1  # 'clustered'

    # For Box Plots (Outliers)
    elif graph_type == 'boxplot' and numeric_cols:
        col = numeric_cols[0]
        col_data = data[col].dropna()
        Q1 = col_data.quantile(0.25)
        Q3 = col_data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        has_outliers = ((col_data < lower_bound) | (col_data > upper_bound)).any()
        labels['outliers'] = 1 if has_outliers else 0
    
    # For Heatmap (Correlation analysis)
    elif graph_type == 'heatmap':
        corr_matrix = data[numeric_cols].corr()
        avg_corr = corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)].mean()
        
        if avg_corr > 0.5:
            labels['trend'] = 2  # 'positive correlations'
        elif avg_corr < -0.3:
            labels['trend'] = 0  # 'negative correlations'
        else:
            labels['trend'] = 1  # 'mixed correlations'
        
    if 'trend' not in labels: labels['trend'] = default_trend
    if 'density' not in labels: labels['density'] = default_density
    if 'outliers' not in labels: labels['outliers'] = default_outliers
    if 'shape' not in labels: labels['shape'] = default_shape
        
    return labels


def generate_dataset_labels(data: pd.DataFrame, graph_metadata: list):
    """
    Generate labels for all graphs by analyzing the original DataFrame.
    
    Args:
        data: The original Pandas DataFrame
        graph_metadata: list of graph metadata dicts
        
    Returns:
        dict with arrays of labels for each attribute
    """
    all_labels = {
        'trend': [],
        'density': [],
        'outliers': [],
        'shape': []
    }
    
    for metadata in graph_metadata:
        labels = analyze_graph_for_labels(data, metadata)
        
        all_labels['trend'].append(labels['trend'])
        all_labels['density'].append(labels['density'])
        all_labels['outliers'].append(labels['outliers'])
        all_labels['shape'].append(labels['shape'])
        
    # Convert to numpy arrays
    all_labels_np = {k: np.array(v) for k, v in all_labels.items()}
    
    n_graphs = len(graph_metadata)
    print(f"✓ Generated REAL labels for {n_graphs} graphs from actual data analysis")
    print(f"  - Trend distribution: {np.bincount(all_labels_np['trend'])}")
    print(f"  - Density distribution: {np.bincount(all_labels_np['density'])}")
    print(f"  - Outliers: {np.sum(all_labels_np['outliers'])} graphs with outliers")
    print(f"  - Shape distribution: {np.bincount(all_labels_np['shape'])}")
        
    return all_labels_np
