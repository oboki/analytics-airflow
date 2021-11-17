from datetime import datetime, timedelta

from airflow import DAG
from airflow.configuration import _default_config_file_path
from airflow.models import DagRun, DagBag, DagModel
from airflow.operators.python_operator import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.utils import timezone
from airflow.utils.state import DagRunState, State
from time import sleep

def _monitor():
    pass
    hook = MySqlHook(
        mysql_conn_id = 'airflow_db',
        database='airflow'
    )

    offset = timezone.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    while True:

        sql = """select btch_id
                      , base_dt
                      , frmw_chng_tmst
                   from btch_job_h
                  where frmw_chng_tmst > '{offset}'
                  order by frmw_chng_tmst
                 ;
              """.format(
                  offset=offset
              )
        print(sql)

        dags_to_run = hook.get_records(sql)

        for dag in dags_to_run:

            print(dag)

            dag_id = dag[0] # btch_id
            execution_date = datetime.strptime(dag[1], '%Y%m%d') # base_dt
            offset = dag[2].strftime('%Y-%m-%d %H:%M:%S') # frmw_chng_tmst

            dag_model = DagModel.get_current(dag_id)

            print("fileloc: ", dag_model.fileloc)
            dagbag = DagBag(
                dag_folder=dag_model.fileloc,
            )

            dag = dagbag.get_dag(dag_id)

            dag.create_dagrun(
                run_id="triggered_by_upstream_monitor__{}".format(
                    str(execution_date.strftime('%Y-%m-%dT%H:%M:%S'))
                ),
                execution_date=execution_date,
                state=DagRunState.QUEUED,
                external_trigger=True,
            )

        sleep(30)


with DAG(
    dag_id='upstream_monitor',
    schedule_interval='0 0 * * *',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['analytics'],
    default_args = {
        'owner': 'analytics'
    },
) as dag:

    t1 = PythonOperator(
        task_id='monitor',
        python_callable=_monitor,
        dag=dag
    )

    t1


if __name__ == "__main__":
    dag.cli()