import pandas as pd
import boto3
from io import BytesIO

def read_s3_excel(file_key):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket='tonabor', Key='uploads/' + file_key)
    return pd.read_excel(BytesIO(obj['Body'].read()))

def process_all_data():
    # Example: merge near_expiry and master file
    near_expiry = read_s3_excel('6_month_Near_expiry.xlsx')
    master = read_s3_excel('master.xls')
    master_subset = master[['ITEM_CODE', 'GENERIC_NAME', 'CONVERSION_FACTOR', 'OP_UNIT']]
    near_expiry = near_expiry.rename(columns={'ITEM_NUMBER': 'ITEM_CODE'})
    merged = pd.merge(near_expiry, master_subset, on='ITEM_CODE', how='left')
    summary = merged.groupby('CATEGORY_NAME').size().reset_index(name='count')
    return {'summary_table': summary.to_html()}
