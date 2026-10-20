# ETL Pipeline Architecture
**Created:** 2024-10-20
**Status:** Planning

## Overview
Data pipeline to move data from sources to warehouse.

## Sources
- PostgreSQL (users, transactions)
- MongoDB (events, sessions)
- CSV files (daily reports)

## Processing Steps
1. **Extract**: Read from source databases
2. **Transform**: Clean and enrich data
3. **Load**: Write to Snowflake warehouse

## Airflow DAG
```
extract_db → transform_data → validate_schema → load_warehouse → notify_complete
```

## Monitoring
- Check [[../Scripts/Schema Validation Script|schema validation script]]
- Reference [[../Scripts/Data Quality Tests|data quality tests]]

## Wikilinks
- [[../Backend Engineering/Schemas/User Schema|User Schema Reference]]
- [[../Project Documentation/Sprint 3 Goals|Sprint Goals]]