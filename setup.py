"""
Setup script for Streamlit Analytics Dashboard
==============================================

Installation and setup utilities for the dashboard project.

Author: RSK World
Website: https://rskworld.in
Email: help@rskworld.in
Phone: +91 93305 39277
"""

from setuptools import setup, find_packages

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="streamlit-analytics-dashboard",
    version="1.0.0",
    author="RSK World",
    author_email="help@rskworld.in",
    description="Interactive analytics dashboard built with Streamlit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://rskworld.in",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    keywords="streamlit, dashboard, analytics, visualization, data-science",
    project_urls={
        "Website": "https://rskworld.in",
        "Source": "https://github.com/rskworld/streamlit-dashboard",
    },
)

