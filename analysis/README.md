# Analysis 
DESCRIBE CONTENT IN THIS DIRECTORY

# Dependencies
1. pip install scipy
2. pip install matplotlib
3. pip install reportlab
4. pip install joblib
5. pip install scikit-learn
6. pip install pandas
7. pip install pytz

## Linear Regression Models
The linear regression model is used to predict the daily power consumption for the entire current month of each device of the racks that were monitored which is Rack 1, Rack 2 & Rack 3.

### **How to use**
Before training the model, we need to preprocess and prepare the dataset first. So, these are the steps taken:
1. Ensure that the Power Consumption CSV file is available inside the analysis/data folder.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/80d7dfd5-1af0-4e4a-ae35-f6324d3eaf10)

2. Next, create an instance of the LinearRegressionModel class.
   
3. Then, call the data_preprocessing method and pass the CSV file as the parameter. This method will read the CSV file and return the data as a Pandas dataframe. Then, it will fill up any missing values in the dataframe by creating the missing timestamps first, then filling the value for those timestamps depending on these conditions:
   - If the device has 'Water' in its name, we perform backward or forward filling. Backward filling means filling the missing value with the previous data while forward filling means filling the missing value with the next data.
   - If the device has 'Light' in its name, we perform backward or forward filling if the missing value falls within the schedule that the grow lights of the rack are supposed to be turned on. Else, we fill in the missing value with the average timer value.

4. Once done, call the data_preparation method and pass the variable from the data_preprocessing method. This method will prepare the variables needed for model training such as x, y, features x_train, y_train, x_test & y_test.
    - First, this method calls on get_daily_values method which will split the dataframe into the different device types and then, calculate the daily values of each device type and store them into another dataframe.
    - Then, it will create the x & y variables.
      - The x and features variable consists of independent variables from the dataframe such as day_of_month, month, device_name.
      - The y variable consists of dependent variable such as _value.
    - Lastly, it will create the x_train, y_train, x_test & y_test variables by splitting the dataframe into training and testing set by 80:20 split ratio.
  
![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/4271130a-88f2-4a02-be15-7e870e519701)

Then, after these steps, we can proceed with the model training and the monthly predictions (if model already exists).

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/1acd815b-48f0-430e-8e65-de2dcfa96c77)

The model_training method takes in x_train, y_train, x_test & y_test variables as its parameters. Then, it will create an instance of the LinearRegression class from sklearn.linear_model and use the x_train & y_train to fit the model. Lastly, it will save the model made into a file for other uses like get_monthly_predictions

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/df900d63-2d9a-4112-88bc-5a05586bc0ce)

The get_monthly_predictions method uses this model to predict the daily power consumption for the entire current month for each device and store the result as a CSV file.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/563b4788-c432-455c-a9ee-262a510f690e)

### Historical Correlation

## Cost Efficiency
