"""
Generate 15 different graphs for data visualization
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from io import BytesIO
import base64


class GraphGenerator:
    """Generate 15 diverse graphs from CSV data"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = data.select_dtypes(include=['object']).columns.tolist()
        sns.set_style("whitegrid")
    
    def create_all_graphs(self) -> tuple:
        """Create all 15 graphs"""
        graphs = []
        metadata = []
        
        # 1. Correlation Heatmap
        graphs.append(self._correlation_heatmap())
        metadata.append({"type": "heatmap", "name": "Correlation Matrix"})
        
        # 2-4. Distribution plots (first 3 numeric columns)
        for col in self.numeric_cols[:3]:
            graphs.append(self._distribution_plot(col))
            metadata.append({"type": "distribution", "name": f"Distribution: {col}"})
        
        # 5-7. Scatter plots (pairs of numeric columns)
        for i in range(min(3, len(self.numeric_cols)-1)):
            graphs.append(self._scatter_plot(self.numeric_cols[i], self.numeric_cols[i+1]))
            metadata.append({"type": "scatter", "name": f"Relationship: {self.numeric_cols[i]} vs {self.numeric_cols[i+1]}"})
        
        # 8-10. Box plots (first 3 numeric columns)
        for col in self.numeric_cols[:3]:
            graphs.append(self._box_plot(col))
            metadata.append({"type": "boxplot", "name": f"Outliers: {col}"})
        
        # 11-13. Category counts (first 3 categorical columns)
        for col in self.categorical_cols[:3]:
            graphs.append(self._category_bar_plot(col))
            metadata.append({"type": "bar", "name": f"Categories: {col}"})
        
        # 14. Data quality
        graphs.append(self._missing_data_plot())
        metadata.append({"type": "missing", "name": "Data Quality"})
        
        # 15. Feature importance via variance
        graphs.append(self._variance_plot())
        metadata.append({"type": "variance", "name": "Feature Importance"})
        
        return graphs, metadata
    
    def _correlation_heatmap(self):
        """Correlation heatmap"""
        fig, ax = plt.subplots(figsize=(10, 8))
        corr = self.data[self.numeric_cols].corr()
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=ax, cbar_kws={'label': 'Correlation'})
        ax.set_title("Correlation Matrix", fontsize=14, fontweight='bold')
        return self._fig_to_bytes(fig)
    
    def _distribution_plot(self, col):
        """Distribution histogram"""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(self.data[col].dropna(), bins=30, color='steelblue', edgecolor='black', alpha=0.7)
        ax.set_title(f"Distribution: {col}", fontsize=12, fontweight='bold')
        ax.set_xlabel(col)
        ax.set_ylabel("Frequency")
        return self._fig_to_bytes(fig)
    
    def _scatter_plot(self, col1, col2):
        """Scatter plot"""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(self.data[col1], self.data[col2], alpha=0.6, s=50, color='steelblue')
        ax.set_title(f"{col1} vs {col2}", fontsize=12, fontweight='bold')
        ax.set_xlabel(col1)
        ax.set_ylabel(col2)
        return self._fig_to_bytes(fig)
    
    def _box_plot(self, col):
        """Box plot for outlier detection"""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.boxplot(self.data[col].dropna())
        ax.set_title(f"Outlier Detection: {col}", fontsize=12, fontweight='bold')
        ax.set_ylabel(col)
        return self._fig_to_bytes(fig)
    
    def _category_bar_plot(self, col):
        """Bar plot for categories"""
        fig, ax = plt.subplots(figsize=(10, 6))
        counts = self.data[col].value_counts()
        ax.bar(range(len(counts)), counts.values, color='steelblue')
        ax.set_xticks(range(len(counts)))
        ax.set_xticklabels(counts.index, rotation=45, ha='right')
        ax.set_title(f"Categories: {col}", fontsize=12, fontweight='bold')
        ax.set_ylabel("Count")
        return self._fig_to_bytes(fig)
    
    def _missing_data_plot(self):
        """Missing data visualization"""
        fig, ax = plt.subplots(figsize=(10, 6))
        missing = (self.data.isnull().sum() / len(self.data)) * 100
        missing = missing[missing > 0]
        if len(missing) > 0:
            ax.barh(missing.index, missing.values, color='coral')
            ax.set_xlabel("Missing %")
            ax.set_title("Data Quality Issues", fontsize=12, fontweight='bold')
        else:
            ax.text(0.5, 0.5, "No Missing Data", ha='center', va='center', fontsize=14)
        return self._fig_to_bytes(fig)
    
    def _variance_plot(self):
        """Feature importance by variance"""
        fig, ax = plt.subplots(figsize=(10, 6))
        variance = self.data[self.numeric_cols].var()
        variance = variance / variance.max()  # Normalize
        ax.barh(variance.index, variance.values, color='seagreen')
        ax.set_xlabel("Normalized Variance")
        ax.set_title("Feature Importance", fontsize=12, fontweight='bold')
        return self._fig_to_bytes(fig)
    
    @staticmethod
    def _fig_to_bytes(fig):
        """Convert matplotlib figure to bytes"""
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)
        return buf.getvalue()
