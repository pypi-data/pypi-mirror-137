import airflow
from airflow import DAG
import traceback
from airflow.exceptions import (
    AirflowException,
    AirflowFailException,
    AirflowRescheduleException,
    AirflowSkipException,
    AirflowTaskTimeout,
)
from airflow.operators.email_operator import EmailOperator
from airflow.operators import BashOperator, PythonOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.models import Variable
from datetime import datetime, timedelta


class Email_Sender:

    def email_operator(self,context,template_name: str,  params: dict = {}):
        context = context
        etl_job_name = context["task_instance"].dag_id
        exception = context.get("exception")
        date_and_time = datetime.today() 
        params["etl_job_name"] = str(etl_job_name)
        params["exception"] = str(exception)
        params["date_and_time"] = str(date_and_time)
        html_content = Variable.get(template_name).format(**params)
        send_email = EmailOperator(
            trigger_rule=TriggerRule.ONE_FAILED,
            mime_charset="utf-8",
            task_id="t1Failed",
            to=[Variable.get("notification_email")],
            subject="IFS "
            + etl_job_name
            + " data pipeline failed - "
            + str(date_and_time),
            html_content=html_content,
        )

        send_email.execute(context=context)


# from novigi_common.utils.custom_error_emails import Email_Sender
#   params = {
#         "data_file_name": source_file,
#         "data_base_name": db_name
#     }
# Email_Sender.email_operator(context,"email_templates_db_connection_failure", params)


   