from datetime import datetime
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.models import Variable

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2021, 1, 1),
    'retries': 0
}

dag = DAG(
    'quiz_recommand',
    default_args=default_args,
    description='DAG for quiz recommand model',
    schedule_interval=None,
    catchup=False,
    tags=['quiz_recommand'],
)

with dag:
    run_train_task = KubernetesPodOperator(
        task_id='run_train',
        name='quiz_recommand',
        namespace='airflow',
        image='012634413971.dkr.ecr.ap-northeast-2.amazonaws.com/task/recommand:latest',  # 미리 패키지를 설치한 이미지
        image_pull_secrets='ecr-credentials',
        cmds=['python'],
        env_vars={
            's3_endpoint_url': Variable.get('s3_endpoint_url'),
            'aws_access_key_id': Variable.get('aws_access_key_id'),
            'aws_secret_access_key': Variable.get('aws_secret_access_key'),
            's3_bucket_name': Variable.get('s3_bucket_name'),
            'mlflow_server': Variable.get('mlflow_server'),
            'mlflow_server': Variable.get('mlflow_server'),
            'mlflow_server': Variable.get('mlflow_server'),
            'MYSQL_HOST':  Variable.get('MYSQL_HOST'),
            'MYSQL_USER':  Variable.get('MYSQL_USER'),
            'MYSQL_PASSWORD':  Variable.get('MYSQL_PASSWORD'),
            'MYSQL_DATABASE':  Variable.get('MYSQL_DATABASE'),
            'MYSQL_PORT':  Variable.get('MYSQL_PORT'),
            'REDIS_HOST':  Variable.get('REDIS_HOST'),
            'REDIS_PORT':  Variable.get('REDIS_PORT'),
            'REDIS_PASSWORD':  Variable.get('REDIS_PASSWORD'),
        },
        is_delete_operator_pod=True,
        in_cluster=True,
        get_logs=True,
        dag=dag,
    )

    run_train_task