import pandas as pd
import boto3
from io import BytesIO
from decouple import config

# Reads a single Excel file from S3 bucket
def read_s3_excel(file_key):
    s3 = boto3.client(
        's3',
        aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
        region_name=config('AWS_S3_REGION_NAME')
    )
    try:
        obj = s3.get_object(Bucket=config('AWS_STORAGE_BUCKET_NAME'), Key='uploads/' + file_key)
        return pd.read_excel(BytesIO(obj['Body'].read()))
    except s3.exceptions.NoSuchKey:
        raise FileNotFoundError(f"The file {file_key} was not found in S3.")
    except Exception as e:
        raise RuntimeError(f"Error reading {file_key}: {str(e)}")

# Aggregates and merges data for dashboard display
def process_all_data():
    try:
        near_expiry = read_s3_excel('6_month_Near_expiry.xlsx')
        master = read_s3_excel('master.xlsx')

        # Clean master file: Ensure numeric and drop rows with invalid values
        master['CONVERSION_FACTOR'] = pd.to_numeric(master['CONVERSION_FACTOR'], errors='coerce')
        master = master.dropna(subset=['CONVERSION_FACTOR'])

        # Extract relevant columns
        master_subset = master[['ITEM_CODE', 'GENERIC_NAME', 'CONVERSION_FACTOR', 'OP_UNIT']]
        near_expiry = near_expiry.rename(columns={'ITEM_NUMBER': 'ITEM_CODE'})

        # Merge datasets
        merged = pd.merge(near_expiry, master_subset, on='ITEM_CODE', how='left')

        if 'CATEGORY_NAME' not in merged.columns:
            raise KeyError("CATEGORY_NAME column not found in merged data.")

        # Group summary
        summary = merged.groupby('CATEGORY_NAME').size().reset_index(name='count')

        return {'summary_table': summary.to_html(classes="table table-bordered")}
    
    except Exception as e:
        return {'summary_table': f'<p style="color:red">Dashboard error: {str(e)}</p>'}
