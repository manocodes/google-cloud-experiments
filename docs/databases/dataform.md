# Dataform for PCA

## Fundamentals
- **Service Type**: Fully managed service for data modeling and ELT (Extract, Load, Transform) in BigQuery.
- **The Core Value**: Allows data teams to treat SQL like software (version control, testing, environments).
- **Git-Native**: It **requires** a Git repository (GitHub/GitLab/Bitbucket) to store the code.

## Key Features
1. **The DAG (Directed Acyclic Graph)**: Automatically manages the execution order of SQL scripts based on dependencies.
2. **SQLX**: An extension of SQL that adds the `${ref()}` function, allowing for dynamic table references and code reuse.
3. **Assertions**: Built-in data quality tests (e.g., uniquely check, non-null check).
4. **Environments**: Easily manage separate schemas for `Development`, `Staging`, and `Production` using the same codebase.

## Dataform vs. Other Tools

| Scenario | Use This Tool |
| :--- | :--- |
| **"Scale SQL modeling in BigQuery"** | **Dataform** |
| **"Visual ETL for non-coders"** | **Cloud Data Fusion** |
| **"Lift and shift Hadoop/Spark"** | **Dataproc** |
| **"Real-time stream processing"** | **Dataflow** |

## PCA Exam Tip: "Dataform vs. dbt"
While **dbt (data build tool)** is the most famous open-source tool for this, **Dataform** is Google's native equivalent. On the exam, if the question asks for a "Google-native" way to manage a transformation pipeline in BigQuery, choose **Dataform**.

## Workflow
1. **Develop**: Write SQLX code in the Dataform Cloud Development Environment.
2. **Test**: Run assertions to verify data quality.
3. **Version**: Commit and push changes to GitHub.
4. **Deploy**: Schedule the execution of the modeling workflow in BigQuery.
