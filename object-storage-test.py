from datetime import datetime
import os
import boto3
import json
from boto3.s3.transfer import TransferConfig

def main():
    # Setting parameters from the configuration file
    config = get_config()
    curr_dir = os.path.realpath(__file__)
    print(config["test_files_folder_name"])
    curr_dir = curr_dir.replace(str(os.path.basename(curr_dir)),'/'+ config['test_files_folder_name'] +'/')
    results_file_name = config['csv_results_file_name']
    bucket = config['bucket']
    # Get the connection and execute tests
    conn = get_connection()
    execute_tests(conn, curr_dir, results_file_name, bucket)


def get_config():
    with open('config.json') as config_file:
        return json.load(config_file)


def get_transfer_config():
    MB = 1024 ** 2
    return TransferConfig(multipart_threshold=get_config()['multipart_transfer_threshold_mb']*MB)


def get_connection():
    return boto3.client('s3',
                        region_name = get_config()['region_name'],
                        aws_access_key_id = get_config()['aws_access_key_id'],
                        aws_secret_access_key =  get_config()['aws_secret_access_key']
                        )


def execute_tests(conn, curr_dir, results_file_name, bucket):
    # Add header row to the results file
    f = open(results_file_name, 'a')
    f.write("filename,file_size_MB,upload_time,download_time, download_speed\n")
    f.close()
    # For each test file, execute upload and download tests, writing the file sizes and timings to the results file
    for filename in os.listdir(curr_dir):
        f = open(results_file_name, 'a')
        file_size = os.path.getsize(curr_dir + filename)
        # upload test
        upload_results = execute_upload_test(conn, curr_dir, filename, bucket)
        #start download test
        download_results = execute_download_test(conn, curr_dir, filename, bucket)
        # Write results to file
        f.write(str(filename) + "," + str(file_size/(1024 ** 2)) + "," + str(upload_results) + "," + str(download_results) + ',' + str((file_size/(1024 ** 2))/float(download_results)) + "\n")
        f.close()


def execute_upload_test(conn, curr_dir, filename, bucket):
    # Execute upload, saving the time taken by the operation
    dt_upload_init = datetime.now()
    conn.upload_file(curr_dir + filename, bucket, curr_dir + filename, Config=get_transfer_config())
    dt_upload_end = datetime.now()
    upload_time = dt_upload_end - dt_upload_init
    #Return the time as seconds.microseconds
    return '%02d.%d' % (upload_time.seconds, upload_time.microseconds)


def execute_download_test(conn, curr_dir, filename, bucket):
    # Execute download, saving the time taken by the operation
    dt_download_init = datetime.now()
    conn.download_file(bucket, curr_dir + filename, curr_dir + filename, Config=get_transfer_config())
    dt_download_end = datetime.now()
    download_time = dt_download_end - dt_download_init
    #Return the time as seconds.microseconds
    return '%02d.%d' % (download_time.seconds, download_time.microseconds)


if __name__ == "__main__":
    main()




