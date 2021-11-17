from datetime import datetime, timedelta
from airflow import DAG
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.dummy import DummyOperator

default_args = {
}

with DAG(
    dag_id='crm_d_0001', 
    schedule_interval='0 0 * * *',
    default_args={
        'owner': 'analytics',
        'start_date': datetime(2021, 1, 1)
    }
) as dag:

    is_it = DummyOperator(
        task_id='is_it_to_do_today'
    )

    run_job = DummyOperator(
        task_id='run_job_maybe_n_times'
    )

    done = DummyOperator(
        task_id='done'
    )

    for i in range(1,4):
        sensor = ExternalTaskSensor(
            task_id='wait_for_upstream_edw_d_000{}'.format(str(i)),
            external_dag_id='edw_d_000{}'.format(str(i)),
            external_task_id='done',
            execution_date_fn=(
                lambda x: x.replace(
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0
                ) # + timedelta(hours=9)
            ),
            mode='reschedule',
            timeout=3600,
        )

        is_it >> sensor >> run_job
    
    run_job >> done