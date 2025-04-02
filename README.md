# Barclays

 # API Call Analysis and Alert System using AI

 ## Problem Statement
AI-Powered API Monitoring and Anomaly Detection System for Large-Scale Distributed Platforms.

## Challenge
Develop an AI-powered monitoring solution for a large-scale, distributed multi-API software platform that generates vast amounts of log data from high-frequency API calls. The system spans various environments, including on-premises, cloud, and multi-cloud setups. APIs from these diverse environments can be part of a single request journey, adding complexity to monitoring and analysis. The system should:

- Automatically analyze API performance
- Detect anomalies
- Provide predictive insights to maintain optimal platform health

## Objectives
- Detect and analyze response time anomalies across all APIs, regardless of hosting environment.
- Identify and alert on error rate anomalies for individual APIs.
- Predict potential issues in end-to-end request journeys across multiple environments.
- Forecast the impact of API issues on system reliability and user experience.


## Technology Stack
- **Python** (for analysis and ML models)
- **Databases** (SQL/NoSQL for storing logs)
- **AWS** (if cloud technology is required)
- **ELK Stack (Elasticsearch, Logstash, Kibana)** (for log aggregation and visualization)
- **Kafka** (for real-time streaming of logs)
- **OpenTelemetry** (for distributed tracing and log collection)
- **Docker** (for containerization)
- **Locust** (for load testing)

## System Flow
1. **Microservices Setup:**
   - Built three microservices:
     - `api-go` (Golang + Gin)
     - `api-js` (Node.js + Express)
     - `api-python` (Flask)
   - Each microservice:
     - Listens on specific ports (5001, 5002, 5003).
     - Simulates API response times with random delays (50ms to 500ms).
     - Randomly fails 20% of the time (returns 500 Internal Server Error).
     - Returns a JSON response with a message and response time.

2. **Aggregator Service:**
   - A Flask-based service aggregates responses from multiple APIs.
   - Uses Locust to simulate multiple users sending requests.

3. **Log Collection & Storage:**
   - OpenTelemetry collects logs.
   - Logs are stored in **Kibana** for visualization.

4. **Anomaly Detection & Alerting:**
   - **Response Time Anomalies:**
     - Detect spikes using rolling percentiles (95th/99th) with Z-score or MAD.
     - Train **Isolation Forest** to detect abnormal response times.
   - **Error Rate Anomalies:**
     - Track 5xx errors using percentile-based thresholds.
     - Use **Poisson distribution** for rare error spike modeling.
   - **Failure Forecasting:**
     - **Short-Term Alerts:** Prophet-based model.
     - **Long-Term Patterns:** LSTM for deep failure trends.

5. **Predicting API Impact on System Performance:**
   - **Monte Carlo Simulation** estimates system downtime and user impact.
   - **LSTM** detects long-term pattern shifts in API performance.

6. **Alerting Mechanism:**
   - Response time exceeds threshold → **Alert triggered**
   - Failure detected → **Alert triggered**
   - Error rate exceeds 99th percentile → **Alert triggered**
   - API predicted to fail → **Alert triggered**

7. **Dashboard & Insights:**
   - Real-time error rate monitoring (various charts in Kibana).
   - Automatically add new applications to monitoring as logs start flowing.
  
  ## Project Structure
```
Barclays/
│── docker-compose.yml
│── Dockerfile  # For the aggregator service
│── requirements.txt  # Dependencies for the aggregator
│── aggregator.py  # The Flask-based API aggregator
│
├── api-python/  # Python microservice
│   │── Dockerfile
│   │── app.py
│   │── requirements.txt
│
├── api-js/  # Node.js microservice
│   │── Dockerfile
│   │── server.js
│   │── package.json
│
├── api-go/  # Go microservice
│   │── Dockerfile
│   │── main.go
│
└── opentelemetry/  # OpenTelemetry configuration
    │── otel-config.yaml
```
## UI Overview 

![Home Dashboard Sidebar](https://github.com/user-attachments/assets/75f17cb5-6859-4118-892c-67844936f4e5)

![Environment Comparison](https://github.com/user-attachments/assets/bdd000a5-d67f-49f9-9c76-600cb66c213f)

![API Performance Metrices](https://github.com/user-attachments/assets/bca08d4f-51d3-466f-bb1b-8759b5edc5ec)

![Alert Configuration](https://github.com/user-attachments/assets/4b47d130-a862-4a74-87d0-4788074631e7)

![Home Dashboard](https://github.com/user-attachments/assets/f7af8e51-f285-40c3-8e00-471bf0fc263d)


![Anomaly Detection Center](https://github.com/user-attachments/assets/18a29297-8a75-402b-8b95-a29faaa7f80b)


## Setup & Execution
1. **Build & Start Services:**
   ```bash
   docker compose up --build
   ```
2. **Check Running Containers:**
   ```bash
   docker ps
   ```

3. **Call API Request using Flask Aggregator:**
   ```bash
   curl -X GET "http://127.0.0.1:5000/aggregate"
   ```
## Extra Features
- **Scalability:** Supports multiple instances using the same data source.
- **Root Cause Analysis:**
  - Streams error logs via Kafka/Kinesis.
  - Correlates using `request_id` to isolate root causes.
- **Adaptive Response Time Thresholds:** Increases thresholds for high-traffic APIs to account for expected latency.

## Benefits
- **Real-time insights** into system health.
- **Predictive analytics** for proactive issue resolution.
- **Actionable alerts** to minimize disruptions in high-traffic environments.
- **End-to-end monitoring** across multiple hosting infrastructures.

---

This project ensures robust monitoring, anomaly detection, and predictive analysis for large-scale API-based platforms, optimizing reliability and user experience across diverse hosting environments.
