"""Module to serve as introduction to AWS Simple Cloud Storage Service (S3)

   Prerequisites:
   - Installation of `boto3`
   - Creating and adding AWS credentials to `.aws/credentials` file
   - Creating and adding AWS region for computing resources in `.aws/config` file
   - s3f3 documentation: https://s3fs.readthedocs.io/en/latest/?badge=latest
   - Note: s3fs is a wrapper for boto3
"""

import logging

import boto3
import joblib
import pandas as pd
import s3fs

logging.basicConfig(level=logging.INFO)
# Define one logger for current file, per
# https://www.loggly.com/blog/4-reasons-a-python-logging-library-is-much-better-than-putting-print-statements-everywhere/
LOGGER = logging.getLogger(__name__)

BUCKET_NAME = "stats404-project"
KEY_NAME_DATA = "airlines_data_1987_1000rows.csv"
KEY_NAME_MODEL = "rf_Fashion_MNIST_500_trees.joblib"
FILE_NAME = "https://s3.amazonaws.com/h2o-airlines-unpacked/year1987.csv"


if __name__ == '__main__':
    ### ---------------------------------------------------------------------------
    ### --- Part 1: Connect to S3 Bucket on AWS
    ### ---------------------------------------------------------------------------
    LOGGER.info("--- Part 1: Connect to S3 Bucket on AWS")

    # Approach 1:
    s3 = boto3.resource('s3')

    # Approach 2:
    # - anon=False: use AWS credentials to connect to file system, not as an anonymous user
    s3_fs = s3fs.S3FileSystem(anon=False)

    LOGGER.info("List of buckets currently available on AWS S3:")
    for bucket in s3.buckets.all():
        if bucket.name == BUCKET_NAME:
            LOGGER.info(f"    {bucket.name}")

    LOGGER.info(f"List of objects in bucket {BUCKET_NAME}:")
    for file in s3.Bucket(BUCKET_NAME).objects.all():
        LOGGER.info(f"    {file.key}")

    ### ---------------------------------------------------------------------------
    ### --- Part 2: Upload CSV File to S3 Bucket
    ### ---------------------------------------------------------------------------
    LOGGER.info("--- Part 2: Upload CSV File to S3 Bucket")

    # --- Create a data set to upload -- or use one for your project:
    LOGGER.info("    Download 1000 rows of Airline flight paths")
    df = pd.read_csv(filepath_or_buffer=FILE_NAME,
                     encoding='latin-1',
                     nrows=1000
                    )

    # --- Specify name of file to be created on s3, to store this CSV:
    LOGGER.info(f"    Uploading file: {KEY_NAME_DATA} to S3 bucket = {BUCKET_NAME}")
    with s3_fs.open(f"{BUCKET_NAME}/{KEY_NAME_DATA}", "w") as file:
        df.to_csv(file)
    LOGGER.info(f"    Uploaded file: {KEY_NAME_DATA} to S3 bucket = {BUCKET_NAME}")

    LOGGER.info(f"List of objects in bucket {BUCKET_NAME} now:")
    for file in s3.Bucket(BUCKET_NAME).objects.all():
        LOGGER.info(f"    {file.key}")

    ### ---------------------------------------------------------------------------
    ### --- Part 3: Upload Model Object to S3 Bucket
    ### ---------------------------------------------------------------------------
    LOGGER.info("--- Part 3: Upload Model Object to S3 Bucket")

    LOGGER.info("    Loading RF model object")
    rf_dict = joblib.load("../Class4/rf.joblib")

    # --- Specify name of file to be created on s3, to store this model object:
    LOGGER.info(f"    Uploading file: {KEY_NAME_MODEL} to S3 bucket = {BUCKET_NAME}")
    with s3_fs.open(f"{BUCKET_NAME}/{KEY_NAME_MODEL}", "wb") as file:
        joblib.dump(rf_dict[500], file)
    LOGGER.info(f"    Uploaded file: {KEY_NAME_MODEL} to S3 bucket = {BUCKET_NAME}")

    LOGGER.info(f"List of objects in bucket {BUCKET_NAME} now:")
    for file in s3.Bucket(BUCKET_NAME).objects.all():
        LOGGER.info(f"    {file.key}")
