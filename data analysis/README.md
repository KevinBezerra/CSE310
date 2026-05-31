# Overview

As a Data Analyst, my goal for this project is to build foundational programming skills for data manipulation. I am moving beyond querying existing data in BI tools to programmatically building scripts that combine, clean, and analyze raw datasets at the source.

This software is a Python script that analyzes three years (2015–2017) of dog registration data from a German city. It reads multiple local CSV files, merges them with a breed mapping table, and performs data manipulation (filtering, sorting, aggregation, and conversion) to extract analytical insights. 

My purpose for writing this software is to gain hands-on experience with Python data analysis libraries, specifically Pandas for data wrangling and Matplotlib for data visualization.

[Software Demo Video](https://youtu.be/4INY6WxG1Ck)

# Data Analysis Results

I am using a dataset consisting of three annual snapshots of dog registrations (2015, 2016, and 2017) and a mapping table that categorizes dog breeds. The data contains information such as owner age demographics, city districts, and primary dog breeds.

The script answers two specific questions about this data:
1. **How did the total number of registered dogs change from 2015 to 2017?** (Demonstrates data aggregation by year).
2. **What were the top 5 most popular dog breeds in 2017?** (Demonstrates filtering by year, sorting, and counting occurrences).

To support the analysis, the software also generates a bar chart visualizing the top 5 most popular breeds in 2017.

# Development Environment

* Visual Studio Code (VS Code)
* Git & GitHub
* Python 3
* Libraries: `pandas`, `matplotlib`

# Useful Websites

* [Pandas Documentation - 10 Minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
* [Matplotlib Plotting Tutorial](https://matplotlib.org/stable/tutorials/introductory/pyplot.html)
* [Python Data Analysis - FreeCodeCamp](https://www.freecodecamp.org/news/data-analysis-with-python-tutorial/)

# Future Work

* Build an automated pipeline to extract this cleaned Pandas dataframe into Snowflake for broader analytical querying and dashboard visualization in ThoughtSpot.
* Implement geospatial mapping to visualize dog breed density across different city districts.
* Write a function to automatically translate all German categorical variables within the rows into English for easier downstream reporting.