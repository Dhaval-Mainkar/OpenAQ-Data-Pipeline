import boto3

glue = boto3.client('glue', region_name='ap-south-1')

TABLE_NAME = 'gld_latest_sensor_data'
FIXED_LOCATION = 's3://openaq-project-dm/transformed_data/'
DATABASE_NAME = 'db-openaq-transformed'

columns = [
    {'Name': 'sensor_id', 'Type': 'bigint'},
    {'Name': 'sensor_name', 'Type': 'string'},
    {'Name': 'coverage_expected_count', 'Type': 'bigint'},
    {'Name': 'coverage_observed_count', 'Type': 'bigint'},
    {'Name': 'latest_latitude', 'Type': 'double'},
    {'Name': 'latest_longitude', 'Type': 'double'},
    {'Name': 'latest_value', 'Type': 'double'},
    {'Name': 'parameter_id', 'Type': 'bigint'},
    {'Name': 'parameter', 'Type': 'string'},
    {'Name': 'parameter_display_name', 'Type': 'string'},
    {'Name': 'parameter_units', 'Type': 'string'},
    {'Name': 'summary_avg', 'Type': 'double'},
    {'Name': 'summary_max', 'Type': 'double'},
    {'Name': 'summary_median', 'Type': 'string'},
    {'Name': 'summary_min', 'Type': 'double'},
    {'Name': 'std_coverage_from_local', 'Type': 'string'},
    {'Name': 'std_coverage_from_utc', 'Type': 'string'},
    {'Name': 'std_coverage_to_local', 'Type': 'string'},
    {'Name': 'std_coverage_to_utc', 'Type': 'string'},
    {'Name': 'std_datetime_first_local', 'Type': 'string'},
    {'Name': 'std_datetime_first_utc', 'Type': 'string'},
    {'Name': 'std_datetime_last_local', 'Type': 'string'},
    {'Name': 'std_datetime_last_utc', 'Type': 'string'},
    {'Name': 'std_latest_datetime_local', 'Type': 'string'},
    {'Name': 'std_latest_datetime_utc', 'Type': 'string'},
    {'Name': 'std_coverage_expected_interval', 'Type': 'string'},
    {'Name': 'std_coverage_observed_interval', 'Type': 'string'},
    {'Name': 'std_coverage_percent_complete', 'Type': 'string'},
    {'Name': 'std_coverage_percent_coverage', 'Type': 'string'},
    {'Name': 'std_parameter_name', 'Type': 'string'},
    {'Name': 'value', 'Type': 'double'},
    {'Name': 'location_id', 'Type': 'bigint'},
    {'Name': 'std_datetime_utc', 'Type': 'string'},
    {'Name': 'std_datetime_local', 'Type': 'string'},
    {'Name': 'std_location_name', 'Type': 'string'},
    {'Name': 'std_locality', 'Type': 'string'},
    {'Name': 'country_id', 'Type': 'bigint'},
    {'Name': 'std_country_name', 'Type': 'string'},
    {'Name': 'std_country_code', 'Type': 'string'},
    {'Name': 'owner_name', 'Type': 'string'},
    {'Name': 'provider_id', 'Type': 'bigint'},
    {'Name': 'isMobile', 'Type': 'boolean'},
    {'Name': 'isMonitor', 'Type': 'boolean'},
    {'Name': 'instrument_id', 'Type': 'bigint'},
    {'Name': 'std_owner_name', 'Type': 'string'},
    {'Name': 'std_provider_name', 'Type': 'string'},
    {'Name': 'parameter_name', 'Type': 'string'},
    {'Name': 'parameter_displayName', 'Type': 'string'},
    {'Name': 'license_id', 'Type': 'bigint'},
    {'Name': 'std_license_name', 'Type': 'string'},
    {'Name': 'std_license_attribution_name', 'Type': 'string'},
    {'Name': 'std_instrument_name', 'Type': 'string'},
    {'Name': 'std_timezone', 'Type': 'string'},
    {'Name': 'std_first_seen_utc', 'Type': 'string'},
    {'Name': 'std_last_seen_utc', 'Type': 'string'},
    {'Name': 'attributionRequired', 'Type': 'boolean'},
    {'Name': 'commercialUseAllowed', 'Type': 'boolean'},
    {'Name': 'modificationAllowed', 'Type': 'boolean'},
    {'Name': 'redistributionAllowed', 'Type': 'boolean'},
    {'Name': 'shareAlikeRequired', 'Type': 'boolean'},
    {'Name': 'manufacturer_id', 'Type': 'bigint'},
    {'Name': 'std_manufacturer_name', 'Type': 'string'}
]

TABLE_INPUT = {
    'Name': FIXED_TABLE_NAME,
    'StorageDescriptor': {
        'Location': FIXED_LOCATION,
        'InputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat',
        'OutputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat',
        'SerdeInfo': {
            'SerializationLibrary': 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
        },
        'Columns': columns
    },
    'TableType': 'EXTERNAL_TABLE',
    'Parameters': {
        'classification': 'parquet',
        'recurse': 'true'          # tells Athena to scan all subfolders
    }
}

def lambda_handler(event, context):
    try:
        # Table already exists — update it in place (no data loss)
        glue.update_table(DatabaseName=DATABASE_NAME, TableInput=TABLE_INPUT)
    except glue.exceptions.EntityNotFoundException:
        # First time — create it
        glue.create_table(DatabaseName=DATABASE_NAME, TableInput=TABLE_INPUT)

    return {
        'statusCode': 200,
        'body': f'Table {FIXED_TABLE_NAME} is up to date'
    }