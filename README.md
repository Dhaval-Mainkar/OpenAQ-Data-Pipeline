# 🌍 OpenAQ Air Quality Data Engineering Pipeline

## 📌 Overview

This project is an end to end data engineering pipeline built to ingest, process, and visualize real time air quality data from the [OpenAQ](https://openaq.org/) public API. It covers the full lifecycle from streaming raw API data through Kafka on AWS, transforming it through a Medallion Architecture on Databricks, all the way to the final report in Power BI, runs on a fully automated schedule with zero manual intervention.

Built entirely from scratch as a hands on learning project, it mirrors real world production patterns across streaming ingestion, cloud infrastructure, batch processing, and business reporting.

---

## 📊 Data Source

**OpenAQ** is a free, open source platform that aggregates real time air quality readings from sensors across the world, covering pollutants like PM2.5, PM10, NO2, and more. The data is publicly available through a [REST API](https://docs.openaq.org/about/about) and is continuously updated as sensors report new readings.

---

## ❓ The Problem

Air pollution is one of the most pressing environmental and public health challenges of our time, yet most people have no easy way to track what they are actually breathing day to day. Raw air quality data exists publicly, but it is scattered, updated continuously, and in a format that is completely inaccessible to anyone who is not technical.

This project solves that by building a fully automated pipeline that takes live sensor readings, cleans and structures them, and surfaces them in a way that is easy to consume whether you are a data analyst running a Power BI report, or a team that only has AWS access. Every stage of this pipeline, from ingestion to transformation to reporting, runs on a schedule so the data is always fresh and the insights are always ready with no human intervention needed at any point.

---

## 🗺️ Architecture Diagram


---

## 🚀 How the Pipeline Works

The pipeline follows a structured, end to end flow with scheduling built in at every layer:

**1. Ingestion :**
Dockerized Python producers run on AWS ECS Fargate and call the OpenAQ API on a schedule. The data is published as messages to an Apache Kafka topic running on EC2 in KRaft mode. Consumers pick up those messages and land the raw JSON into Amazon S3. In addition to the streaming data, certain data from the API that is rarely updated which is extracted separately using a scheduled AWS Lambda function, triggered based on how frequently that data is expected to change rather than continuously.

**2. Medallion Architecture on Databricks :**
The raw data in S3 flows through a three layer Medallion Architecture in Databricks:

- 🥉 **Bronze** — Raw JSON as is, directly from S3. No transformations, just ingestion.
- 🥈 **Silver** — Cleaned, flattened, and structured data. Nested JSON is exploded into proper tabular format, data is transformed and validated.
- 🥇 **Gold** — Curated, aggregated, and business ready data optimized for reporting, analytics, and decision making.

**3. Procedural Pipeline :**
Each layer in Databricks is triggered sequentially as a scheduled pipeline Bronze runs first, Silver picks up after Bronze completes, and Gold runs after Silver. This ensures data integrity across every layer without manual execution.

**4. AWS Athena — Data Access for Non Databricks Users :**
After each transformation layer, the processed data is written to S3 as Parquet files , a columnar storage format that makes analytical queries significantly faster since only the columns needed are read rather than the entire dataset, while also compressing far better than CSV or JSON, reducing storage costs. These Parquet files act as a reliable snapshot, and because Athena can query Parquet on S3 directly, any team or role with AWS access can run SQL queries against the data without needing Databricks, Python, or any additional setup, giving them full visibility and a sense of control over the data in a way that fits naturally into how access is typically structured in a corporate environment

**5. Power BI — Scheduled Incremental Reports :**
The Gold layer feeds into a Power BI report with **incremental refresh** configured, meaning only new data is pulled on each refresh cycle rather than reloading everything from scratch. 

The entire process is scheduled end to end from the Lambda function triggering ingestion, through the Databricks pipeline, to the Power BI incremental refresh so the report is always up to date automatically.

---

## 🎯 What This Delivers

✅ A fully scheduled, zero touch pipeline right from API ingestion to final report, no manual steps required.

✅ A Medallion Architecture (Bronze → Silver → Gold) ensuring clean, trustworthy, and analytics ready data at every stage.

✅ An Athena table giving any AWS user direct SQL access to monitor air quality data.

✅ A Power BI report with incremental refresh so stakeholders always see fresh data without full reloads.

✅ Real infrastructure built and debugged from scratch — Kafka on EC2, ECS Fargate, Docker, ECR, S3, Databricks, Athena, and Power BI all wired together end to end.

---

## # 🛠️ Technologies Used

-   **[Apache Kafka](https://kafka.apache.org/)**

-   **[Docker](https://www.docker.com/)**

-   **[Amazon Web Services (AWS)](https://aws.amazon.com/)**

-   **[SQL](https://www.w3schools.com/sql/)**

-   **[PySpark](https://spark.apache.org/docs/latest/api/python/)**

-   **[Databricks](https://www.databricks.com/)**

-   **[Python](https://www.python.org/)**

-   **[Jupyter Notebook](https://jupyter.org/)**

-   **[Microsoft Power BI](https://powerbi.microsoft.com/)**

-   **[Git](https://git-scm.com/)**