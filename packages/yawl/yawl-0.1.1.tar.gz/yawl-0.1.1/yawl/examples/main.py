"""This module is a simple example of how to use YAWL.
You essencially have to:
- Add the workflow steps, defining either an
sql command or a path to a sql file, the destination table,
the scheduled query name, and the definition of the schedule;

- Create a queue, adding the steps you want to create a
dependency;

- Call the process method in order to add or update the queries.
"""
from yawl.workflows.bigquery_workflow import BigQueryWorkflowStep
from yawl.workflows.queue import queue

if __name__ == "__main__":
    step_1 = BigQueryWorkflowStep(
        sql="./sql_files/example.sql",
        dest_table="google_cloud_project_id.transfer_test.table_1",
        squeduled_query_name="test_query101",
        schedule="every mon,wed 09:00",
    )
    step_2 = BigQueryWorkflowStep(
        sql="./sql_files/example.sql",
        dest_table="google_cloud_project_id.transfer_test.table_2",
        squeduled_query_name="test_query_102",
        schedule="every tue,thu 10:00",
    )
    with queue() as q:
        q.add(step_1).add(step_2).process()
