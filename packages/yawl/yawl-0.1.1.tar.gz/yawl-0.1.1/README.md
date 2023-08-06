# YAWL - Yet Another Workload
[
![Checks](https://github.com/gbieul/yawl/actions/workflows/yawl-checks.yml/badge.svg)
![Build](https://github.com/gbieul/yawl/actions/workflows/yawl-build.yml/badge.svg)
](https://pypi.org/project/flake8-markdown/)

## 1.0. Intro
YAWL - Yet Another WorkLoad is a tool to help you organize better [at least for now] your queries on BigQuery [only]. If you're working with scheduled queries, this tool is for you.

It intends to manage your repo organization, and to let you automate the process of updating your queries on BigQuery Data Transfer service.
## 2.0. Installing YAWL
You just have to do a `pip install yawl` and that's it! YAWL is published on PyPI.

## 3.0. Using YAWL
Let's say that you have the scheduled query `test_query101`, that runs on such schedule as `every mon,wed 09:00`, and that defines a table such as `myproject.mydataset.revenue_per_users` and that's represented by a SQL statement such as:

```SQL
SELECT username, SUM(revenue) AS revenue
FROM some_project.some_dataset.some_table
GROUP BY username
```

Then, things are going nice, but then you find that you have to add the user's e-mail also over the same query in order to generate the results. Now, you'd have a query like this:

```SQL
SELECT username, user_email, SUM(revenue) AS revenue
FROM some_project.some_dataset.some_table
GROUP BY username, user_email
```

If you don't have anything connected to your data transfer service, you'll need to:
1. Manually enter uder the scheduled query on the UI in order to change how it should behave;
2. Try to deploy again programatically the `test_query101` just to find out that BigQuery will now have two `test_query101`

Other possible problem is that you can't have a nice CI/CD process with this, in order to allow a good practice with other teammates reviewing your code, and automaticaly deploying it when approved.

Now, in order to use YAWL, you have two things to consider:
1. Creating the steps
```python
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
```
2. Creating the queue
```python
with queue() as q:
        q.add(step_1).add(step_2).process()
```
And that's it! The process method will be in charge of pushing your queries directly into BigQuery Data Transfer Service. You may note that the `sql` argument can have either a SQL statement, or a path to a SQL file.

And other cool thing is that if you're changing something over a SQL file, let's say, to update how a query should behave, and you just want to maintain the same scheduled query display name, well, you can! This way you can let your git maintain your queries history, this way if anything goes wrong you'll be able to rollback to an older commit.