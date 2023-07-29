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
8. pip install numpy

## Linear Regression Models
The ``LinearRegressionAnalysis.py`` is used to predict the daily power consumption for the entire current month of each device of the racks that were monitored which is Rack 1, Rack 2 & Rack 3.

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

The model_training method takes in x_train, y_train, x_test & y_test variables as its parameters. Then, it will create an instance of the LinearRegression class from sklearn.linear_model and use the x_train & y_train to fit the model. Lastly, it will save the model made into a file for other uses like get_monthly_predictions.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/df900d63-2d9a-4112-88bc-5a05586bc0ce)

The get_monthly_predictions method uses this model to predict the daily power consumption for the entire current month for each device and store the result as a CSV file.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/563b4788-c432-455c-a9ee-262a510f690e)

## Historical Correlation
The ``HistoricalCorrelation.py`` is used to calculate the correlation between 2 buckets - Historical Power Consumption & Historical Weather Data and produce a heatmap to represent the result. It uses the CorrleationCalculator & CorrelationPlotter classes from the ``CorrelationCalculator.py`` to do this.

### **How to use**
Inside ``HistoricalCorrelation.py``, we define the buckets that we want to read from as the bucket_configs variable.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/ab7944fd-3f4c-4052-9985-3e43c628eb33)

Then, we create an instance of the CorrelationCalculator and call the read_data_from_bucket method and pass the bucket_configs as its parameter.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/f2dbe580-b1d7-449d-859d-0d2f041193b0)

The read_data_from_bucket method will process each bucket as a dataframe and process the dataframe based on the bucket as some buckets only have monthly data while others have daily data and to calculate correlation, each variable needs to have the same amount of data points. Hence, the different processing of each bucket.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/66207f72-9899-4f63-b6ad-910564f7ffa1)

The output from read_data_from_bucket method will be passed to the calculate_correlations method which will correlate each variable in the output against each other including itself and store the result into a dictionary in this format -  "variable 1 vs variable 2" : result. Then, we create an instance of CorrelationPlotter and call the plot_correlation_matrix method to produce the heatmap for our correlation result.

![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/92836838/122025e1-47bd-483a-8c29-4cd89b738d08)

## Monthly Correlation
The ``MonthlyCorrelation.py`` works similarly to ``HistoricalCorrelation.py`` but it produces 2 types of heatmap instead - 1 heatmap represents the correlation of WeatherAPI bucket and Internal Farm Conditions bucket (Temperature & Humidity) and the other heatmap represents only the strong correlation between the WeatherAPI bucket, Internal Farm Conditions bucket (Temperature & Humidity) and power consumption (which is a CSV file). 

Inside ``MonthlyCorrelation.py``, we made 2 functions - Correlate_ExtCond_To_IntCond and Correlate_ExtCond_To_IntCond_To_FPC which differentiates the 2 heatmaps. The Correlate_ExtCond_To_IntCond works exactly the same as in ``HistoricalCorrelation.py`` where it will process the bucket_configs and then, calculate the correlation and produce the heatmap.

But for the Correlate_ExtCond_To_IntCond_To_FPC, it has additional steps which are to read the CSV file and store the power consumption value into the output of read_data_from_bucket method. Then, it will calculate the correlation and remove any weak correlation of those variables against power consumption based on the threshold (0 < 0.4 for positive relationship & -0.4 > 0 for negative relationship). Once we remove the weak correlation, we will produce the heatmap.

Threshold is based on https://www.bmj.com/about-bmj/resources-readers/publications/statistics-square-one/11-correlation-and-regression

## Cost Efficiency

# Temperature Analysis
Linear regression model was used to gauge / predict how internal farm temperature changes based off external farm temperature. Internal farm temperature retrieved from rack1, rack2 and rack3 temperature sensor readings while external farm temperature uses OpenWeatherMap temperature field.

## High Level Overview
1. Load both internal and external temperature data from their respective CSV files.
2. Parse the timestamps from both datasets and set them as the index.
3. Resample both datasets to get hourly average temperatures.
4. Merge the two dataframes based on their timestamps.
5. Handle missing data by replacing NaN entries with the mean of the respective column.
6. Split the merged dataset into features (X - external temperatures) and target (y - internal temperatures).
7. Further split the datasets into training and testing sets.
8. Use the training set to train a linear regression model.
9. Use the testing set to evaluate the model.

## Model Explanation
We used a linear regression model to predict the internal farm temperature based on the external temperature.

The model assumes that there is a linear relationship between these two variables. The slope of the model (~0.755) implies that for every degree Celsius increase in the external temperature, the model predicts that the internal temperature will increase by about 0.755 degrees Celsius. The intercept of the model is approximately -2.21.

We evaluated the model using the mean absolute error (MAE) metric, which provides an average of the absolute differences between the model's predictions and the actual internal temperatures. The MAE for this model is approximately 0.96, indicating that on average, the model's predictions are about 0.96 degrees Celsius away from the actual values.

Please note that these results are based on the specific dataset we have and may vary as new data are collected.

Conclusion
This model provides a simple way to predict the internal temperature of the farm based on the external temperature, and it can be a useful tool for farm management. However, it is important to remember that temperature dynamics can be influenced by many other factors not considered in this model, such as insulation, humidity, and air circulation. Further research and more complex models might be needed to accurately predict internal temperature under various conditions.