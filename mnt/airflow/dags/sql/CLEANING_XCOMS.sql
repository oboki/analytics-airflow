DELETE 
FROM xcom 
WHERE dag_id='partner'
AND execution_date='{{ macros.ds_format(ts, "%Y-%m-%dT%H:%M:%S+00:00", "%Y-%m-%d %H:%M:%S+00:00") }}'