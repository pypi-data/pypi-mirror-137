# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yawl', 'yawl.clients', 'yawl.examples', 'yawl.shared', 'yawl.workflows']

package_data = \
{'': ['*'], 'yawl.examples': ['sql_files/*']}

install_requires = \
['google-cloud-bigquery-datatransfer>=3.3.1,<4.0.0',
 'google-cloud-bigquery-storage==2.0.0',
 'google-cloud-bigquery>=2.6.0,<3.0.0',
 'numpy>=1.22.2,<2.0.0',
 'pandas>=1.3.2,<2.0.0',
 'pytest-xdist>=2.3.0,<3.0.0']

setup_kwargs = {
    'name': 'yawl',
    'version': '0.1.1',
    'description': 'Yet Another WorkLoad - manage scheduled queries [currently] on BigQuery',
    'long_description': '# YAWL - Yet Another Workload\n[\n![Checks](https://github.com/gbieul/yawl/actions/workflows/yawl-checks.yml/badge.svg)\n![Build](https://github.com/gbieul/yawl/actions/workflows/yawl-build.yml/badge.svg)\n](https://pypi.org/project/flake8-markdown/)\n\n## 1.0. Intro\nYAWL - Yet Another WorkLoad is a tool to help you organize better [at least for now] your queries on BigQuery [only]. If you\'re working with scheduled queries, this tool is for you.\n\nIt intends to manage your repo organization, and to let you automate the process of updating your queries on BigQuery Data Transfer service.\n## 2.0. Installing YAWL\nYou just have to do a `pip install yawl` and that\'s it! YAWL is published on PyPI.\n\n## 3.0. Using YAWL\nLet\'s say that you have the scheduled query `test_query101`, that runs on such schedule as `every mon,wed 09:00`, and that defines a table such as `myproject.mydataset.revenue_per_users` and that\'s represented by a SQL statement such as:\n\n```SQL\nSELECT username, SUM(revenue) AS revenue\nFROM some_project.some_dataset.some_table\nGROUP BY username\n```\n\nThen, things are going nice, but then you find that you have to add the user\'s e-mail also over the same query in order to generate the results. Now, you\'d have a query like this:\n\n```SQL\nSELECT username, user_email, SUM(revenue) AS revenue\nFROM some_project.some_dataset.some_table\nGROUP BY username, user_email\n```\n\nIf you don\'t have anything connected to your data transfer service, you\'ll need to:\n1. Manually enter uder the scheduled query on the UI in order to change how it should behave;\n2. Try to deploy again programatically the `test_query101` just to find out that BigQuery will now have two `test_query101`\n\nOther possible problem is that you can\'t have a nice CI/CD process with this, in order to allow a good practice with other teammates reviewing your code, and automaticaly deploying it when approved.\n\nNow, in order to use YAWL, you have two things to consider:\n1. Creating the steps\n```python\nstep_1 = BigQueryWorkflowStep(\n    sql="./sql_files/example.sql",\n    dest_table="google_cloud_project_id.transfer_test.table_1",\n    squeduled_query_name="test_query101",\n    schedule="every mon,wed 09:00",\n)\nstep_2 = BigQueryWorkflowStep(\n    sql="./sql_files/example.sql",\n    dest_table="google_cloud_project_id.transfer_test.table_2",\n    squeduled_query_name="test_query_102",\n    schedule="every tue,thu 10:00",\n)\n```\n2. Creating the queue\n```python\nwith queue() as q:\n        q.add(step_1).add(step_2).process()\n```\nAnd that\'s it! The process method will be in charge of pushing your queries directly into BigQuery Data Transfer Service. You may note that the `sql` argument can have either a SQL statement, or a path to a SQL file.\n\nAnd other cool thing is that if you\'re changing something over a SQL file, let\'s say, to update how a query should behave, and you just want to maintain the same scheduled query display name, well, you can! This way you can let your git maintain your queries history, this way if anything goes wrong you\'ll be able to rollback to an older commit.',
    'author': 'Gabriel Benvegmi',
    'author_email': 'gbieul_benveg@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gbieul/yawl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
