# Project summary

## Project description
In this project, a extraction-transfer-load pipeline for a data warehouse is built on AWS Redshift. This project is quite similar to the first project (ETL with postgres), with the main difference being in the utilization of (potentially distributed) cloud infrastructure. In total, five tables should be created and populated using data from two different S3 sources:

1. songplays, a fact table listing who played which song by which artist at what time, extracted from log data
2. users, a dimension table containing user information like name and level, extracted from log data
3. songs, a dimension table containing song information like title and length, extracted from song data
4. artists, a dimension table containing artist information like name and location, extracted from song data
5. time, a dimension table that lists the units of time (hours, minutes etc.) for each timestamp in the fact table, extracted from log data

## Project files and running the project
The relevant files for submission are `sql_queries.py` and `iac_create_cluster.ipynb`. `create_tables.py` and `etl.py` were provided and not altered (except for adding docstrings). I split this project into two parts.

In the first part, the cloud infrastructure is created via IaC. For this, the Jupyter notebook `iac_create_cluster.ipynb` provides the necessary functions to *create* an IAM role and a Redshift cluster. Further, the notebook generates a file `dwh.cfg` which is used by the main scripts to identify the IAM arn and the cluster endpoint. The notebook also provides functions to *query* and *delete* the cluster. 

In the second part, once `dwh.cfg` has been created, the tables are created and the ETL job is executed with the provided Python scripts:
```
python create_tables.py
python etl.py
```

## Considerations for CREATE and INSERT statements
I made slight modifications compared to the first project (ETL with postgres):
* I chose `VARCHAR` and `NUMERIC` types that match the provided data (in terms of character length and precision) that was provided. 
* Two staging tables needed to be created to accomodate the data from the S3 buckets. Here, I chose values that match the types provided in the raw json logs. No restrictions for NULL values were imposed, as we want the complete picture of the available data at this stage.
* For the five final tables, distribution keys and sorting keys needed to be provided. The sorting key is usually the unique id of the given fact or dimension table row. For the distribution key, I decided that the time field makes the most sense, as distributing by time ensures an even distrbituion of data accross all nodes of the cluster, and from all dimension tables, the `time` table likely has the most rows. Therefore, the tables `songplays` and `time` follow the `KEY` distribution style.
* The `songplays` table cannot be extracted purely from event data, since it is missing the `song_id` and `artist_id` fields only present in song data. It is likely sufficient to join on song title and artist name. The song length could be used here as well, but might have different precisions in the two staging tables, which might prevent reasonable joins if not taken care of properly. 