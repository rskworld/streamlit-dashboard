"""
Utility Functions for Streamlit Analytics Dashboard
===================================================

Helper functions for data processing, validation, and formatting.

Author: RSK World
Website: https://rskworld.in
Email: help@rskworld.in
Phone: +91 93305 39277
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional, List, Dict, Any


def validate_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validate a pandas DataFrame and return validation results.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    
    Args:
        df: DataFrame to validate
        
    Returns:
        Dictionary with validation results
    """
    validation_results = {
        'is_valid': True,
        'errors': [],
        'warnings': [],
        'info': {}
    }
    
    if df is None:
        validation_results['is_valid'] = False
        validation_results['errors'].append("DataFrame is None")
        return validation_results
    
    if df.empty:
        validation_results['is_valid'] = False
        validation_results['errors'].append("DataFrame is empty")
        return validation_results
    
    # Check for missing values
    missing_values = df.isnull().sum()
    if missing_values.sum() > 0:
        validation_results['warnings'].append(
            f"Found {missing_values.sum()} missing values across columns"
        )
        validation_results['info']['missing_values'] = missing_values.to_dict()
    
    # Check for duplicate rows
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        validation_results['warnings'].append(
            f"Found {duplicate_count} duplicate rows"
        )
        validation_results['info']['duplicate_count'] = duplicate_count
    
    # Basic info
    validation_results['info']['shape'] = df.shape
    validation_results['info']['columns'] = df.columns.tolist()
    validation_results['info']['dtypes'] = df.dtypes.to_dict()
    
    return validation_results


def format_number(value: float, decimals: int = 2) -> str:
    """
    Format a number with commas and specified decimal places.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    
    Args:
        value: Number to format
        decimals: Number of decimal places
        
    Returns:
        Formatted string
    """
    if pd.isna(value) or value is None:
        return "N/A"
    
    return f"{value:,.{decimals}f}"


def format_currency(value: float, currency: str = "$") -> str:
    """
    Format a number as currency.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    
    Args:
        value: Number to format
        currency: Currency symbol
        
    Returns:
        Formatted currency string
    """
    if pd.isna(value) or value is None:
        return "N/A"
    
    return f"{currency}{value:,.2f}"


def detect_date_columns(df: pd.DataFrame) -> List[str]:
    """
    Detect columns that might contain dates.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        List of column names that might be dates
    """
    date_columns = []
    
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in ['date', 'time', 'timestamp', 'day', 'month', 'year']):
            date_columns.append(col)
        elif df[col].dtype == 'object':
            # Try to parse as date
            try:
                pd.to_datetime(df[col].head(10), errors='raise')
                date_columns.append(col)
            except:
                pass
    
    return date_columns


def get_numeric_columns(df: pd.DataFrame) -> List[str]:
    """
    Get list of numeric columns from DataFrame.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        List of numeric column names
    """
    return df.select_dtypes(include=[np.number]).columns.tolist()


def get_categorical_columns(df: pd.DataFrame) -> List[str]:
    """
    Get list of categorical columns from DataFrame.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        List of categorical column names
    """
    return df.select_dtypes(include=['object', 'category']).columns.tolist()


def calculate_statistics(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    """
    Calculate comprehensive statistics for a numeric column.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    
    Args:
        df: DataFrame containing the data
        column: Column name to analyze
        
    Returns:
        Dictionary with statistics
    """
    if column not in df.columns:
        return {'error': f"Column '{column}' not found"}
    
    if not pd.api.types.is_numeric_dtype(df[column]):
        return {'error': f"Column '{column}' is not numeric"}
    
    stats = {
        'count': df[column].count(),
        'mean': df[column].mean(),
        'median': df[column].median(),
        'std': df[column].std(),
        'min': df[column].min(),
        'max': df[column].max(),
        'q25': df[column].quantile(0.25),
        'q75': df[column].quantile(0.75),
        'skewness': df[column].skew(),
        'kurtosis': df[column].kurtosis()
    }
    
    return stats


def clean_dataframe(df: pd.DataFrame, 
                   remove_duplicates: bool = True,
                   fill_missing: Optional[str] = None) -> pd.DataFrame:
    """
    Clean a DataFrame by removing duplicates and handling missing values.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    
    Args:
        df: DataFrame to clean
        remove_duplicates: Whether to remove duplicate rows
        fill_missing: Strategy for filling missing values ('mean', 'median', 'mode', 'drop', None)
        
    Returns:
        Cleaned DataFrame
    """
    cleaned_df = df.copy()
    
    # Remove duplicates
    if remove_duplicates:
        cleaned_df = cleaned_df.drop_duplicates()
    
    # Handle missing values
    if fill_missing:
        numeric_cols = get_numeric_columns(cleaned_df)
        
        if fill_missing == 'mean':
            for col in numeric_cols:
                cleaned_df[col].fillna(cleaned_df[col].mean(), inplace=True)
        elif fill_missing == 'median':
            for col in numeric_cols:
                cleaned_df[col].fillna(cleaned_df[col].median(), inplace=True)
        elif fill_missing == 'mode':
            for col in numeric_cols:
                cleaned_df[col].fillna(cleaned_df[col].mode()[0] if not cleaned_df[col].mode().empty else 0, inplace=True)
        elif fill_missing == 'drop':
            cleaned_df = cleaned_df.dropna()
    
    return cleaned_df

