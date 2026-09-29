# Cost-Of-Care-Analytics

A Serverless Healthcare Data Engineering Project using Event-Driven Pipeline with AWS (S3, Lambda, SQS, Aurora, SNS, QuickSight).

## 📌 Architecture Diagram
![Architecture Diagram](https://github.com/SATWIKKUMARGANTA/Cost-Of-Care-Analytics/blob/main/Architecture/Architecture.jpeg)

## 🏗️ Architecture Flow
1.  **Ingestion & Validation Layer:** S3 Source Bucket (Raw Claims/Cost Files) -> Lambda Pre-processing (1. File validations)
2.  **Queueing & Core Processing Layer:** SQS Queue-1 (2) -> Lambda Processing (3. 2. Data processing) -> Target & Auditing DB (4)
3.  **Post-Processing Layer:** SQS Queue-2 (5) -> Lambda Post-processing (6)
4.  **Archival & Notification Layer:** Post-processing -> S3 Archive (7) + S3 Failure (on error) -> SNS (8)
5.  **BI & Analytics Layer:** Target DB -> Amazon QuickSight (9. Dashboard / Analytics)

## 🛠️ Tech Stack
- **Storage:** Amazon S3 (Source, Archive, Failure)
- **Compute:** AWS Lambda (Pre-processing, Processing, Post-processing)
- **Queueing:** Amazon SQS (Queue-1, Queue-2)
- **Database:** Amazon Aurora / RDS (Target, Auditing)
- **Notification:** Amazon SNS
- **BI Tool:** Amazon QuickSight
- **Language:** Python, SQL

## 📁 Project Structure

├── architecture/
│   ├── architecture.md
│   └── Architecture_Diagram.jpeg
├── lambdas/
│   ├── pre_processing/
│   │   └── lambda_function.py
│   ├── data_processing/
│   │   └── lambda_function.py
│   └── post_processing/
│       └── lambda_function.py
├── sql/
│   ├── target_ddl.sql
│   └── auditing_ddl.sql
├── sqs/
│   └── queue_config.json
├── requirements.txt
└── README.md

## 🚀 Key Features
- Fully Serverless Event-Driven Pipeline
- Decoupled Architecture with SQS for retry & fault tolerance
- Audit Trail for compliance (Auditing DB)
- Failure Bucket for error isolation & reprocessing
- Archive for historical data retention
- SNS Alerts for real-time monitoring
- QuickSight Integration for Cost of Care Insights

## 📊 Gold Layer Reports (Target DB)
1.  `cost_by_member/` - Total cost and claims by member
2.  `cost_by_provider/` - Cost breakdown by provider / facility
3.  `monthly_pmpm/` - Per Member Per Month cost trends

## 📊 Dashboards & Analytics

### QuickSight Dashboards
Screenshots are available in `/dashboards/` folder

- **Cost of Care Overview Dashboard** - Total cost, PMPM, Member count
- **High-Cost Members Dashboard** - Top 10 high-cost claimers
- **Provider Performance Dashboard** - Cost by provider, utilization metrics

