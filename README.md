# utilities
Pip Package for Database Connectors, Alerter, Log Formatter etc


***

<p float="left">
  <img src=https://img.shields.io/pypi/v/trell-ai-utils />
  <img src=https://img.shields.io/pypi/dm/trell-ai-utils?logo=Python&style=social /> 
</p>
 

## Table of Contents

- [Installation](#Installation)
- Connector
  - [S3 Connector](#S3_Connector)
  - [MySQL Connector](#MySQL_Connector)
  - [MongoDB Connector](#MongoDB_Connector)
  - [BigQuery Connector](#BigQuery_Connector)
 
- Configurer
  - [Log Formatter](#Log_Formatter)
  - [Profile Decorator](#Profile_Decorator)
  
- Alerter
  - [Slack Alerter](#Slack_Alerter)

***

## 1.  Installation<a id="Installation" name="Installation">    

- **Installation** (Any one)      
    `pip install utilities`  
    `pip install git+https://github.com/rahulnkumar/utilities.git`  
    `pip install git+https://github.com/rahulnkumar/utilities.git@<tag_no>`  
    `pip install git+https://github.com/rahulnkumar/utilities.git@<branch_name>`    
    
---
    
	
## 1. Connector  

    
### 1. S3 Connector<a id="S3_Connector" name="S3_Connector">     

**Code Snippet Sample :**
```python
from utilities.connector.S3 import S3

# Uplaoding data to S3
demo = {"Name": "Trell", "Age": 4}
S3.write_to_s3_bucket(python_data_object=demo,
                             bucket='data-science-datas',
                             sub_bucket='models/', file_name="demo.pickle")
                             
# Doownlaoding data from S3

demo = S3.read_from_s3_bucket(bucket='data-science-datas',          
                                         sub_bucket='models/',
                                         file_name="demo.pickle")
```

**S3 Connector Documentation**
    
```
```
---
    

---
   
### 2. MySQL Connector<a id="MySQL_Connector" name="MySQL_Connector">  
  
**Code Snippet Sample :**  
```python
# Query from Custom MySQL Database
from utilities.connector.mysql import MySQL 
user = "***"
password = "***"
host = "***"
port = "***"
database = "***"
db_string = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
query = "select * from table_name limit 10"
mysql = MySQL(db_string=db_string)
df = mysql.get_data(query = query) 
```
    
**MySQL Connector Documentaion**
```
```
    
---
    
    
### 3.  MongoDB Connector<a id="MongoDB_Connector" name="MongoDB_Connector">
    
**Code Snippet Sample :**  
```python
from utilities.connector.mongodb import MongoDB
uri = "****"
db = "***"
collection = "****"
mongo = MongoDb(uri = uri, db = db)

#Reading with pull method
data =  mongo.pull_data(collection=collection, list_dict=list_dict)

# Reading with fetch method
query = {'id': {'$in': [1,2]}}
data = mongo.fetch_data(collection, query=query, only_include_keys=["name"])

#Writing inot MongoDB
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
```
---
	
### 4.  BigQuery Connector<a id="BigQuery_Connector" name="BigQuery_Connector">
    
**Code Snippet Sample :**  
```python

# Fetching data from BigQuery
from utilities.connector.bigquery import BigQuery
bq = BigQuery(read_big_query_project = "****",
                    service_account_file_path="***.json")
query = "select * from `trellatale.trellDbDump.userLanguages` limit 2"
df = bq.get_data(query)

# Dumping Dataframe in BigQuery
bq.dump_data(database="rahul_temp", table="demo", dataframe=df, mode="append")

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
```
---
	
	
## 2. Configurer    
	
### 1. Profile Decorator<a id="Profile_Decorator" name="Profile_Decorator">    
    
**Code Snippet Sample :**  
```python
from utilities.configurer.profiler import profiler
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
###  2.  Log Formatter<a id="Log_Formatter" name="Log_Formatter">
 
**Code Snippet Sample :**
```python
from utilities.configurer.utils import LogFormatter
LogFormatter.apply()
```
    
**Log Formatter Documentation**
```
class LogFormatter(logging.Formatter)
 |  LogFormatter(fmt=None, datefmt=None, style='%', validate=True)
 |  
 |  Log Formatter class
 |  
 |  Method resolution order:
 |      LogFormatter
 |      logging.Formatter
 |      builtins.object
 |  
 |  Methods defined here:
 |  
 |  formatException(self, execution_info)
 |      Handle logging in case of exceptions.
 |      :param execution_info:
 |      :return:
 |  
 |  ----------------------------------------------------------------------
 |  Static methods defined here:
 |  
 |  apply(level=20)
 |      Start logging in json format.
 |      :return:
 |  
 |  ----------------------------------------------------------------------
 |  Methods inherited from logging.Formatter:
 |  
 |  __init__(self, fmt=None, datefmt=None, style='%', validate=True)
 |      Initialize the formatter with specified format strings.
 |      
 |      Initialize the formatter either with the specified format string, or a
 |      default as described above. Allow for specialized date formatting with
 |      the optional datefmt argument. If datefmt is omitted, you get an
 |      ISO8601-like (or RFC 3339-like) format.
 |      
 |      Use a style parameter of '%', '{' or '$' to specify that you want to
 |      use one of %-formatting, :meth:`str.format` (``{}``) formatting or
 |      :class:`string.Template` formatting in your format string.
 |      
 |      .. versionchanged:: 3.2
 |         Added the ``style`` parameter.
 |  
 |  format(self, record)
 |      Format the specified record as text.
 |      
 |      The record's attribute dictionary is used as the operand to a
 |      string formatting operation which yields the returned string.
 |      Before formatting the dictionary, a couple of preparatory steps
 |      are carried out. The message attribute of the record is computed
 |      using LogRecord.getMessage(). If the formatting string uses the
 |      time (as determined by a call to usesTime(), formatTime() is
 |      called to format the event time. If there is exception information,
 |      it is formatted using formatException() and appended to the message.
 |  
 |  formatMessage(self, record)
 |  
 |  formatStack(self, stack_info)
 |      This method is provided as an extension point for specialized
 |      formatting of stack information.
 |      
 |      The input data is a string as returned from a call to
 |      :func:`traceback.print_stack`, but with the last trailing newline
 |      removed.
 |      
 |      The base implementation just returns the value passed in.
 |  
 |  formatTime(self, record, datefmt=None)
 |      Return the creation time of the specified LogRecord as formatted text.
 |      
 |      This method should be called from format() by a formatter which
 |      wants to make use of a formatted time. This method can be overridden
 |      in formatters to provide for any specific requirement, but the
 |      basic behaviour is as follows: if datefmt (a string) is specified,
 |      it is used with time.strftime() to format the creation time of the
 |      record. Otherwise, an ISO8601-like (or RFC 3339-like) format is used.
 |      The resulting string is returned. This function uses a user-configurable
 |      function to convert the creation time to a tuple. By default,
 |      time.localtime() is used; to change this for a particular formatter
 |      instance, set the 'converter' attribute to a function with the same
 |      signature as time.localtime() or time.gmtime(). To change it for all
 |      formatters, for example if you want all logging times to be shown in GMT,
 |      set the 'converter' attribute in the Formatter class.
 |  
 |  usesTime(self)
 |      Check if the format uses the creation time of the record.
 |  
 |  ----------------------------------------------------------------------
 |  Static methods inherited from logging.Formatter:
 |  
 |  converter = localtime(...)
 |      localtime([seconds]) -> (tm_year,tm_mon,tm_mday,tm_hour,tm_min,
 |                                tm_sec,tm_wday,tm_yday,tm_isdst)
 |      
 |      Convert seconds since the Epoch to a time tuple expressing local time.
 |      When 'seconds' is not passed in, convert the current time instead.
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors inherited from logging.Formatter:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
 |  
 |  ----------------------------------------------------------------------
 |  Data and other attributes inherited from logging.Formatter:
 |  
 |  default_msec_format = '%s,%03d'
 |  
 |  default_time_format = '%Y-%m-%d %H:%M:%S'
```
---
	
	
## 3. Alerter    
	
###  1.  Slack Alerter<a id="Slack_Alerter" name="Slack_Alerter">  
    
    
**Code Snippet Sample :**
```
from utilities.slack_alerter import Alerter
try:
    """Write your code"""
except:
    """Catch exceptions"""
    Alerter.send_alert(message=message, url=url, userId=userId, send_error=True) 
```
    
**Alerter Documentation :**
```python
class Alerter(builtins.object)
     |  Class for sending alerts and monitoring stats to a slack channel
     |  
     |  Static methods defined here:
     |  
     |  send_alert(message: str, url: str, user_id: str = None, send_error: bool = False)
     |      This function send alert to a target channel tagging a user
     |                         with a alert message and traceback error.
     |      args:
     |              message     : Pass the message to be displayed in the channel
     |              url         : Pass webhook of target channel
     |              user_id     : Slack user_id of user who needs to be tagged (
     |              send_error  : This should be set True,
     |                           if slack_alert is called while catching exception
     |      returns: Nothing
     |  
     |  send_monitoring_stats(start: tuple, stop: tuple, message: str, url: str, user_id: str = None)
     |      This function send run time and RAM usage for a cronjob
     |      to a target channel tagging a user with a  message
     |      
     |      Args:
     |              message : Pass the message to be displayed in the channel
     |              url : Pass webhook of target channel
     |              user_id : Slack user_id of user who needs to be tagged
     |              start : this should be set to output of start_monitoring function
     |              stop : this should be set to output of start_monitoring function
     |  
     |  start_monitoring()
     |      function for initiating monitoring
     |  
     |  stop_monitoring()
     |      function for end monitoring
     |  
     |  ----------------------------------------------------------------------
```
---
