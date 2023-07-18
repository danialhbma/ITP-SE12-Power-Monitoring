from CorrelationCalculator import CorrelationCalculator, CorrelationPlotter

# Define the bucket configurations
bucket_configs = [
    {
        'bucket_name': 'Temperature',
        'time_frame': '16d',
        'time_interval': '30m'
    },
    {
        'bucket_name': 'Power Consumption',
        'time_frame': '16d',
        'time_interval': '1h'
    },
        {
        'bucket_name': 'WeatherAPI',
        'time_frame': '16d',
        'time_interval': '30m'
    },
    # Add more bucket configurations if needed
]

# Create an instance of the CorrelationCalculator
calculator = CorrelationCalculator(bucket_configs)

# Read and process data from each bucket
for bucket_config in bucket_configs:
    result = calculator.read_data_from_bucket(bucket_config)

calculator.calculate_historical_correlations(result)
calculator.print_historical_correlations()
plotter = CorrelationPlotter(calculator.correlations)
plotter.plot_correlation_matrix("Monthly corrleation")