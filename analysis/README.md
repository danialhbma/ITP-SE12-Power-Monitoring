# Analysis 
DESCRIBE CONTENT IN THIS DIRECTORY

# Dependencies
1. pip install scipy
2. pip install matplotlib
3. pip install reportlab
4. pip install pandas
5. pip install pytz
6. pip install numpy

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
The ``MonthlyCorrelation.py`` works similarly to ``HistoricalCorrelation.py`` but it performs correlation analysis on external weather data (from OpenWeatherMap API) and internal farm conditions (which is our live sensor data obtained from our deployed sensors) for the month.

Strength of Correlation Coefficients is based on https://www.bmj.com/about-bmj/resources-readers/publications/statistics-square-one/11-correlation-and-regression

## Cost Efficiency
The ``cost_efficiency.py`` uses a historical analysis to retrieve the lowest cost period (day/night) and season (within 3 temperature ranges) based on the data collected for power consumption and external environmental API calls.

For the analysis on cost efficient period, the script categorises the power data into the categories defined by the two time ranges, before retrieving the total power consumption (kWh). These values will be converted into cost, and the most cost efficient period can be determined.

Analysis on cost efficient season works in a similar fashion. The script categorises the power data into categories defined by 3 different temperature ranges, before retreiving the total power consumption (kWh) for each of the categories. These values will be converted into cost, and the most cost efficient season can be determined.

## Variables that Affect Power Consumption
``variables_that_affect_power.py`` works by taking power consumption data, obtaining the mean readings for purple LED grow lights, white LED grow lights, and water pumps. Using the mean readings, it calculates the estimated power consumption of each item, as well as the estimated power consumption of the aircon units used in the container. 

This is outputted in a pie chart that shows a breakdown of the total power consumption of the current container farm and how much each item contributes to the overall power consumption.

# Analysis and Reports Generation
Retrieves updated data files from InfluxDB using [extract_raw_data.py](README.md), executes all analysis scripts in [analysis folder](../analysis) and runs the [ReportGeneration.py](../analysis/ReportGeneration.py). Generated report is sent via Telegram. 
