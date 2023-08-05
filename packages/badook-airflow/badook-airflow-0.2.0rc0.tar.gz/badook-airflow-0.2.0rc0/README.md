# badook Airflow

## Dag code example:

```
from airflow import DAG
from airflow.utils.dates import days_ago

from badook_airflow.operators.badook_operator import BadookTestOperator


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0)
}

with DAG(
    dag_id='badook_test_runner',
    default_args=default_args,
    schedule_interval='@once'
) as dag:
    badook_test = BadookTestOperator(
        target_directory='test_dir',
        data_cluster_url='https://test.url',
        management_cluster_url='https://test.managment.url',
        client_id='APIKEY',
        client_secret='SECRETKEY',
        task_id="run_tests"
    )
    badook_test
```
