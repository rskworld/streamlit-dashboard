# Quick Start Guide - Streamlit Analytics Dashboard

**Author:** RSK World  
**Website:** [https://rskworld.in](https://rskworld.in)  
**Email:** help@rskworld.in  
**Phone:** +91 93305 39277

## Installation Steps

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Dashboard

**Option 1: Using Streamlit directly**
```bash
streamlit run app.py
```

**Option 2: Using provided scripts**

Windows:
```bash
run.bat
```

Linux/Mac:
```bash
chmod +x run.sh
./run.sh
```

### 4. Access the Dashboard

The dashboard will automatically open in your default web browser at:
```
http://localhost:8501
```

## Using the Dashboard

### Sample Data Mode
1. Select "Sample Data" from the sidebar
2. The dashboard will load with pre-generated sample data
3. Use filters to explore the data
4. Switch between different chart types

### Upload Your Own Data
1. Select "Upload CSV File" from the sidebar
2. Click "Browse files" and select your CSV file
3. Wait for the file to load
4. The dashboard will automatically detect columns and create visualizations

### Features to Try
- **Filters**: Use sidebar filters to narrow down your data
- **Chart Types**: Switch between Line, Bar, Scatter, Pie, Area, and Heatmap charts
- **Search**: Use the search box to find specific records
- **Export**: Download filtered data as CSV

## Troubleshooting

### Port Already in Use
If port 8501 is already in use, Streamlit will automatically use the next available port.

### Missing Dependencies
If you encounter import errors, make sure all dependencies are installed:
```bash
pip install --upgrade -r requirements.txt
```

### File Upload Issues
- Ensure your CSV file has headers in the first row
- Check that the file is not too large (max 200MB recommended)
- Verify the file encoding is UTF-8

## Next Steps

- Customize the dashboard by editing `app.py`
- Add your own data processing logic in `utils.py`
- Create custom visualizations in `visualizations.py`
- Modify configuration in `config.py`

## Support

For help and support:
- **Email:** help@rskworld.in
- **Website:** [https://rskworld.in](https://rskworld.in)
- **Phone:** +91 93305 39277

---

**Happy Analyzing! 📊**

