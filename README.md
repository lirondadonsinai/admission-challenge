# Performance Engineer – Admission Challenge

## Background
Our company has a web application for inventory management.
Users report that the application is slow.

Your task is to analyze the performance and suggest improvements.

## System Overview
The system consists of:
- **Web** – Nginx frontend
- **API** – FastAPI backend
- **Database** – PostgreSQL
- **Monitoring** – Prometheus

All services are provided via **Docker Compose**.

## Tasks

### 1. Identify the Bottleneck
Find the main reason the system is slow.
Examples:
- Slow API responses
- Database performance issues
- High CPU or memory usage

Explain what is slow and why.

### 2. Recommend Improvements
Suggest practical solutions to improve performance.
Explain how each solution helps - Use AI if needed.

Examples:
- Database indexing
- Caching
- Better resource usage

### 3. Add Graphs
Provide graphs to support your findings.
Examples:
- Response time
- Requests per second
- CPU or memory usage

Graphs can be real or simulated, but clearly explain them.

## Deliverables
Submit a short report including:
- Problem summary
- Bottleneck explanation
- Recommendations
- Graphs / Screenshots with short explanations

Optional: test scripts.

---

## Getting Started

### Prerequisites
- Docker
- Docker Compose

### Run the System
From the project root directory, run:

```bash
docker compose up --build
```

web:
http://localhost

app metrics:
http://localhost/api/metrics

prometheus:
http://localhost:9090

## Notes
- You may simulate data if needed
- Focus on clear thinking, not complex tools

Please contact me if you have any questions.
liron.sinai@flolive.net
