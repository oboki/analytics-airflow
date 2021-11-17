from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime


def create_dag(
    dag_id,
    default_args
):

    dag = DAG(
        dag_id,
        schedule_interval=None,
        default_args=default_args
    )

    with dag:
        upstream = DummyOperator(
            task_id='done'
        )

    return dag


for n in range(1,10):
    dag_id = 'edw_d_000{}'.format(str(n))
    default_args = {
        'owner': 'analytics',
        'start_date': datetime(2021, 1, 1)
    }

    globals()[dag_id] = create_dag(
        dag_id,
        default_args
    )