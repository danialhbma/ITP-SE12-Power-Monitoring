from CorrelationCalculator import CorrelationCalculator, CorrelationPlotter

# Define the bucket configurations
bucket_configs = [
    {
        'bucket_name': 'Historical Weather Data',
        'time_frame': '30d',
        'time_interval': '1m'
    },
    {
        'bucket_name': 'Historical Power Consumption',
        'time_frame': '30d',
        'time_interval': '1m'
    },
    # Add more bucket configurations if needed
]

# Create an instance of the CorrelationCalculator
calculator = CorrelationCalculator(bucket_configs)

# Read and process data from each bucket
for bucket_config in bucket_configs:
    result = calculator.read_data_from_bucket(bucket_config)

calculator.calculate_correlations(result)
calculator.print_correlations()

plotter = CorrelationPlotter(calculator.correlations)
plotter.plot_correlation_matrix("Historical Weather data vs Historical Farm Power Consumption")
