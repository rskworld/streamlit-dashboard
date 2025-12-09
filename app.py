"""
Streamlit Analytics Dashboard
=============================

Interactive analytics dashboard built with Streamlit for data exploration, 
visualization, and real-time analysis with user-friendly interface.

Author: RSK World
Website: https://rskworld.in
Email: help@rskworld.in
Phone: +91 93305 39277

This project creates a comprehensive analytics dashboard using Streamlit framework.
It provides interactive widgets, real-time data filtering, multiple visualization types,
and user-friendly interface for data exploration.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import json
import io
from scipy import stats
try:
    from openpyxl import Workbook
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Analytics Dashboard - RSK World",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = None
if 'chart_fig' not in st.session_state:
    st.session_state.chart_fig = None

@st.cache_data
def load_sample_data():
    """
    Generate sample data for demonstration purposes.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    """
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    
    data = {
        'Date': dates,
        'Sales': np.random.normal(1000, 200, len(dates)),
        'Revenue': np.random.normal(50000, 10000, len(dates)),
        'Customers': np.random.randint(50, 500, len(dates)),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], len(dates)),
        'Product': np.random.choice(['Product A', 'Product B', 'Product C', 'Product D'], len(dates)),
        'Category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books'], len(dates))
    }
    
    df = pd.DataFrame(data)
    df['Sales'] = np.abs(df['Sales'])
    df['Revenue'] = np.abs(df['Revenue'])
    return df

def load_data_from_file(uploaded_file):
    """
    Load data from uploaded CSV file.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    """
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

def apply_filters(df, date_range, region_filter, product_filter, category_filter):
    """
    Apply filters to the dataset.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    """
    filtered_df = df.copy()
    
    # Date filter
    if date_range and len(date_range) == 2:
        try:
            start_date, end_date = date_range
            if 'Date' in filtered_df.columns:
                filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], errors='coerce')
                filtered_df = filtered_df[
                    (filtered_df['Date'] >= pd.Timestamp(start_date)) & 
                    (filtered_df['Date'] <= pd.Timestamp(end_date))
                ]
        except (ValueError, TypeError) as e:
            st.warning(f"Date filter error: {str(e)}")
    
    # Region filter
    if region_filter and 'Region' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Region'].isin(region_filter)]
    
    # Product filter
    if product_filter and 'Product' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Product'].isin(product_filter)]
    
    # Category filter
    if category_filter and 'Category' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Category'].isin(category_filter)]
    
    return filtered_df

def get_date_presets():
    """
    Get date range presets for quick selection.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    """
    today = datetime.now().date()
    return {
        "Last 7 Days": (today - timedelta(days=7), today),
        "Last 30 Days": (today - timedelta(days=30), today),
        "Last 90 Days": (today - timedelta(days=90), today),
        "Last 6 Months": (today - timedelta(days=180), today),
        "Last Year": (today - timedelta(days=365), today),
        "This Month": (today.replace(day=1), today),
        "This Year": (today.replace(month=1, day=1), today),
    }

def calculate_data_quality(df):
    """
    Calculate data quality metrics.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    """
    quality_metrics = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_values": df.isnull().sum().sum(),
        "missing_percentage": (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100,
        "duplicate_rows": df.duplicated().sum(),
        "duplicate_percentage": (df.duplicated().sum() / len(df)) * 100,
        "numeric_columns": len(df.select_dtypes(include=[np.number]).columns),
        "categorical_columns": len(df.select_dtypes(include=['object', 'category']).columns),
    }
    return quality_metrics

def calculate_advanced_stats(df, column):
    """
    Calculate advanced statistical measures.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    """
    if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
        return None
    
    data = df[column].dropna()
    if len(data) == 0:
        return None
    
    stats_dict = {
        "Mean": data.mean(),
        "Median": data.median(),
        "Mode": data.mode()[0] if not data.mode().empty else None,
        "Std Dev": data.std(),
        "Variance": data.var(),
        "Min": data.min(),
        "Max": data.max(),
        "Range": data.max() - data.min(),
        "Q1 (25%)": data.quantile(0.25),
        "Q3 (75%)": data.quantile(0.75),
        "IQR": data.quantile(0.75) - data.quantile(0.25),
        "Skewness": data.skew(),
        "Kurtosis": data.kurtosis(),
        "Coefficient of Variation": (data.std() / data.mean()) * 100 if data.mean() != 0 else None,
    }
    
    # Outliers using IQR method
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = data[(data < lower_bound) | (data > upper_bound)]
    stats_dict["Outliers Count"] = len(outliers)
    stats_dict["Outliers Percentage"] = (len(outliers) / len(data)) * 100 if len(data) > 0 else 0
    
    return stats_dict

def export_to_excel(df, filename):
    """
    Export DataFrame to Excel format.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    """
    if not OPENPYXL_AVAILABLE:
        return None
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    output.seek(0)
    return output.getvalue()

def export_to_json(df):
    """
    Export DataFrame to JSON format.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    """
    return df.to_json(orient='records', indent=2)

def main():
    """
    Main function to run the Streamlit dashboard.
    
    Author: RSK World
    Website: https://rskworld.in
    Email: help@rskworld.in
    Phone: +91 93305 39277
    """
    # Header
    st.markdown('<h1 class="main-header">📊 Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("⚙️ Dashboard Controls")
    st.sidebar.markdown("**Author:** RSK World")
    st.sidebar.markdown("**Website:** [rskworld.in](https://rskworld.in)")
    st.sidebar.markdown("**Email:** help@rskworld.in")
    st.sidebar.markdown("---")
    
    # Data source selection
    data_source = st.sidebar.radio(
        "Select Data Source",
        ["Sample Data", "Upload CSV File"]
    )
    
    # Load data
    if data_source == "Sample Data":
        df = load_sample_data()
        st.sidebar.success("✅ Using sample data")
    else:
        uploaded_file = st.sidebar.file_uploader(
            "Upload CSV File",
            type=['csv'],
            help="Upload your CSV file for analysis"
        )
        if uploaded_file is not None:
            df = load_data_from_file(uploaded_file)
            if df is not None:
                st.sidebar.success("✅ File loaded successfully")
        else:
            st.info("👆 Please upload a CSV file to get started")
            st.stop()
    
    if df is None or df.empty:
        st.error("No data available. Please check your data source.")
        st.stop()
    
    st.session_state.data = df
    
    # Sidebar filters
    st.sidebar.markdown("### 🔍 Filters")
    
    # Date range filter with presets
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        min_date = df['Date'].min().date() if not df['Date'].isna().all() else datetime.now().date()
        max_date = df['Date'].max().date() if not df['Date'].isna().all() else datetime.now().date()
        
        # Date preset selector
        date_preset = st.sidebar.selectbox(
            "Quick Date Presets",
            ["Custom", "Last 7 Days", "Last 30 Days", "Last 90 Days", "Last 6 Months", "Last Year", "This Month", "This Year"],
            index=0
        )
        
        if date_preset != "Custom":
            presets = get_date_presets()
            if date_preset in presets:
                preset_start, preset_end = presets[date_preset]
                # Adjust to data range
                preset_start = max(preset_start, min_date)
                preset_end = min(preset_end, max_date)
                date_range = (preset_start, preset_end)
            else:
                date_range = (min_date, max_date)
        else:
            date_range = st.sidebar.date_input(
                "Select Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
    else:
        date_range = None
    
    # Region filter
    if 'Region' in df.columns:
        regions = st.sidebar.multiselect(
            "Select Regions",
            options=sorted(df['Region'].unique()),
            default=sorted(df['Region'].unique())
        )
    else:
        regions = None
    
    # Product filter
    if 'Product' in df.columns:
        products = st.sidebar.multiselect(
            "Select Products",
            options=sorted(df['Product'].unique()),
            default=sorted(df['Product'].unique())
        )
    else:
        products = None
    
    # Category filter
    if 'Category' in df.columns:
        categories = st.sidebar.multiselect(
            "Select Categories",
            options=sorted(df['Category'].unique()),
            default=sorted(df['Category'].unique())
        )
    else:
        categories = None
    
    # Apply filters
    filtered_df = apply_filters(df, date_range, regions, products, categories)
    st.session_state.filtered_data = filtered_df
    
    # Main content area
    col1, col2, col3, col4 = st.columns(4)
    
    # Key metrics
    with col1:
        if 'Sales' in filtered_df.columns:
            total_sales = filtered_df['Sales'].sum()
            st.metric("Total Sales", f"${total_sales:,.2f}")
        else:
            st.metric("Total Records", len(filtered_df))
    
    with col2:
        if 'Revenue' in filtered_df.columns:
            total_revenue = filtered_df['Revenue'].sum()
            st.metric("Total Revenue", f"${total_revenue:,.2f}")
        else:
            st.metric("Avg Records", f"{len(filtered_df):,}")
    
    with col3:
        if 'Customers' in filtered_df.columns:
            total_customers = filtered_df['Customers'].sum()
            st.metric("Total Customers", f"{total_customers:,}")
        else:
            numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                avg_value = filtered_df[numeric_cols[0]].mean()
                st.metric("Average", f"{avg_value:,.2f}")
    
    with col4:
        st.metric("Data Points", f"{len(filtered_df):,}")
    
    # Data Quality Metrics
    st.markdown("---")
    st.subheader("📊 Data Quality Metrics")
    quality_metrics = calculate_data_quality(filtered_df)
    
    qcol1, qcol2, qcol3, qcol4, qcol5 = st.columns(5)
    with qcol1:
        st.metric("Total Rows", f"{quality_metrics['total_rows']:,}")
    with qcol2:
        st.metric("Total Columns", f"{quality_metrics['total_columns']:,}")
    with qcol3:
        st.metric("Missing Values", f"{quality_metrics['missing_values']:,}", 
                 delta=f"{quality_metrics['missing_percentage']:.2f}%")
    with qcol4:
        st.metric("Duplicate Rows", f"{quality_metrics['duplicate_rows']:,}",
                 delta=f"{quality_metrics['duplicate_percentage']:.2f}%")
    with qcol5:
        st.metric("Numeric Columns", f"{quality_metrics['numeric_columns']:,}")
    
    st.markdown("---")
    
    # Visualization section
    st.header("📈 Visualizations")
    
    # Chart type selection with more options
    chart_type = st.selectbox(
        "Select Chart Type",
        ["Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart", "Area Chart", "Heatmap", 
         "Box Plot", "Histogram", "Violin Plot", "3D Scatter"]
    )
    
    # Create visualizations based on available columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"{chart_type} - Overview")
        
        if chart_type == "Line Chart":
            if 'Date' in filtered_df.columns and 'Sales' in filtered_df.columns:
                fig = px.line(
                    filtered_df,
                    x='Date',
                    y='Sales',
                    title='Sales Over Time',
                    labels={'Sales': 'Sales ($)', 'Date': 'Date'}
                )
                st.session_state.chart_fig = fig
                st.plotly_chart(fig, use_container_width=True)
            elif 'Date' in filtered_df.columns:
                numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    fig = px.line(
                        filtered_df,
                        x='Date',
                        y=numeric_cols[0],
                        title=f'{numeric_cols[0]} Over Time'
                    )
                    st.session_state.chart_fig = fig
                    st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Bar Chart":
            if 'Region' in filtered_df.columns and 'Sales' in filtered_df.columns:
                region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
                fig = px.bar(
                    region_sales,
                    x='Region',
                    y='Sales',
                    title='Sales by Region',
                    color='Region'
                )
                st.session_state.chart_fig = fig
                st.plotly_chart(fig, use_container_width=True)
            elif 'Region' in filtered_df.columns:
                region_counts = filtered_df['Region'].value_counts().reset_index()
                region_counts.columns = ['Region', 'Count']
                fig = px.bar(
                    region_counts,
                    x='Region',
                    y='Count',
                    title='Records by Region',
                    color='Region'
                )
                st.session_state.chart_fig = fig
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Scatter Plot":
            numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) >= 2:
                fig = px.scatter(
                    filtered_df,
                    x=numeric_cols[0],
                    y=numeric_cols[1],
                    title=f'{numeric_cols[0]} vs {numeric_cols[1]}',
                    hover_data=filtered_df.columns.tolist()
                )
                st.session_state.chart_fig = fig
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Pie Chart":
            if 'Region' in filtered_df.columns:
                region_counts = filtered_df['Region'].value_counts()
                fig = px.pie(
                    values=region_counts.values,
                    names=region_counts.index,
                    title='Distribution by Region'
                )
                st.session_state.chart_fig = fig
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Area Chart":
            if 'Date' in filtered_df.columns and 'Sales' in filtered_df.columns:
                fig = px.area(
                    filtered_df,
                    x='Date',
                    y='Sales',
                    title='Sales Over Time (Area)'
                )
                st.session_state.chart_fig = fig
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Heatmap":
            numeric_df = filtered_df.select_dtypes(include=[np.number])
            if not numeric_df.empty:
                corr = numeric_df.corr()
                fig = px.imshow(
                    corr,
                    title='Correlation Heatmap',
                    color_continuous_scale='RdBu'
                )
                st.session_state.chart_fig = fig
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Box Plot":
            numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) > 0:
                selected_col = st.selectbox("Select Column for Box Plot", numeric_cols, key="box_col")
                if 'Region' in filtered_df.columns:
                    fig = px.box(filtered_df, x='Region', y=selected_col, title=f'Box Plot: {selected_col} by Region')
                else:
                    fig = px.box(filtered_df, y=selected_col, title=f'Box Plot: {selected_col}')
                st.session_state.chart_fig = fig
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Histogram":
            numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) > 0:
                selected_col = st.selectbox("Select Column for Histogram", numeric_cols, key="hist_col")
                bins = st.slider("Number of Bins", 10, 100, 30, key="hist_bins")
                fig = px.histogram(filtered_df, x=selected_col, nbins=bins, title=f'Histogram: {selected_col}')
                st.session_state.chart_fig = fig
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Violin Plot":
            numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) > 0 and 'Region' in filtered_df.columns:
                selected_col = st.selectbox("Select Column for Violin Plot", numeric_cols, key="violin_col")
                fig = px.violin(filtered_df, x='Region', y=selected_col, title=f'Violin Plot: {selected_col} by Region')
                st.session_state.chart_fig = fig
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Violin plot requires a categorical column (e.g., Region) and a numeric column")
        
        elif chart_type == "3D Scatter":
            numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) >= 3:
                col1_3d = st.selectbox("X-axis", numeric_cols, index=0, key="3d_x")
                col2_3d = st.selectbox("Y-axis", numeric_cols, index=1, key="3d_y")
                col3_3d = st.selectbox("Z-axis", numeric_cols, index=2, key="3d_z")
                color_col_3d = st.selectbox("Color by", ['None'] + list(filtered_df.columns), key="3d_color")
                
                if color_col_3d == 'None':
                    fig = px.scatter_3d(filtered_df, x=col1_3d, y=col2_3d, z=col3_3d, 
                                       title=f'3D Scatter: {col1_3d} vs {col2_3d} vs {col3_3d}')
                else:
                    fig = px.scatter_3d(filtered_df, x=col1_3d, y=col2_3d, z=col3_3d, color=color_col_3d,
                                       title=f'3D Scatter: {col1_3d} vs {col2_3d} vs {col3_3d}')
                st.session_state.chart_fig = fig
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("3D Scatter plot requires at least 3 numeric columns")
    
    with col2:
        st.subheader("Additional Analysis")
        
        # Advanced Statistics Tab
        analysis_tab = st.tabs(["Summary Stats", "Advanced Stats", "Trend Analysis"])
        
        with analysis_tab[0]:
            # Summary statistics
            st.markdown("### 📊 Summary Statistics")
            numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                st.dataframe(filtered_df[numeric_cols].describe(), use_container_width=True)
            else:
                st.info("No numeric columns available for statistics")
            
            # Top records
            st.markdown("### 🔝 Top Records")
            if 'Sales' in filtered_df.columns:
                top_sales = filtered_df.nlargest(10, 'Sales')
                display_cols = ['Date', 'Sales', 'Region', 'Product'] if all(c in top_sales.columns for c in ['Date', 'Sales', 'Region', 'Product']) else top_sales.columns[:4]
                st.dataframe(top_sales[display_cols], use_container_width=True)
            else:
                numeric_cols_list = numeric_cols.tolist()
                if len(numeric_cols_list) > 0:
                    top_records = filtered_df.nlargest(10, numeric_cols_list[0])
                    st.dataframe(top_records.head(10), use_container_width=True)
                else:
                    st.dataframe(filtered_df.head(10), use_container_width=True)
        
        with analysis_tab[1]:
            # Advanced Statistics
            st.markdown("### 📈 Advanced Statistics")
            numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) > 0:
                selected_stat_col = st.selectbox("Select Column for Advanced Stats", numeric_cols, key="adv_stat_col")
                adv_stats = calculate_advanced_stats(filtered_df, selected_stat_col)
                if adv_stats:
                    stats_df = pd.DataFrame(list(adv_stats.items()), columns=['Metric', 'Value'])
                    st.dataframe(stats_df, use_container_width=True)
            else:
                st.info("No numeric columns available for advanced statistics")
        
        with analysis_tab[2]:
            # Trend Analysis
            st.markdown("### 📉 Trend Analysis")
            if 'Date' in filtered_df.columns:
                numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
                if len(numeric_cols) > 0:
                    trend_col = st.selectbox("Select Column for Trend", numeric_cols, key="trend_col")
                    if len(filtered_df) > 1:
                        try:
                            # Calculate trend (simple linear regression)
                            filtered_df_sorted = filtered_df.sort_values('Date').dropna(subset=['Date', trend_col])
                            if len(filtered_df_sorted) > 1:
                                x = np.arange(len(filtered_df_sorted))
                                y = filtered_df_sorted[trend_col].values
                                
                                slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                                
                                st.metric("Trend Slope", f"{slope:.4f}")
                                st.metric("R-squared", f"{r_value**2:.4f}")
                                st.metric("P-value", f"{p_value:.4e}")
                                
                                trend_direction = "Increasing" if slope > 0 else "Decreasing" if slope < 0 else "Stable"
                                st.metric("Trend Direction", trend_direction)
                            else:
                                st.warning("Not enough valid data points for trend analysis")
                        except Exception as e:
                            st.error(f"Error calculating trend: {str(e)}")
                    else:
                        st.info("Need at least 2 data points for trend analysis")
                else:
                    st.info("No numeric columns available for trend analysis")
            else:
                st.info("Date column required for trend analysis")
    
    st.markdown("---")
    
    # Data table section
    st.header("📋 Data Table")
    
    # Search functionality
    search_term = st.text_input("🔍 Search in data", "")
    if search_term:
        mask = filtered_df.astype(str).apply(
            lambda x: x.str.contains(search_term, case=False, na=False)
        ).any(axis=1)
        display_df = filtered_df[mask]
    else:
        display_df = filtered_df
    
    # Display data with pagination
    page_size = st.selectbox("Rows per page", [10, 25, 50, 100], index=1)
    
    total_pages = (len(display_df) // page_size) + (1 if len(display_df) % page_size > 0 else 0)
    if total_pages > 1:
        page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        st.dataframe(display_df.iloc[start_idx:end_idx], use_container_width=True)
        st.caption(f"Showing {start_idx + 1}-{min(end_idx, len(display_df))} of {len(display_df)} records")
    else:
        st.dataframe(display_df, use_container_width=True)
        st.caption(f"Showing all {len(display_df)} records")
    
    # Export section with multiple formats
    st.markdown("---")
    st.subheader("💾 Export Data")
    
    export_col1, export_col2, export_col3, export_col4 = st.columns(4)
    
    with export_col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            key="download_csv"
        )
    
    with export_col2:
        if OPENPYXL_AVAILABLE:
            excel_data = export_to_excel(filtered_df, "data.xlsx")
            if excel_data:
                st.download_button(
                    label="📊 Download as Excel",
                    data=excel_data,
                    file_name=f"filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_excel"
                )
        else:
            st.info("Excel export requires openpyxl")
    
    with export_col3:
        json_data = export_to_json(filtered_df)
        st.download_button(
            label="📄 Download as JSON",
            data=json_data,
            file_name=f"filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            key="download_json"
        )
    
    with export_col4:
        # Chart export
        if st.session_state.chart_fig is not None:
            try:
                chart_img = st.session_state.chart_fig.to_image(format="png")
                st.download_button(
                    label="🖼️ Download Chart as PNG",
                    data=chart_img,
                    file_name=f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png",
                    key="download_chart_png"
                )
            except Exception as e:
                st.info("Chart export requires kaleido package. Install with: pip install kaleido")
    
    st.markdown("---")
    st.subheader("🔧 Data Transformations")
    
    transform_col1, transform_col2 = st.columns(2)
    
    with transform_col1:
        # Data transformation options
        st.markdown("**Transform Options**")
        transform_option = st.selectbox(
            "Select Transformation",
            ["None", "Remove Duplicates", "Fill Missing (Mean)", "Fill Missing (Median)", "Drop Missing", "Normalize", "Standardize"],
            key="transform_option"
        )
        
        if transform_option != "None":
            transformed_df = filtered_df.copy()
            if transform_option == "Remove Duplicates":
                transformed_df = transformed_df.drop_duplicates()
                st.success(f"✅ Removed duplicates. Rows: {len(filtered_df)} → {len(transformed_df)}")
            elif transform_option == "Fill Missing (Mean)":
                numeric_cols = transformed_df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    transformed_df[col].fillna(transformed_df[col].mean(), inplace=True)
                st.success("✅ Filled missing values with mean")
            elif transform_option == "Fill Missing (Median)":
                numeric_cols = transformed_df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    transformed_df[col].fillna(transformed_df[col].median(), inplace=True)
                st.success("✅ Filled missing values with median")
            elif transform_option == "Drop Missing":
                original_len = len(transformed_df)
                transformed_df = transformed_df.dropna()
                st.success(f"✅ Dropped rows with missing values. Rows: {original_len} → {len(transformed_df)}")
            elif transform_option == "Normalize":
                numeric_cols = transformed_df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    col_min = transformed_df[col].min()
                    col_max = transformed_df[col].max()
                    if col_max != col_min:
                        transformed_df[col] = (transformed_df[col] - col_min) / (col_max - col_min)
                st.success("✅ Normalized numeric columns (0-1 scale)")
            elif transform_option == "Standardize":
                numeric_cols = transformed_df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    col_mean = transformed_df[col].mean()
                    col_std = transformed_df[col].std()
                    if col_std != 0:
                        transformed_df[col] = (transformed_df[col] - col_mean) / col_std
                st.success("✅ Standardized numeric columns (z-score)")
            
            if transform_option != "None":
                st.dataframe(transformed_df.head(20), use_container_width=True)
                csv_transformed = transformed_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Transformed Data",
                    data=csv_transformed,
                    file_name=f"transformed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    key="download_transformed"
                )
    
    with transform_col2:
        # Data sampling
        st.markdown("**Data Sampling**")
        sample_size = st.number_input(
            "Sample Size",
            min_value=1,
            max_value=len(filtered_df),
            value=min(100, len(filtered_df)),
            key="sample_size"
        )
        if st.button("Generate Sample", key="generate_sample"):
            sampled_df = filtered_df.sample(n=min(sample_size, len(filtered_df)), random_state=42)
            st.dataframe(sampled_df, use_container_width=True)
            csv_sample = sampled_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Sample",
                data=csv_sample,
                file_name=f"sample_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key="download_sample"
            )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p><strong>Analytics Dashboard</strong> by <a href='https://rskworld.in' target='_blank'>RSK World</a></p>
        <p>Email: help@rskworld.in | Phone: +91 93305 39277</p>
        <p>Built with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

