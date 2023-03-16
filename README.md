## Get things running
1. Clone repo
2. Install docker + docker-compose
3. Run `docker-compose up -d`
4. Run `bash superset_init.sh`
4. Done! Checkout the service endpoints:

Trino: `http://localhost:8080/ui/` (username can be anything) <br>
Minio: `http://localhost:9001/` (username: `minio_access_key`, password: `minio_secret_key`)<br>
Superset: `http://localhost:8088/` (username: `admin`, password: `admin`)<br>
AirFlow: `https://localhost:9090/` (username: `admin`, password: `airflow`)<br>

## Connect to Trino in Superset:
1. Go to `data` dropdown and click `databases`
2. Click the `+ database` button
3. For `Select a database to connect` choose `presto`
4. In `SQLALCHEMY URI` put `trino://hive@trino-coordinator:8080/hive`
5. Switch over to `Advanced` tab
5. In `SQL Lab` select all options
5. In `Security` select `Allow data upload`

## Trino CLI

```
docker exec -it trino-hive-superset-docker_trino-coordinator_1 trino
```
Upload parquet file on MinIO bucket datalake and run commands:
```
CREATE SCHEMA IF NOT EXISTS hive.LPD_datasets_metadata
WITH (location = 's3a://datalake/');

# Path s3a://datalake is the holding directory. We dont give full file path. Only parent directory
CREATE TABLE IF NOT EXISTS hive.LPD_datasets_metadata.LPD_datasets_metadata (
  img_name	VARCHAR,
	size_img	INTEGER,
	img_w	INTEGER,
	img_h	INTEGER,
	area_img	INTEGER,
	x_min	DOUBLE,
	y_min	DOUBLE,
	x_max	DOUBLE,
	y_max	DOUBLE,
	bbox_w	DOUBLE,
	bbox_h	DOUBLE,
	area_bbox	DOUBLE,
	xmin_scale	DOUBLE,
	ymin_scale	DOUBLE,
	xmax_scale	DOUBLE,
	ymax_scale	DOUBLE,
	area_scale	DOUBLE,
	bbox_wscale	DOUBLE,
	bbox_hscale	DOUBLE
)
WITH (
  external_location = 's3a://datalake/',
  format = 'PARQUET'
);
```

## AirFlow

When we need to run and set up the tasks, we need to attach to AirFlow's container and install the corresponding lib

 
