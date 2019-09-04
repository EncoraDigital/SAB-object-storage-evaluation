# Object storage evaluation

This test was designed to measure the bandwidth of S3 compatible solutions from the perspective of a normal user, downloading one file at a time.

Parameters, as well as fields for credentials,  are is available in the file *config.json*. 

To execute this test, simply add a folder containing test files to this directory, and set the parameter *test_files_folder_name* to be equal to the name of the folder. 

Upon execution of the script, all files located in the folder will be uploaded and then downloaded from the chosen bucket, and results will be saved to a file with the name specified in the parameter *csv_results_file_name*.

To connect with Ceph instead of S3, just add the following parameters to the *get_connection* method of the test:

```
            endpoint_url='your_rados_gw_endpoint:7480',
            use_ssl=False)
``````