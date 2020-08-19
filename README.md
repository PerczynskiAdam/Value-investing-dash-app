# GPW value investing app
Visualization app created to automate stocks value analyzes. Data used in this app was scraped from the websites using Beautiful Soap 4. Gathered data was transformed with ETL methods in Python.
https://gpw-value-app.herokuapp.com/

# General info
   The goal of this project was to interactive visualize the data for GPW stocks.  
   Based on this solution we can filter stocks to answer a question:  
   Can we find stocks on polish stock market that have good valuation according to buisness fundamentals?  
   The next step will be to check how change the prize of companies that had good valuation in the past. 

# Technologies
1.  Dash - version 1.11.0
2.  Dash-bootstrap-components - version 0.10.0
3.  Dash-table - version 4.6.2
4.  Python - version 3.8.2
  * Beatiful Soap 4
  * Request
  * Plotly
  * Pandas
  * Numpy
  * Re
  * Glob
  * Functools (reduce)
5.  CSS/HTML

# Setup
To run this project create virtual environment, install dependencies from requirements.txt file and run code from Dashboard.py file

# Features
The dashboard_tables.py give possibility to answer questions:  
1. Which stocks are well valuated according to buisness fundamentals like Prize to Earning ratio and Return on Equity ratio?  
2. Is companies well valuated in the past gave profits?


To answer first question we can filter dataset with p/e and roe values.  
By providing values with inputs:  
![alt text](https://github.com/PerczynskiAdam/Value-investing-dash-app/blob/master/images/inputs.png "Inputs to filter data")  


We filter dataset on backend and app is displaying results:  
![alt text](https://github.com/PerczynskiAdam/Value-investing-dash-app/blob/master/images/filtered_data.png "Filtered table on backend")  
Based on this we see stocks tickers which corresponds to defined inputs  
Those stocks can be taken for further analysis  


