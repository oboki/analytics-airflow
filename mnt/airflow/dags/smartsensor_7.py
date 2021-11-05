from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.hooks.filesystem import FSHook
from plugins.smart_file_sensor import SmartFileSensor
from airflow.operators.dummy_operator import DummyOperator

import logging
import json

default_args = {
    'start_date': days_ago(1),
}

@dag(schedule_interval='@daily', default_args=default_args, catchup=False)
def smartsensor_7():
    sensors = [
        SmartFileSensor(
            task_id=f'edw_d_000{sensor_id}',
            filepath=f'edw.000{sensor_id}.job',
            fs_conn_id='fs_default'
        ) for sensor_id in range(4, 5)
    ]

    @task
    def proccess_n_times():
        path = FSHook(conn_id='fs_default').get_path()
        logging.info(f'{path}/file.json')

    @task
    def finish():
        logging.info('storing data')
    
    start = DummyOperator(task_id='is_it_to_do_today')

    start >> sensors
    sensors >> proccess_n_times() >> finish()

dag = smartsensor_7()