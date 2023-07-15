import json
from InfluxDBWriter import InfluxDBWriter

"""
Helper function to mass create buckets 
Running python BucketCreator.py will create all the buckets listed in buckets.json. 
Ignores if buckets already exists.

Usage: 
1. populate the buckets.json file with names and buckets to create.
2. python BucketCreator.py 
"""

# Instantiate InfluxDBWriter
writer = InfluxDBWriter()

# Load bucket configurations from JSON file
with open('buckets.json') as json_file:
    buckets = json.load(json_file)

# Create buckets from configurations
for bucket_config in buckets:
    bucket_name = bucket_config['name']
    bucket_description = bucket_config['description']
    writer.create_bucket(bucket_name, bucket_description)
