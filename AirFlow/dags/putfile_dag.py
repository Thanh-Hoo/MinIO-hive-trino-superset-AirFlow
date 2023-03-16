import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.python import PythonSensor
from minio import Minio


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 8),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


dag = DAG(
    'put_new_object_to_minio',
    default_args=default_args,
    description='DAG for putting new object to MinIO',
    schedule_interval=timedelta(minutes=5),
)


def check_new_file_in_folder():
    path = '/path/to/folder' # đường dẫn đến thư mục cần theo dõi
    new_file = max(os.listdir(path), key=os.path.getctime) # tìm file mới nhất
    return new_file


def put_object_to_minio(**kwargs):
    # get the file path of the new object
    file_path = kwargs['task_instance'].xcom_pull(task_ids='check_new_file_in_folder')

    # create an instance of the Minio client
    minio_client = Minio(
        endpoint='localhost:9000',
        access_key='minioaccesskey',
        secret_key='miniosecretkey',
        secure=False
    )

    # upload the object to the MinIO bucket
    with open(file_path, 'rb') as file_data:
        file_stat = os.stat(file_path)
        minio_client.put_object(
            bucket_name='my-minio-bucket',
            object_name='path/to/destination/file/in/bucket',
            data=file_data,
            length=file_stat.st_size
        )


task_check_new_file = PythonSensor(
    task_id='check_new_file_in_folder',
    python_callable=check_new_file_in_folder,
    poke_interval=5,
    timeout=3600,
    dag=dag
)

task_put_object_to_minio = PythonOperator(
    task_id='put_object_to_minio',
    python_callable=put_object_to_minio,
    provide_context=True,
    dag=dag
)

task_check_new_file >> task_put_object_to_minio