# Earthquakes from 1995 to 2023

A simple Streamlit app template for you to modify!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://my-app-5nq20n29mrw.streamlit.app/)

Project: Earthquake Data Analysis and Visualization
This project focuses on analyzing earthquake data and visualizing different aspects of their characteristics, such as magnitude, depth, frequency, geographic location, and the relationship with tsunami occurrences. Streamlit is used to build an interactive interface, and pandas, matplotlib, and folium libraries are used for data processing and visualization.

Files
earthquake_1995-2023.csv: CSV file containing data on earthquakes from 1995 to 2023, including magnitude, depth, date, coordinates, continent, and information about tsunamis.
streamlit_app.py: Main application script that performs data processing and visualization in Streamlit.

Key Functionality
1. Interactive Earthquake Distribution Map
Description: Allows the user to select a continent and year to view earthquakes in a specific region and time period.
Filters: Continent, year (with options to select "All Continents" and "All Years").
Visualization Features: Color-coded by earthquake magnitude with a legend.
Library: folium is used for the interactive map.
2. Earthquake Trend by Year
Description: A trend line chart showing the change in the number of earthquakes over the years, helping to analyze yearly trends.
Table: Displays the number of earthquakes per year in a horizontal format.
Library: matplotlib for the trend line, pandas for data preparation.
3. Tsunami Occurrence Based on Depth and Magnitude
Description: A scatter plot showing the relationship between earthquake depth, magnitude, and the probability of triggering a tsunami.
Color Coding: Earthquakes that caused a tsunami are shown in red, while others are shown in blue.
Library: matplotlib for the scatter plot.

How to Run the Application
1. Install Dependencies:
$ pip install -r requirements.txt

2. Run the Application in Streamlit:
$ streamlit run streamlit_app.py

3. Open Your Browser and go to the link displayed in the console (typically http://localhost:8501).

Code Structure
Data Loading and Processing: The CSV file is loaded using pandas. The app processes the dates and adds a column with the year for convenient filtering.
Filtering: All filters are applied directly in Streamlit, providing an intuitive interface.
Visualization:
Map visualization (folium): Used for the interactive display of earthquake distribution.
Graphs (matplotlib): Used for trend lines and scatter plots.

Visualization Examples
Earthquake Map: Shows earthquake distribution by selected continent and year.
Trend Line: Displays the number of earthquakes over the years and a horizontal table of earthquake counts by year.
Scatter Plot (Tsunami): Visualizes the relationship between magnitude, depth, and tsunami occurrence probability.

Future Enhancements
Add more filters, such as magnitude or depth.
Implement tsunami probability forecasting based on depth and magnitude.
Enable exporting of graphs and tables.

Conclusions
This application provides a tool for exploring earthquake data, helping to gain deeper insights into their characteristics and the factors contributing to tsunami occurrences.
