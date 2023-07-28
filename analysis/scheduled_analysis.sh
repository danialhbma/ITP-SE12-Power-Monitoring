#!/bin/bash

# Change working directory to the analysis directory
cd /home/yappi/ITP-SE12-Power-Monitoring/analysis

# Execute scripts in sequence
python3 extract_raw_data.py
# Copy Power Consumption.csv to the ../docker-containers/api folder
cp /home/yappi/ITP-SE12-Power-Monitoring/analysis/data/"Power Consumption.csv" /home/yappi/ITP-SE12-Power-Monitoring/docker-containers/api/
python3 MonthlyCorrelation.py
python3 HistoricalCorrelation.py
python3 cost_efficiency.py
python3 variables_that_affect_power.py
python3 LinearRegressionAnalysis.py
