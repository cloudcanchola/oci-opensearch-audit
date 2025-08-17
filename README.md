# OpenSearch-IAM Audit
Over the past three years, I have worked with customers struggling to manage multiple environments and audit user data. 
While SIEM solutions exist, not every organization has one implemented, so I developed alternatives, 
documented in other repositories. This repository focuses on setting up an OpenSearch instance, configuring dashboards, 
and providing a script-based ingestion method. In this demo, the script will be executed manually. 
The goal is to showcase a lightweight approach to monitoring and analyzing audit data 
without requiring a full SIEM deployment.

## Table of Contents
- [Summary](#-summary)
- [Project Structure](#-project-structure)
- [Environment Configuration](#-environment-configuration)
- [Usage](#-usage)

---

## Summary

---

## 📂 Project Structure
```
project-root/
├── opensearch/ # Files to create opensearch, opensearch dashboards ond ingest
    ├── data-prepper-config.yml
    ├── pipelines.yml
    └── podman-compose.yml 
├── scripts/ 
├── utils/ 
├── .env
├── README.md 
└── requirements.txt 
```

---

## ⚙️ Environment Configuration

In case you would like to configure .env and create config from those variables 

```bash
TENANCY=<tenancy_ocid>
USER=<user_ocid>
FINGERPRINT=<fingerprint>
KEY_FILE=<path_to_private_key>
REGION=<region>
INGEST_URL=<endpoint>
```

---

## ▶️ Usage

Run compose command, this will create 3 containers
OpenSearch, OpenSearch Dashboards and OpenSearch Ingest setup
(For the sake of this demo security is disabled).

```bash
podman-compose up -d
 ```

Once containers are up and running, execute the oci_audit_to_ingest.py
the script limit is 92 days, but remember to adjust and control larger data sets.

```bash
python -m scripts.oci_audit_to_ingest --time-start 2025-07-01 --time-end 2025-08-16
```
---

