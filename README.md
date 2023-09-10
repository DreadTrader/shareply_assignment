
sharpely_assignment

Working:

In this code, I am extracting data on-demand and staging it for experimentation since my laptop has low space.
After the server starts, the user will log in to 127.0.0.1:5005, and login safety is not provided.
Once logged in, the user will choose from available scripts, as the requirement was for a search bar that can be implemented as well.
The user will choose a time frame duration, with default values provided for the start and end times.
After making selections, the user will click on "Get Data" to populate charts and indicator values.

Explanation of the Code:

A. Frontend:

    1. The frontend is written in JavaScript using JQuery and Plotly for plotting.
    2. Charts are provided in a list of record format, and indicator values are provided in a dictionary format.
    3. An event listener is added to the "Get Data" button.
B. Backend:

    1. The backend is written in Flask in Python.
    2. Spark is not used for three main reasons:
    3. The data to be processed is less than 1 GB, which is manageable by my computer's power.
    4. Forward filling and aggregation of data, as per my knowledge, require taking data back to Pandas, as we are using Pandas_TA libraries.
    5. It's been a while since I haven't used Spark, and I want to complete the problem statement as soon as possible.
Working of the backend:
    a. Once the data to be processed is received by the "get_stock_data" API, the program will check if uncompressed data is available or not. If not, it will extract it from the zip file and then process it.
    b. Required data cleaning logic has been written here.
    c. Data will be aggregated based on user requirements.
    d. The entire data will be stored in the data_raw variable, and a sample of data will be taken for indicator calculation.
    f. After calculation, raw data and indicator values will be sent back to the frontend.

Instructions to Use the Frontend:
    1. Open 127.0.0.1:5005.
    2. username = mangesh, password = mangesh
    3. select stock from dropdown, select time frame from dropdown
    4. select data recomended from date = "10-02-2015" to date = "10-02-2016"
    5. click on GET DATA 

    indicator and chart will be populated

Caveats:
    1. CCA indicator and Ichimoku indicator are not implemented properly due to time restrictions.
    2. To check rough work, I'm intentionally keeping test.ipynb with the code. It won't make any sense but might be useful.
    3. logic of read filenames from zip and then taking decision to download it or not is developed becuase of less space in computer.

****** Important inorder to program to work please add zip file in data folder ********
        

