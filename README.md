# Streamlit Analytics Dashboard

Interactive analytics dashboard built with Streamlit for data exploration, visualization, and real-time analysis with user-friendly interface.

**Author:** RSK World  
**Website:** [https://rskworld.in](https://rskworld.in)  
**Email:** help@rskworld.in  
**Phone:** +91 93305 39277

## Description

This project creates a comprehensive analytics dashboard using Streamlit framework. It provides interactive widgets, real-time data filtering, multiple visualization types, and user-friendly interface for data exploration. Perfect for building quick prototypes and data analysis applications.

## Features

### Core Features
- ✅ Interactive widgets and filters
- ✅ Real-time data exploration
- ✅ User-friendly interface
- ✅ Easy deployment
- ✅ CSV file upload support
- ✅ Sample data generation for demonstration

### Visualizations (10+ Chart Types)
- ✅ Line Charts - Time series analysis
- ✅ Bar Charts - Categorical comparisons
- ✅ Scatter Plots - Relationship analysis
- ✅ Pie Charts - Distribution visualization
- ✅ Area Charts - Cumulative trends
- ✅ Heatmaps - Correlation analysis
- ✅ Box Plots - Distribution and outliers
- ✅ Histograms - Frequency distribution
- ✅ Violin Plots - Distribution comparison
- ✅ 3D Scatter Plots - Multi-dimensional analysis

### Advanced Features
- ✅ Date range presets (Last 7/30/90 days, Last 6 months, Last year, etc.)
- ✅ Data quality metrics dashboard
- ✅ Advanced statistical analysis (skewness, kurtosis, outliers, etc.)
- ✅ Trend analysis with linear regression
- ✅ Multiple export formats (CSV, Excel, JSON)
- ✅ Chart export as PNG images
- ✅ Data transformation tools (normalize, standardize, fill missing values)
- ✅ Data sampling functionality
- ✅ Duplicate detection and removal
- ✅ Missing value analysis and handling

## Technologies Used

- **Python** - Programming language
- **Streamlit** - Web framework for building the dashboard
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **SciPy** - Statistical analysis and scientific computing
- **OpenPyXL** - Excel file support

## Installation

1. Clone or download this repository

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit dashboard:
```bash
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## Features Overview

### Data Sources
- **Sample Data**: Pre-generated sample dataset for demonstration
- **CSV Upload**: Upload your own CSV files for analysis

### Interactive Filters
- Date range selection
- Region filtering
- Product filtering
- Category filtering
- Real-time data filtering

### Visualizations
- **Line Charts**: Time series analysis
- **Bar Charts**: Categorical comparisons
- **Scatter Plots**: Relationship analysis
- **Pie Charts**: Distribution visualization
- **Area Charts**: Cumulative trends
- **Heatmaps**: Correlation analysis

### Data Management
- Search functionality
- Pagination support
- Data export (CSV download)
- Summary statistics
- Top records display

## Project Structure

```
streamlit-dashboard/
├── app.py                 # Main Streamlit application
├── utils.py               # Utility functions for data processing
├── visualizations.py      # Custom visualization functions
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## Customization

You can customize the dashboard by:

1. **Modifying data sources**: Edit the `load_sample_data()` function in `app.py`
2. **Adding new visualizations**: Extend `visualizations.py` with new chart types
3. **Customizing filters**: Modify the filter section in the sidebar
4. **Styling**: Update the CSS in the `st.markdown()` section

## Deployment

### Local Deployment
Simply run `streamlit run app.py` on your local machine.

### Cloud Deployment

#### Streamlit Cloud
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy!

#### Other Platforms
- **Heroku**: Use the Streamlit buildpack
- **AWS**: Deploy using EC2 or ECS
- **Docker**: Containerize the application

## Example Use Cases

- Sales analytics and reporting
- Customer behavior analysis
- Financial data visualization
- Marketing campaign performance
- Inventory management
- Any time-series or categorical data analysis

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Author:** RSK World  
**Website:** [https://rskworld.in](https://rskworld.in)  
**Email:** help@rskworld.in  
**Phone:** +91 93305 39277

## Support

For questions or support, please contact:
- **Email:** help@rskworld.in
- **Website:** [https://rskworld.in](https://rskworld.in)
- **Phone:** +91 93305 39277

## Acknowledgments

Built with ❤️ using Streamlit and Plotly.

---

**RSK World** - Free Programming Resources & Source Code  
Visit us at [rskworld.in](https://rskworld.in)

