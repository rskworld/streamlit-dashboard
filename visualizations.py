"""
Visualization Functions for Streamlit Analytics Dashboard
=========================================================

Custom visualization functions using Plotly for interactive charts.

Author: RSK World
Website: https://rskworld.in
Email: help@rskworld.in
Phone: +91 93305 39277
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any


def create_line_chart(df: pd.DataFrame, 
                     x_col: str, 
                     y_col: str,
                     title: str = "Line Chart",
                     color_col: Optional[str] = None) -> go.Figure:
    """
    Create an interactive line chart.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    
    Args:
        df: DataFrame with data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        title: Chart title
        color_col: Optional column for color grouping
        
    Returns:
        Plotly figure object
    """
    if color_col:
        fig = px.line(
            df, 
            x=x_col, 
            y=y_col, 
            color=color_col,
            title=title,
            labels={x_col: x_col.replace('_', ' ').title(), 
                   y_col: y_col.replace('_', ' ').title()}
        )
    else:
        fig = px.line(
            df, 
            x=x_col, 
            y=y_col, 
            title=title,
            labels={x_col: x_col.replace('_', ' ').title(), 
                   y_col: y_col.replace('_', ' ').title()}
        )
    
    fig.update_layout(
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    return fig


def create_bar_chart(df: pd.DataFrame,
                    x_col: str,
                    y_col: str,
                    title: str = "Bar Chart",
                    orientation: str = 'v',
                    color_col: Optional[str] = None) -> go.Figure:
    """
    Create an interactive bar chart.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    
    Args:
        df: DataFrame with data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        title: Chart title
        orientation: 'v' for vertical, 'h' for horizontal
        color_col: Optional column for color grouping
        
    Returns:
        Plotly figure object
    """
    if color_col:
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            color=color_col,
            title=title,
            orientation=orientation,
            labels={x_col: x_col.replace('_', ' ').title(), 
                   y_col: y_col.replace('_', ' ').title()}
        )
    else:
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            title=title,
            orientation=orientation,
            labels={x_col: x_col.replace('_', ' ').title(), 
                   y_col: y_col.replace('_', ' ').title()}
        )
    
    fig.update_layout(
        template='plotly_white',
        height=500
    )
    
    return fig


def create_scatter_plot(df: pd.DataFrame,
                       x_col: str,
                       y_col: str,
                       title: str = "Scatter Plot",
                       size_col: Optional[str] = None,
                       color_col: Optional[str] = None) -> go.Figure:
    """
    Create an interactive scatter plot.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    
    Args:
        df: DataFrame with data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        title: Chart title
        size_col: Optional column for point sizes
        color_col: Optional column for color grouping
        
    Returns:
        Plotly figure object
    """
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        size=size_col,
        color=color_col,
        title=title,
        hover_data=df.columns.tolist(),
        labels={x_col: x_col.replace('_', ' ').title(), 
               y_col: y_col.replace('_', ' ').title()}
    )
    
    fig.update_layout(
        template='plotly_white',
        height=500
    )
    
    return fig


def create_pie_chart(df: pd.DataFrame,
                    value_col: str,
                    name_col: str,
                    title: str = "Pie Chart") -> go.Figure:
    """
    Create an interactive pie chart.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    
    Args:
        df: DataFrame with data
        value_col: Column name for values
        name_col: Column name for labels
        title: Chart title
        
    Returns:
        Plotly figure object
    """
    fig = px.pie(
        df,
        values=value_col,
        names=name_col,
        title=title
    )
    
    fig.update_layout(
        template='plotly_white',
        height=500
    )
    
    return fig


def create_heatmap(df: pd.DataFrame,
                  title: str = "Correlation Heatmap",
                  columns: Optional[List[str]] = None) -> go.Figure:
    """
    Create a correlation heatmap for numeric columns.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    
    Args:
        df: DataFrame with numeric data
        title: Chart title
        columns: Optional list of columns to include
        
    Returns:
        Plotly figure object
    """
    if columns:
        numeric_df = df[columns].select_dtypes(include=[np.number])
    else:
        numeric_df = df.select_dtypes(include=[np.number])
    
    if numeric_df.empty:
        raise ValueError("No numeric columns found for heatmap")
    
    corr_matrix = numeric_df.corr()
    
    fig = px.imshow(
        corr_matrix,
        title=title,
        color_continuous_scale='RdBu',
        aspect="auto",
        labels=dict(color="Correlation")
    )
    
    fig.update_layout(
        template='plotly_white',
        height=600
    )
    
    return fig


def create_area_chart(df: pd.DataFrame,
                     x_col: str,
                     y_col: str,
                     title: str = "Area Chart",
                     color_col: Optional[str] = None) -> go.Figure:
    """
    Create an interactive area chart.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    
    Args:
        df: DataFrame with data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        title: Chart title
        color_col: Optional column for color grouping
        
    Returns:
        Plotly figure object
    """
    if color_col:
        fig = px.area(
            df,
            x=x_col,
            y=y_col,
            color=color_col,
            title=title,
            labels={x_col: x_col.replace('_', ' ').title(), 
                   y_col: y_col.replace('_', ' ').title()}
        )
    else:
        fig = px.area(
            df,
            x=x_col,
            y=y_col,
            title=title,
            labels={x_col: x_col.replace('_', ' ').title(), 
                   y_col: y_col.replace('_', ' ').title()}
        )
    
    fig.update_layout(
        template='plotly_white',
        height=500
    )
    
    return fig


def create_dashboard_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Create a summary dictionary for dashboard display.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    
    Args:
        df: DataFrame to summarize
        
    Returns:
        Dictionary with summary statistics
    """
    summary = {
        'total_records': len(df),
        'total_columns': len(df.columns),
        'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
        'categorical_columns': df.select_dtypes(include=['object', 'category']).columns.tolist(),
        'date_columns': [],
        'missing_values': df.isnull().sum().to_dict(),
        'duplicate_rows': df.duplicated().sum()
    }
    
    # Detect date columns
    for col in df.columns:
        if 'date' in col.lower() or 'time' in col.lower():
            summary['date_columns'].append(col)
    
    return summary

