# Cloud Data Fusion for PCA

## Fundamentals
- **Service Type**: Fully managed, visual (GUI) data integration / ETL service.
- **Base Technology**: Based on open-source **CDAP**.
- **The Core Value**: "Democratizing data engineering." Allows people who don't code to build Big Data pipelines.

## When to Choose Data Fusion (Exam Clues)
- **"Visual interface"** / **"Drag-and-drop"**.
- **"No-code / Low-code"** requirements.
- **"Large library of connectors"** (SAP, Salesforce, Oracle, etc.).
- **"Data Lineage"** tracking is required (seeing the history of data transformations).

## Decision Matrix: The "Big Three" ETL Tools

| Tool | Focus | Why pick it? |
| :--- | :--- | :--- |
| **Data Fusion** | **Visual / Enterprise** | No-code, legacy connectors, data lineage. |
| **Dataflow** | **Streaming / Real-time** | High scale, complex logic, unified stream/batch code. |
| **Dataproc** | **Lift & Shift** | Running existing Hadoop/Spark jobs without rewriting them. |

## Important Points
- **Architecture**: It actually runs on **Dataproc** clusters under the hood (though this is managed for you).
- **Wranger**: A tool within Data Fusion that lets you "clean" and "shape" data visually before the pipeline runs.
- **Deployment**: High availability is supported via a Private IP deployment into your VPC.

## Tips for the Exam
- If the team is **"Legacy SQL-only"** or **"non-technical"**, choose **Data Fusion**.
- If the goal is **"High performance / high scale streaming"**, choose **Dataflow**.
- If the goal is **"Moving an existing Hadoop cluster"**, choose **Dataproc**.
