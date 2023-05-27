# custom-utils
Pip Package for Database Connectors, Alerter, Log Formatter etc


***

<p float="left">
  <img src=https://img.shields.io/pypi/v/custom-utils />
  <img src=https://www.code-inspector.com/project/29426/score/svg />
  <img src=https://img.shields.io/pypi/dm/custom-utils?logo=Python&style=social /> 
  <a href="https://github.com/RahulnKumar/custom-utils/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/RahulnKumar/custom-utils"></a>
</p>
 

## Table of Contents

- [custom-utils](#custom-utils)
  - [Table of Contents](#table-of-contents)
  - [1.  Installation](#1--installation)
  - [2. Connector](#2-connector)
    - [1. S3 Connector](#1-s3-connector)
    - [2. MySQL Connector](#2-mysql-connector)
    - [3.  MongoDB Connector](#3--mongodb-connector)
    - [4.  BigQuery Connector](#4--bigquery-connector)
  - [3. Configurer](#3-configurer)
    - [1. Profile Decorator](#1-profile-decorator)
    - [2.  Log Formatter](#2--log-formatter)
  - [4. Alerter](#4-alerter)
    - [1.  Slack Alerter](#1--slack-alerter)

***

## 1.  Installation<a id="1--installation">    

- **Installation from Pypi repository** (Any one)
	
    `pip install custom-utils`  --> minimal installation  
    `pip install custom-utils[full]` --> full installation  
    `pip install custom-utils[s3,mysql,bigquery,mongodb,slack]`  --> selective installation 
- **Installation from github repository** (Any one)  
	
    `pip install git+https://github.com/rahulnkumar/custom-utils.git`  
    `pip install git+https://github.com/rahulnkumar/custom-utils.git@<tag_no>`  
    `pip install git+https://github.com/rahulnkumar/custom-utils.git@<branch_name>`    

<img src="https://i.ibb.co/WHwqTpr/pip-cu.gif" alt="pip-cu" border="0">
    
---
    
	
## 2. Connector<a id="2-connector">

    
### 1. S3 Connector<a id="1-s3-connector">     

**Code Snippet Sample :**
```python
## To use S3 either setup AWS CLI or set the credentials from pip package only

## Setup AWS CLI
sudo apt install awscli && aws configure

## Setup Credentials from pip package
from custom_utils.configurer.utils import Credential
Credential.set(ACCESS_KEY="*********", SECRET_KEY="*********")


from custom_utils.connector.s3 import S3

# Uplaoding data to S3
S3.push_local_data(file_path, s3_uri)
                             
# Doownlaoding data from S3
S3.pull_s3_data(file_path, s3_uri)
```

**S3 Connector Documentation**
    
```
class S3(builtins.object)
 |  AWS S3 utility functions
 |  
 |  Static methods defined here:
 |  
 |  pull_python_object(s3_uri)
 |      read python object stored in S3 bucket
 |      :param string s3_uri: s3 uri of the object
 |      :return python_object : python object stored in the S3
 |  
 |  pull_s3_data(file_path, s3_uri)
 |      write data stored in local machine into S3 bucket from
 |      :param string s3_uri: target s3 uri
 |      :param string file_path:  local path of the file 
 |      :return None
 |  
 |  push_local_data(file_path, s3_uri)
 |      write data stored in local machine into S3 bucket from
 |      :param string s3_uri: target s3 uri
 |      :param string file_path:  local path of the file 
 |      :return None
 |  
 |  push_python_object(python_object, s3_uri)
 |      write python objects/variables etc  into S3 bucket
 |      :param string bucket: bucket name
 |      :param string sub_bucket: sub-bucket name
 |      :param string file_name: name of the file to be written
 |      :return None
 |  
 |  read_csv(s3_uri)
 |      write data stored in local machine into S3 bucket from
 |      :param string s3_uri: csv file S3 URI
 |      :return df : pandas dataframe
 |  
 |  ----------------------------------------------------------------------
  
```
---
    

---
   
### 2. MySQL Connector<a id="2-mysql-connector">  
  
**Code Snippet Sample :**  
```python
# Query from Custom MySQL Database
from custom_utils.connector.mysql import MySQL 
user = "***"
password = "***"
host = "***"
port = "***"
database = "***"
db_string = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
query = "select * from table_name limit 10"
mysql = MySQL(db_string=db_string)
df = mysql.pull_data(query = query) 
```
    
**MySQL Connector Documentaion**
```
class MySQL(builtins.object)
 |  MySQL(db_string)
 |  
 |  MySQL database utility functions
 |  
 |  Methods defined here:
 |  
 |  __init__(self, db_string)
 |      initialisation method for MySQL Connector
 |      :param string db_string: mysql database connection string
 |  
 |  push_data(self, data, table_name, mode='append')
 |      Execute a query in the mysql table
 |      :param pd.DataFrame data: dataframe to be appended or replaced
 |      :param string table_name: name of the the target table
 |      :param string mode: it can be either replace or append
 |      :return None
 |  
 |  execute_query(self, query)
 |      Execute a query in the mysql table
 |      :param string query: query for execution in the table
 |      :return :
 |  
 |  pull_data(self, query)
 |      Fetch data from mysql as a dataframe.
 |      :param string query: query for fetching data from table
 |      :return pd.DataFrame data
```
    
---
    
    
### 3.  MongoDB Connector<a id="3--mongodb-connector">
    
**Code Snippet Sample :**  
```python
from custom_utils.connector.mongodb import MongoDB
uri = "****"
db = "***"
collection = "****"
mongo = MongoDb(uri = uri, db = db)

#Reading with pull method
data =  mongo.pull_data(collection=collection, list_dict=list_dict)

# Reading with fetch method
query = {'id': {'$in': [1,2]}}
data = mongo.fetch_data(collection, query=query, only_include_keys=["name"])

#Writing into MongoDB
mongo.push_data(collection = collection, data = data)

#Updating value
id_dict = {"id":"2"}
set_dict = {"$set": {"name":"ram"}}
mongo.update_value(id_dict, set_dict,collection=collection, upsert=True)

# Deleting data
mongo.delete_data(collection=collection, overall=False, condition_dict= {"id":None})

```

 **MongoDB Connector Documentaion**
```    
class MongoDB(builtins.object)
 |  MongoDB(db=None, uri=None)
 |  
 |  MongoDB utility functions.
 |  
 |  Methods defined here:
 |  
 |  __init__(self, db=None, uri=None)
 |      initialisation method for MongoDB connector
 |      :param str db: database name
 |      :param str uri: mongo uri string for establishing connection
 |  
 |  delete_data(self, collection, db=None, overall=False, condition_dict=None)
 |      Function for inserting data into db
 |      :param str db : database name
 |      :param str collection : collection name
 |      :param bool overall : delete whole collection if True
 |      :param dict condition_dict : query for deletion
 |      :return:
 |  
 |  fetch_data(self, collection, db=None, query={}, only_include_keys=[])
 |      function to fetch data from the given database and collection on given query
 |      :param str db : db_name in mongo
 |      :param str collection: collection name in mongo for database db
 |      :param dict query : execution query statement; default is {} which means fetch
 |                         all without any filters
 |      :param list only_include_keys : list of keys to be included while fetching rows
 |      :return: pd.DataFrame
 |  
 |  fetch_data_sorted(self, collection, db=None, pipeline=[])
 |      function to fetch data from the given database and collection on given query
 |      :param str db: db_name in mongo
 |      :param str collection: collection name in mongo for database db
 |      :param list pipeline: pipeline required to aggregate
 |      :return: pd.DataFrame
 |  
 |  pull_data(self, list_dict, collection, db=None)
 |      Function for inserting data into db
 |      :param str db : database name
 |      :param str collection : collection name
 |      :param list list_dict : query for fetching data
 |      :return: pd.DataFrame
 |  
 |  push_data(self, data, collection, db=None)
 |      Function for inserting data into db
 |      :param str db : database name
 |      :param str collection : collection name
 |      :param list/pd.DataFrame data : data to be inserted in the form of
 |                                      dataframe or list of dictionaries
 |      :return:
 |  
 |  update_value(self, id_dict, set_dict, collection, db=None, upsert=None)
 |      Function for updating data into db
 |      :param str db : database name
 |      :param str collection : collection name
 |      :param dict id_dict : query for updation
 |      :param dict set_dict : key and value dictionary to be updated
 |      :param bool upsert : whether to upsert or just update
 |      :return:
 |  
 |  upsert_json(self, output_json, upsert_keys, collection, db=None)
 |      Function for inserting data into db
 |      :param str db : database name
 |      :param str collection : collection name
 |      :param dict output_json : list of dictionaries where each dictionary is
 |                                a row with keys as column names
 |      :param list upsert_keys : keys to be upserted
 |      :return:
 |  
 |  ----------------------------------------------------------------------
```
---
	
### 4.  BigQuery Connector<a id="4--bigquery-connector">
    
**Code Snippet Sample :**  
```python

# Fetching data from BigQuery
from custom_utils.connector.bigquery import BigQuery
bq = BigQuery(read_big_query_project = "****",
                    service_account_file_path="***.json")
query = "select * from table_name"
df = bq.pull_data(query)

# Dumping Dataframe in BigQuery
bq.push_data(database="rahul_temp", table="demo", dataframe=df, mode="append")

# Executing any query in BigQuery
query = "INSERT rahul_temp.Demo (id, userId) VALUES(1,1),(1,1)"
BigQuery.execute_query(query)

# Streaming insert in BigQuery
row_to_insert = [{"id": 1, "userid": 1, "languageId": 58,
             "mode":0,"active":1}]
BigQuery.insert_rows_in_bigquery(dataset="rahul_temp", table="Demo", rows_to_insert=row_to_insert)

```
    
**BigQuery Connector Documentaion**
```
class BigQuery(builtins.object)
 |  BigQuery(read_big_query_project, write_big_query_project, service_account_file_path)
 |  
 |  BigQuery database utility functions
 |  
 |  Methods defined here:
 |  
 |  __init__(self, read_big_query_project, write_big_query_project, service_account_file_path)
 |      initialisation method for BigQuery Connector
 |      :param str read_big_query_project : project used while reading from BigQuery
 |      :param str write_big_query_project: project used while writing into BigQuery
 |      :param str service_account_file_path: project specific BigQuery Credential
 |  
 |  push_data(self, database=None, table=None, dataframe=None, mode='append')
 |      Dumps data into from BigQuery
 |      :param string database: target bigquery database
 |      :param string table: target table name
 |      :param pd.DataFrame dataframe: pandas dataframe for dumping into bigquery
 |      :param string mode: it can be either append or replace
 |  
 |  execute_query(self, query, job_config=None, timeout=900, max_retries=0, time_interval=5)
 |      Executes query from from BigQuery table
 |      :param string query: query for execution
 |      :param string query_cofig: config for parameterised query
 |      :param integer timeout : maximum bigquery execution timeout
 |      :param string max_retries: maximum retries if data is not fetched
 |      :param integer time_interval : time interval between retries
 |  
 |  pull_data(self, query=None, job_config=None, max_retries=0, time_interval=5)
 |      Fetches data from from BigQuery
 |      :param string query: query for fetching data from table
 |      :param string query_cofig: config for parameterised query
 |      :param string max_retries: maximum retries if data is not fetched
 |      :param integer time_interval : time interval between retries
 |  
 |  insert_rows_array(self, dataset=None, table=None, rows_to_insert=None)
 |      Streaming insert into from BigQuery
 |      :param string dataset: target bigquery database
 |      :param string table: target table name
 |      :param list rows_to_insert: list of dictionaries where each dictionary is a
 |                                  row with keys as column names
 |  
 |  insert_rows_in_bigquery(self, dataset=None, table=None, rows_to_insert=None)
 |      Streaming insert into from BigQuery
 |      :param string dataset: target bigquery database
 |      :param string table: target table name
 |      :param  rows_to_insert: list of dictionaries where each dictionary is a
 |                              row with keys as column names
```
---
	
	
## 3. Configurer<a id="3-configurer">   
	
### 1. Profile Decorator<a id="1-profile-decorator">    
    
**Code Snippet Sample :**  
```python
from custom_utils.configurer.profiler import profiler
@profiler(sort_by='cumulative', lines_to_print=10, strip_dirs=True)
def product_counter_v3():
    return [1, 2, 3, 4, 5]
```
**Profiler Documentaion**
```python
def profiler(output_file=None, sort_by='cumulative', lines_to_print=None, strip_dirs=False):
    """
    A time profiler decorator

    :param str output_file: Path of the output file. If only name of the file is given, it's saved in the current
    directory. If it's None, the name of the decorated function is used.
    :param str sort_by: SortKey enum or tuple/list of str/SortKey enum Sorting criteria for the Stats object. For a list
    of valid string and SortKey refer to: https://docs.python.org/3/library/profile.html#pstats.Stats.sort_stats
    :param int lines_to_print: Number of lines to print. Default (None) is for all the lines. This is useful in reducing
    the size of the printout, especially that sorting by 'cumulative', the time consuming operations are printed toward
    the top of the file.
    :param bool strip_dirs: Whether to remove the leading path info from file names. This is also useful in reducing the
    size of the printout
    :return: Profile of the decorated function
    """
```
###  2.  Log Formatter<a id="2--log-formatter">
 
**Code Snippet Sample :**
```python
from custom_utils.configurer.utils import LogFormatter
LogFormatter.apply()
```
    
**Log Formatter Documentation**
```
class LogFormatter(logging.Formatter):
    """Log Formatter class for custom-utils package"""

    __date_format = '%d/%b/%Y:%H:%M:%S %Z'

    @staticmethod
    def apply(level=logging.INFO):
        """
        Start logging in json format.
        :return:
```
---
	
	
## 4. Alerter<a id="4-alerter">    
	
###  1.  Slack Alerter<a id="1--slack-alerter">  
    
    
**Code Snippet Sample :**
```python3
from custom_utils.alerter.slack import Slack
slack = Slack(token=SLACK_BOT_TOKEN) # OR Slack() with  SLACK_BOT_TOKEN as env variable
channel="#shield"
message = "testing"
uids = ["U03PAP8C1RC", "U03PAP8C1RC"]
slack.send_alert(channel, message, uids)
```
    
**Alerter Documentation :**
```python
class Slack(builtins.object)
 |  Slack(token=None)
 |
 |  Class for sending alerts and monitoring stats to a slack channel
 |
 |  Methods defined here:
 |
 |  __init__(self, token=None)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |
 |  send_alert(self, channel: str, message: str, uids: list = [])
 |      This function send alert to a target channel tagging a user
 |                          with a alert message and traceback error.
 |      args:
 |          channel     : Name of the channel (ex : #channel_name)
 |          message     : Pass the message to be displayed in the channel
 |          uids        : List of Slack user_ids  who needs to be tagged
 |
 |      returns: Nothing
 |
 |  ----------------------------------------------------------------------
```
---
