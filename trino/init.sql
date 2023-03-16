-- Need to manually run each query now.

CREATE SCHEMA IF NOT EXISTS hive.LPD_datasets_metadata
WITH (location = 's3a://datalake/');

-- Path s3a://iris/iris_data is the holding directory. We dont give full file path. Only parent directory
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

-- Testing
SELECT 
  y_min,
  area_scale
FROM hive.LPD_datasets_metadata.LPD_datasets_metadata
LIMIT 10;

SHOW TABLES IN hive.iris;